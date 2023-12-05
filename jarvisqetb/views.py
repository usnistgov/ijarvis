#from core_main_app.utils.rendering import render
from django.shortcuts import render
from .forms import ContactForm
from django.http import HttpResponse
from jarvis.io.vasp.inputs import Poscar
from jarvis.core.composition import Composition
from jarvis.ai.descriptors.cfid import CFID
import numpy as np
import os
import pickle
from django.utils.decorators import method_decorator
import core_main_app.utils.decorators as decorators
import core_explore_keyword_app.permissions.rights as rights
from django.urls import reverse_lazy, reverse
from numpy import linalg as LA
from jarvis.db.figshare import data


def get_chem_data(formula='Al2O3'):
    dat=data('dft_3d')
    print ('formula',formula)
    comp=Composition(formula)
    for i in dat:
        if i['formula']==formula:
            print (i['jid'])
    return i['jid']

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
    result = False #Turn to True if django form is needed/enabled
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            chem_form=str(form.cleaned_data["body"])
            print ('input',chem_form,type(chem_form))
            tmp_dat=get_chem_data(formula=chem_form)
            print ('dft is valid',tmp_dat)
            # result = "Jamura naach"
    return render(request, "jarvisqetb/qetb.html", {"form": form,"result":result})
