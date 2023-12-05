#from core_main_app.utils.rendering import render
from django.shortcuts import render
from .forms import ContactForm
from django.http import HttpResponse
from jarvis.io.vasp.inputs import Poscar
from jarvis.ai.descriptors.cfid import CFID
import numpy as np
import os
import pickle
from numpy import linalg as LA
from django.utils.decorators import method_decorator
import core_main_app.utils.decorators as decorators
import core_explore_keyword_app.permissions.rights as rights
from django.urls import reverse_lazy, reverse



@decorators.permission_required(
    content_type=rights.EXPLORE_KEYWORD_CONTENT_TYPE,
    #content_type=rights.explore_keyword_content_type,
    permission=rights.EXPLORE_KEYWORD_ACCESS,
    #permission=rights.explore_keyword_access,
    #permission=None,
    login_url=reverse_lazy("core_main_app_login"),
    raise_exception=False,
)

def contact(request):
    form = ContactForm()
    result = False
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            print ('is valid')
            # result = "Jamura naach"
    return render(request, "jarvisff/ff.html", {"form": form,"result":result})
