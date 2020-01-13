import json
from json import JSONDecodeError
from datetime import datetime, date
from PIL import Image
from io import BytesIO

from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import ensure_csrf_cookie
from django import forms

from .models import Event, Like, Posting
from users.models import CalendarUser



class PostingForm(forms.Form):
    """Image upload form."""
    title = forms.CharField(max_length=100)
    image = forms.ImageField()
    content = forms.CharField(widget = forms.Textarea)

    

@ensure_csrf_cookie
def token(request):
    if request.method == 'GET':
        return HttpResponse(status=204)
    else:
        return HttpResponseNotAllowed(['GET'])

def login(request):
    if request.method == 'POST':
        try:
            req_data = json.loads(request.body.decode())
            email = req_data['email']
            password = req_data['password']
        except (KeyError, JSONDecodeError):
            return HttpResponseBadRequest()

        user = authenticate(username=email, password=password)
        if user is not None:
            auth_login(request, user)
            return HttpResponse(status=204)
        else:
            return HttpResponse(status=401)

    else:
        return HttpResponseNotAllowed(['POST'])

def logout(request):
    if request.method == 'GET':
        auth_logout(request)
        return HttpResponse(status=204)
    else:
        return HttpResponseBadRequest(['GET'])

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

def calendarMonth(request, year, month):
    if request.method == 'GET':
        return_json = []
        for i in range(1, 31):
            dict = {
                "year" : year,
                "month" : month,
                "date" : i,
                "events" : []
            }
            return_json.append(dict)
        events = list(Event.objects.filter(year = year, month = month).values())
        for event in events:
            event['author'] = CalendarUser.objects.get(id=event['author_id']).username
            del event['author_id']
            return_json[int(event['date'])-1]['events'].append(event)
        return JsonResponse(return_json, safe=False, status=200)
    else:
        return HttpResponseNotAllowed(['GET'])


def calendarDate(request):
    if request.method == 'GET':
        return_json = {}
        events = list(Event.objects.filter(year = year, month = month, date = date).values())
        for event in events:
            event['author'] = CalendarUser.objects.get(id=event['author_id']).username
            del event['author_id']
        return_json['events'] = events
        return_json['year'] = year
        return_json['month'] = month
        return_json['date'] = date
        return JsonResponse(return_json, safe=False, status=200)
    else:
        return HttpResponseNotAllowed(['GET'])

def events(request):
    if request.method == 'POST':
        try:
            req_data = json.loads(request.body.decode())
            author = request.user
            title = req_data['title']
            content = req_data['content']
            date = req_data['date']
            time = req_data['time']
            type = req_data['type']
        except (KeyError, json.decoder.JSONDecodeError):
            return HttpResponseBadRequest()
        date = datetime.strptime(date, '%Y/%m/%d').date()
        time = datetime.strptime(time, '%H::%M::%S').time()

        new_event = Event(title = title,
                        author = author, 
                        content = content, 
                        year = date.year,
                        month = date.month,
                        date = date.date, 
                        time = time, 
                        type = type)
        new_event.save()
        new_like = Like(like = 0, event = new_event)
        new_like.save()
        return HttpResponse(status = 201)
    else: 
        return HttpResponseNotAllowed(['POST'])

def event(request, id):
    if request.method == 'GET':
        try:
            event = Event.objects.get(id=id)
        except Event.DoesNotExist:
            return HttpResponse(status = 404)
        return_json = {
            "title" : event.title,
            "content" : event.content,
            "date" : event.year+'/'+event.month+'/'+event.date,
            "time" : event.time.strftime("%H::%M::%S"),
            "type" : event.type,
            "like" : event.like.like
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
            type = req_data['type']
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
        event.year = date.year
        event.month = date.month
        event.date = date.date
        event.time = time
        event.type = type
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

def participate(request, id):
    if request.method == 'POST':
        try:
            req_data = json.loads(request.body.decode())
            type = req_data['type']
        except (KeyError, json.decoder.JSONDecodeError):
            return HttpResponseBadRequest()
        try:
            event = Event.objects.get(id=id)
        except Event.DoesNotExist:
            return HttpResponse(status=404)
        
        if type == 'participate':
            event.participate.add(request.user)
        elif type == 'interested':
            event.interested.add(request.user)
    else:
        return HttpResponseNotAllowed(['POST'])

def like(request, id):
    if request.method == 'POST':
        try:
            event = Event.objects.get(id=id)
        except Event.DoesNotExist:
            return HttpResponse(status=404)
        if event.like.user.filter(id=request.user.id).count == 0:
            event.like.user.add(request.user)
            event.like.like += 1
        else:
            event.like.user.remove(request.user)
            event -= 1
        return HttpResponse(status = 200)
    else:
        return HttpResponseNotAllowed(['POST'])

def search(request, keyword):
    if request.method == 'GET':
        events = list(Event.objects.filter(title__icontains=keyword).values())
        for event in events:
            event['author']= CalendarUser.objects.get(id=event['author_id']).username
            del event['author_id']
        return JsonResponse(events, safe=False)
    else:
        return HttpResponseNotAllowed(['GET'])

def myevents(request):
    if request.method == 'GET':
        user = request.user
        participated_events = list(user.participated_events.all().values())
        interested_events = list(user.interested_events.all().values())
        for event in participated_events:
            event['author']= CalendarUser.objects.get(id=event['author_id']).username
            del event['author_id']
        for event in interested_events:
            event['author']= CalendarUser.objects.get(id=event['author_id']).username
            del event['author_id']
        return_json = {
            "participated_events" : participated_events,
            "interested_events" : interested_events
        }
        return JsonResponse(return_json, safe=False)
    else:
        return HttpResponseNotAllowed(['GET'])

def postings(request, id):
    if request.method == 'POST':
        user = request.user
        form = ImageUploadForm(request.POST, request.FILES)
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
        try:
            event = Event.objects.get(id=id)
        except Event.DoesNotExist:
            return HttpResponse(status=404)
        postings = list(Posting.objects.filter(event=event).values())
        for posting in postings:
            posting.upload_date = posting.upload_date.strftime("%Y/%m/%d %H::%M::%S")

        return JsonResponse(json.dumps(postings), safe=False)
    else:
        return HttpResponseNotAllowed(['POST', 'GET'])   

def posting(request, id):
    try:
        posting = Posting.objects.get(id=id)
    except Posting.DoesNotExist:
        return HttpResponse(status=404)
    
    return_dic = {
        title : posting.title,
        image : posting.image,
        author : CalendarUser.get(id=posting.author_id).username,
        event : posting.event,
        content : posting.content,
        upload_date : posting.upload_date.strftime("%Y/%m/%d %H::%M::%S")
    }

    return JsonResponse(json.dumps(return_dic), safe=False)

def postdate_pagination(request, start, interval):
    pass

def duedate_pagination(request, start, interval):
    pass