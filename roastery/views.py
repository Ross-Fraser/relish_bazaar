from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def my_roastery(request):
    return HttpResponse("Hello, coffee!")