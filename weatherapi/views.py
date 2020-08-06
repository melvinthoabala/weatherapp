from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import requests
from django.http import JsonResponse
from django.conf import settings
from geopy.geocoders import Nominatim
import statistics


def index(request):
    return HttpResponse("Hello, Welcome to the weather App.")


def forcast(request, cityname, period):

    geolocator = Nominatim(user_agent="weatherapi")
    location = geolocator.geocode(cityname)

    url = "http://api.openweathermap.org/data/2.5/onecall?"
    payload = {
        "lat": location.latitude,
        "lon": location.longitude,
        "units": "metric",
        "appid": settings.OPENWEATHERAPIKEY,
        "exclude": "hourly",
    }
    city_weather = requests.get(url, payload).json()

    temperatures = []
    humidity = []
    for day in city_weather["daily"]:
        temperatures.append(day["temp"]["day"])
        humidity.append(day["humidity"])
    results = {
        "humidity": {
            "min": min(humidity),
            "max": max(humidity),
            "mean": statistics.mean(humidity),
            "median": statistics.median(humidity),
        },
        "temperature": {
            "min": min(temperatures),
            "max": max(temperatures),
            "mean": statistics.mean(temperatures),
            "median": statistics.median(temperatures),
        },
    }

    return JsonResponse(results)
