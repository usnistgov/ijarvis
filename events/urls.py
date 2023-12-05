from django.views.generic import TemplateView
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.school),
    path(r"aims", views.aims),
    path(r"aims2022", views.aims),
    path(r"aims2020", views.aims),
    path(r"aims2019", views.aims),
    path(r"aims2018", views.aims),
    path(r"qmms", views.qmms),
    path(r"qmms2020", views.qmms),
    path(r"school", views.school),
]
