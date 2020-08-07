from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("forcast/<str:cityname>/<str:period>", views.forcast, name="forcast"),
]

