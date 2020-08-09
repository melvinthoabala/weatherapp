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
    allowedperiods = ['hourly', 'daily']
    if period not in allowedperiods:
        return HttpResponse("Invalid period provided")

    find_from_cache = cache.get(hash(cityname + period))
    
    if find_from_cache == None:
        
        city_weather = get_weather_data(cityname)
        if 'cod' in city_weather and city_weather['cod'] != 200:
            # This is key is returned on error by openweather
            # Log request and response for system audit
            return HttpResponse("Something bad happend")

        results = construct_weather_data_response(city_weather,period)
        cache.add(hash(cityname + period), results, 30000)
        return JsonResponse(results)
    else:
        return JsonResponse(find_from_cache)


def get_lat_long_from_cityname(cityname):
    geolocator = Nominatim(user_agent="weatherapi")
    return geolocator.geocode(cityname)

def get_weather_data(cityname):
    location = get_lat_long_from_cityname(cityname)
    url = "http://api.openweathermap.org/data/2.5/onecall?"
    payload = {
        "lat": location.latitude,
        "lon": location.longitude,
        "units": "metric",
        "appid": settings.OPENWEATHERAPIKEY,
    }
    try:
        response = requests.get(url, payload).json()
        return response
    except requests.exceptions.RequestException as e:
        # log error for system audit
        return HttpResponse("Something bad happend")

def construct_weather_data_response(city_weather,period):
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
    return results