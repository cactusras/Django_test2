from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    context={}
    return render(request, "myApp/home.html", context)

def index(request):
    context={}
    return render(request, "myApp/index.html", context)
