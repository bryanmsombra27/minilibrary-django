from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    # los parametros pueden ir tipados
    path("<int:day>", views.weekNumber, name="number-quote"),
    path("<str:day>", views.weekdays, name="day-quote"),
    path("", views.index, name="list-quotes"),
]
