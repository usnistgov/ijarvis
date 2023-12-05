from django.views.generic import TemplateView
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.contact),
]
