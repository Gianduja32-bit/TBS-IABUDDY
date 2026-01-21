from django.shortcuts import render

def home(request):
    return render(request, 'index.html')

def chatbot(request):
    return render(request, 'chatbot.html')
