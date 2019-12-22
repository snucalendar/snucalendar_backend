from django.urls import path
from . import views

urlpatterns = [
    path('token/', views.token, name='token'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('userinfo/', views.userinfo, name='userinfo'),
    path('calendar/month/<int:year>/<int:month>/', views.calendarMonth, name='calendarMonth'),
    path('calendar/date/<int:year>/<int:month>/<int:date>/', views.calendarDate, name='calendarDate'),
    
    path('api/events/', views.events),
    path('api/events/<int:id>/', views.event),
    path('api/events/<int:id>/participate/'),
    path('api/events/<int:id>/rating'),
    path('api/search/<str:keyword>'),
    path()
    
]
