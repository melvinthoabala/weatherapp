from django.shortcuts import render
from django.http import HttpResponse
import requests
from django.http import JsonResponse
from django.conf import settings
from geopy.geocoders import Nominatim
import statistics
from django.core.cache import cache


def index(request):
    return HttpResponse("Hello, Welcome to the weather App.")


def forcast(request, cityname, period):

    geolocator = Nominatim(user_agent="weatherapi")
    location = geolocator.geocode(cityname)
    findfromcache = cache.get(hash(cityname + period))
    if findfromcache == None:
        url = "http://api.openweathermap.org/data/2.5/onecall?"
        payload = {
            "lat": location.latitude,
            "lon": location.longitude,
            "units": "metric",
            "appid": settings.OPENWEATHERAPIKEY,
        }
        city_weather = requests.get(url, payload).json()

        temperatures = []
        humidity = []
        for day in city_weather[period]:
            if period == "hourly":
                temperatures.append(day["temp"])
            else:
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
        cache.add(hash(cityname + period), results, 30000)
        return JsonResponse(results)
    else:
        return JsonResponse(findfromcache)

