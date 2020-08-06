from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("forcast/<str:cityname>/<int:period>", views.forcast, name="forcast"),
]

