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
    
    path('api/events/', views.events, name = 'events'),
    path('api/events/<int:id>/', views.event, name = 'event'),
    path('api/events/<int:id>/participate/', views.participate, name = 'participate'),
    path('api/events/<int:id>/rating/', views.rating, name = 'rating'),
    path('api/events/<int:id>/comments/', views.comments, name='comments'),
    path('api/events/<int:id>/comments/<int:cid>/', views.comment, name='comment'),

    path('api/search/<str:keyword>/', views.search, name='search'),

    path('api/myevents/', views.myevents, name = 'myevents')
    
]
