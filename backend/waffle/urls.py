from django.urls import path
from . import views

urlpatterns = [
    path('token/', views.token, name='token'),
    path('login/', views.login, name='login'),
    path('logout/', views.signup, name='logout'),
    

]