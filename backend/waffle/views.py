import json
from json import JSONDecodeError
from datetime import datetime, date
from PIL import Image

from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import ensure_csrf_cookie
from django import forms
from django.db.models import F
from django.db import transaction

from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page

from .models import Event, Like, Posting
from users.models import CalendarUser
from django.core.cache import cache

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

class PostingForm(forms.Form):
    """Image upload form."""
    title = forms.CharField(max_length=100)
    image = forms.ImageField()
    content = forms.CharField(widget = forms.Textarea)

def check_logged_in(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if args and args[0].user.is_authenticated:
            return func(*args, **kwargs)
        return HttpResponse(status=401)

    return wrapper

def checklogin(request):
    if request.user.is_authenticated:
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=401)

@ensure_csrf_cookie
def token(request):
    if request.method == 'GET':
        return HttpResponse(status=204)
    else:
        return HttpResponseNotAllowed(['GET'])

@transaction.atomic
def login(request):
    if request.method == 'POST':
        try:
            req_data = json.loads(request.body.decode())
            email = req_data['email']
            password = req_data['password']
        except (KeyError, JSONDecodeError):
            return HttpResponseBadRequest()

        user = authenticate(email=email, password=password)
        if user is not None:
            auth_login(request, user)
            return HttpResponse(status=204)
        else:
            return HttpResponse(status=401)
    elif request.method == 'OPTIONS':
        return HttpResponse(status = 204)
    else:
        return HttpResponseNotAllowed(['POST', 'OPTIONS'])

@transaction.atomic
def logout(request):
    if request.method == 'GET':
        auth_logout(request)
        return HttpResponse(status=204)
    else:
        return HttpResponseBadRequest(['GET'])

@transaction.atomic
def signup(request):  # create new
    if request.method == 'POST':
        try:
            req_data = json.loads(request.body.decode())
            username = req_data['username']
            password = req_data['password']
            email = req_data['email']
        except (KeyError, json.decoder.JSONDecodeError):
            return HttpResponseBadRequest()
        if CalendarUser.objects.filter(username=username).exists():
            return HttpResponse(status=400)

        CalendarUser.objects.create_user(username=username,
                                    email=email,
                                    password=password)
        return HttpResponse(status=201)
    else:
        return HttpResponseNotAllowed(['POST'])

