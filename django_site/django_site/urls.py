from django.contrib import admin
from django.urls import path
from web_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('api/chatbot/', views.chatbot_api, name='chatbot_api'),
]
