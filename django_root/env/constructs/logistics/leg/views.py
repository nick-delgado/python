from django.shortcuts import render
from django.http import HttpResponse
import requests

# Create your views here.
def home(request):
    response = requests.get('http://127.0.0.1:8000/aircrafts/')
    data = response.json()

    return HttpResponse("Hello, world" + str(data))
