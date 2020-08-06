from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import requests
from django.http import JsonResponse
from django.conf import settings


def index(request):
    return HttpResponse("Hello, Welcome to the weather App.")


def forcast(request, cityname, period):
    # TODO change to a POST return method not allowed on a GET, add caching move this logic to getweatherdata.py
    url = "http://api.openweathermap.org/data/2.5/weather?"
    payload = {"q": cityname, "units": "metric", "appid": settings.OPENWEATHERAPIKEY}
    city_weather = requests.get(
        url, payload
    ).json()  # request the API data and convert the JSON to Python data types
    return JsonResponse(city_weather)
