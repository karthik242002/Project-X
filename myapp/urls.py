from django.urls import path 
from . import views

urlpatterns =[
    path('',views.index,name='index'),
    path('counter',views.counter,name='counter'),
    path('register',views.register,name='register'),
    path('login',views.login,name='login'),
    path('studemp',views.studemp,name='studemp'),
    
    path('chatbot',views.chatbot),

]

