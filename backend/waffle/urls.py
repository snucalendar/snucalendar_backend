from django.urls import path
from . import views

urlpatterns = [
    path('token/', views.token, name='token'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('userinfo/', views.getUserInfo, name='userinfo'),

    path('calendar/<int:year>/<int:month>/', views.calendarMonth, name='calendarMonth'),
    path('calendar/<int:year>/<int:month>/<int:date>/', views.calendarDate, name='calendarDate'),
    
    path('events/', views.events, name = 'events'),
    path('events/<int:id>/', views.event, name = 'event'),
    path('events/<int:id>/participate/', views.participate, name = 'participate'),
    path('events/<int:id>/rating/', views.rating, name = 'rating'),
    path('events/<int:id>/comments/', views.comments, name='comments'),
    path('events/<int:id>/comments/<int:cid>/', views.comment, name='comment'),

    path('search/<str:keyword>/', views.search, name='search'),

    path('myevents/', views.myevents, name = 'myevents')
    
]
