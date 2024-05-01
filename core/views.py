from django.shortcuts import render

def index(request):
    return HttpResponse("welcome to my shop")