@transaction.atomic
def getUserInfo(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            info = {'username': request.user.username,
                    'email': request.user.email}
            return JsonResponse(info, safe=False)
        else:
            info = {'username': "",
                    'email' : ""}
            return JsonResponse(info, safe=False)
    else:
        return HttpResponseNotAllowed(['GET'])

@transaction.atomic
def calendarMonth(request, year, month):
    if request.method == 'GET':
        return_json = []
        this_month = datetime(year, month, 1).date()
        if month == 12:
            next_month = datetime(year+1, 1, 1).date()
        else:
            next_month = datetime(year, month+1, 1).date()
        for i in range(1, 32):
            dict = {
                "year" : year,
                "month" : month,
                "date" : i,
                "events" : []
            }
            return_json.append(dict)
        events = list(Event.objects
            .filter(date__gte = this_month, date__lt = next_month)
            .select_related('author')
            .values('title', 'content', 'date', 'time', 'event_type', 'interest', 'participate', 'id')
            .annotate(author = F('author__username')))
        for event in events:
            return_json[int(event['date'].day)-1]['events'].append(event)
        return JsonResponse(return_json, safe=False, status=200)
    else:
        return HttpResponseNotAllowed(['GET'])

@transaction.atomic
def calendarDate(request, year, month, date):
    if request.method == 'GET':
        return_json = {}
        events = list(Event.objects
            .filter(date = datetime(year, month, date).date())
            .select_related('author')
            .values('title', 'content', 'date', 'time', 'event_type', 'interest', 'participate', 'id')
            .annotate(author = F('author__username')))
        return_json['events'] = events
        return_json['year'] = year
        return_json['month'] = month
        return_json['date'] = date
        return JsonResponse(return_json, safe=False, status=200)
    else:
        return HttpResponseNotAllowed(['GET'])

@transaction.atomic
def events(request):
    if request.method == 'POST':
        try:
            req_data = json.loads(request.body.decode())
            author = request.user
            title = req_data['title']
            content = req_data['content']
            date = req_data['date']
            time = req_data['time']
            event_type = req_data['event_type']
        except (KeyError, json.decoder.JSONDecodeError):
            return HttpResponseBadRequest()
        date = datetime.strptime(date, '%Y/%m/%d').date()
        time = datetime.strptime(time, '%H::%M::%S').time()

        new_event = Event(title = title,
                        author = author, 
                        content = content,
                        date = date, 
                        time = time, 
                        event_type = event_type)
        new_event.save()
        new_like = Like(like = 0, event = new_event)
        new_like.save()

        return HttpResponse(status = 201)
    else: 
        return HttpResponseNotAllowed(['POST'])

@transaction.atomic
def event(request, id):
    if request.method == 'GET':
        try:
            event = Event.objects.select_related('author').get(id=id)
        except Event.DoesNotExist:
            return HttpResponse(status = 404)
        return_json = {
            "id" : event.id,
            "title" : event.title,
            "content" : event.content,
            "author" : event.author.username,
            "date" : event.date.strftime("%Y/%m/%d"),
            "time" : event.time.strftime("%H::%M::%S"),
            "event_type" : event.event_type,
            "like" : Like.objects.get(event=event).like
        }
        return JsonResponse(return_json, safe=False, status=200)

    elif request.method == 'PUT':
        try:
            req_data = json.loads(request.body.decode())
            author = request.user
            title = req_data['title']
            content = req_data['content']
            date = req_data['date']
            time = req_data['time']
            event_type = req_data['event_type']
        except (KeyError, json.decoder.JSONDecodeError):
            return HttpResponseBadRequest()
        date = datetime.strptime(date, '%Y/%m/%d').date()
        time = datetime.strptime(time, '%H::%M::%S').time()
        try:
            event = Event.objects.get(id=id)
        except Event.DoesNotExist:
            return HttpResponse(status=404)
        event.title = title
        event.content = content
        event.date = date
        event.time = time
        event.event_type = event_type
        event.save()
        return HttpResponse(status = 200)

    elif request.method == 'DELETE':
        try:
            event = Event.objects.get(id=id)
        except Event.DoesNotExist:
            return HttpResponse(status=404)
        event.delete()
        return HttpResponse(status = 200)
    else:
        return HttpResponseNotAllowed(['GET', 'PUT', 'DELETE'])

@transaction.atomic
def participate(request, id):
    if request.method == 'POST':
        try:
            req_data = json.loads(request.body.decode())
            event_type = req_data['event_type']
        except (KeyError, json.decoder.JSONDecodeError):
            return HttpResponseBadRequest()
        try:
            event = Event.objects.get(id=id)
        except Event.DoesNotExist:
            return HttpResponse(status=404)
        
        if event_type == 'participate':
            event.participate.add(request.user)
            event.interested.remove(request.user)
        elif event_type == 'interested':
            event.participate.remove(request.user)
            event.interested.add(request.user)
        else:
            event.participate.remove(request.user)
            event.interested.remove(request.user)
    else:
        return HttpResponseNotAllowed(['POST'])

@transaction.atomic
def like(request, id):
    if request.method == 'POST':
        try:
            like = Like.objects.get(event_id=id)
        except Event.DoesNotExist:
            return HttpResponse(status=404)
        if like.user.filter(id=request.user.id).count == 0:
            like.user.add(request.user)
            like.like += 1
        else:
            like.user.remove(request.user)
            like.like -= 1
        return HttpResponse(status = 200)
    elif request.method == 'GET':
        try:
            like = Like.objects.get(event_id=id)
        except Event.DoesNotExist:
            return HttpResponse(status=404)
        response_dic = {}
        if like.user.filter(id=request.user.id).count == 0:
            response_dic['like'] = False
        else:
            response_dic['like'] = True
        return JsonResponse(json.dumps(response_dic),safe=False )
    else:
        return HttpResponseNotAllowed(['POST'])

@transaction.atomic
def search(request, keyword):
    if request.method == 'GET':
        events = list(Event.objects
            .filter(title__icontains=keyword)
            .select_related('author')
            .values('title', 'content', 'date', 'time', 'event_type', 'interest', 'participate', 'id')
            .annotate(author = F('author__username')))
        return JsonResponse(events, safe=False)
    else:
        return HttpResponseNotAllowed(['GET'])

@transaction.atomic
def myevents(request):
    if request.method == 'GET':
        user = request.user
        participated_events = list(Event.objects
            .filter(participate = user)
            .select_related('author')
            .prefetch_related('participate')
            .values('title', 'content', 'date', 'time', 'event_type', 'interest', 'participate', 'id')
            .annotate(author = F('author__username')))
        interested_events = list(Event.objects
            .filter(interest = user)
            .select_related('author')
            .prefetch_related('interest')
            .values('title', 'content', 'date', 'time', 'event_type', 'interest', 'participate', 'id')
            .annotate(author = F('author__username')))
        return_json = {
            "participated_events" : participated_events,
            "interested_events" : interested_events
        }
        return JsonResponse(return_json, safe=False)
    else:
        return HttpResponseNotAllowed(['GET'])

@transaction.atomic
def myevents_calendar(request, year, month):
    if request.method == 'GET':
        user = request.user
        return_json = []
        this_month = datetime(year, month, 1).date()
        if month == 12:
            next_month = datetime(year+1, 1, 1).date()
        else:
            next_month = datetime(year, month+1, 1).date()
        for i in range(1, 32):
            dict = {
                "year" : year,
                "month" : month,
                "date" : i,
                "participated_events" : [],
                "interested_events" : []
            }
            return_json.append(dict)
        participated_events = list(Event.objects
            .filter(participate = user, date__gte = this_month, date__lt = next_month)
            .select_related('author')
            .prefetch_related('participate')
            .values('title', 'content', 'date', 'time', 'event_type', 'interest', 'participate', 'id')
            .annotate(author = F('author__username')))
        interested_events = list(Event.objects
            .filter(interest = user, date__gte = this_month, date__lt = next_month)
            .select_related('author')
            .prefetch_related('interest')
            .values('title', 'content', 'date', 'time', 'event_type', 'interest', 'participate', 'id')
            .annotate(author = F('author__username')))
        for participated in participated_events:
            return_json[int(participated['date'].day)-1]['participated_events'].append(participated)
        for interested in interested_events:
            return_json[int(interested['date'].day)-1]['interested_events'].append(interested)
        return JsonResponse(return_json, safe=False)
        
    else:
        return HttpResponseNotAllowed(['GET'])

@transaction.atomic
def postings(request, id):
    if request.method == 'POST':
        user = request.user
        form = PostingForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
        else:
            return HttpResponseBadRequest()
        try:
            event = Event.objects.get(id=id)
        except:
            return HttpResponse(status=404)
        
        new_posting = Posting(title = title,
            image = image,
            content = content,
            author = user,
            event = event)
        new_posting.save()
        return HttpResponse(status=200)
        
    elif request.method == 'GET':
        postings = list(Posting.objects
            .filter(event_id=id)
            .select_related('author', 'event')
            .values('title', 'content', 'image', 'upload_date', 'id')
            .annotate(author = F('author__username'), event = F('event')))
        for posting in postings:
            posting['upload_date'] = posting['upload_date'].strftime("%Y/%m/%d %H::%M::%S")
        return JsonResponse(json.dumps(postings), safe=False)
    else:
        return HttpResponseNotAllowed(['POST', 'GET'])   

@transaction.atomic
def posting(request, id):
    if request.method == 'GET':
        try:
            posting = Posting.objects.select_related('author', 'event').get(id=id)
        except Posting.DoesNotExist:
            return HttpResponse(status=404)
        
        return_dic = {
            "id" : posting.id,
            "title" : posting.title,
            "image" : posting.image,
            "author" : posting.author.username,
            "event" : posting.event.id,
            "content" : posting.content,
            "upload_date" : posting.upload_date.strftime("%Y/%m/%d %H::%M::%S")
        }
        return JsonResponse(json.dumps(return_dic), safe=False)
    else:
        return HttpResponseNotAllowed(['GET'])

@transaction.atomic
def postdate_pagination(request, start, interval):
    if request.method == 'GET':
        postings = list(Posting.objects
            .all()
            .select_related('author', 'event')
            .order_by('-upload_date')
            .values('title', 'content', 'image', 'upload_date', 'id', 'event_id')
            .annotate(author = F('author__username'), event_date = F('event__date'))[start-1:start+interval-1])
        for posting in postings:
            posting['upload_date'] = posting['upload_date'].strftime("%Y/%m/%d %H::%M::%S")
            posting['event_date'] = posting['event_date'].strftime("%Y/%m/%d")
        return JsonResponse(json.dumps(postings), safe=False)
    else:
        return HttpResponseNotAllowed(['GET'])

@transaction.atomic
def duedate_pagination(request, start, interval):
    if request.method == 'GET':
        postings = list(Posting.objects
            .all()
            .select_related('author', 'event')
            .order_by('-event__date','-event__time')
            .values('title', 'content', 'image', 'upload_date', 'id', 'event_id')
            .annotate(author = F('author__username'), event_date = F('event__date'))[start-1:start+interval-1])
        for posting in postings:
            posting['upload_date'] = posting['upload_date'].strftime("%Y/%m/%d %H::%M::%S")
            posting['event_date'] = posting['event_date'].strftime("%Y/%m/%d")
        return JsonResponse(json.dumps(postings), safe=False)
    else:
        return HttpResponseNotAllowed(['GET'])

@transaction.atomic
def posting_search(request, keyword):
    if request.method == 'GET':
        postings = list(Posting.objects
            .filter(title__icontains=keyword)
            .select_related('author', 'event')
            .values('title', 'content', 'image', 'id')
            .annotate(author = F('author__username'), event = F('event')))
        for posting in postings:
            posting['upload_date'] = posting['upload_date'].strftime("%Y/%m/%d %H::%M::%S")
        return JsonResponse(json.dumps(postings), safe=False)
    else:
        return HttpResponseNotAllowed(['GET'])

@transaction.atomic
def posting_events_list(request):
    if request.method == 'GET':
        return_json = []
        today = date.today()
        events = list(Event.objects
            .filter(date__gte = today)
            .values('title','date', 'time', 'event_type', 'id'))
        for event in events:
            return_json.append(event)
        return JsonResponse(return_json, safe=False, status=200)