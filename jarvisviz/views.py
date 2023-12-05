# from core_main_app.utils.rendering import render
from django.shortcuts import render
from .forms import ContactForm1,ContactForm2,ContactForm3,ContactForm4
from django.http import HttpResponse
from jarvis.io.vasp.inputs import Poscar
from jarvis.ai.descriptors.cfid import CFID
import numpy as np
import os
import joblib, pickle
from numpy import linalg as LA
from jarvis.core.kpoints import Kpoints3D
import tempfile
from jarvis.core.atoms import Atoms
#from jarvis.core.pdb_atoms import read_pdb
from django.utils.decorators import method_decorator
import core_main_app.utils.decorators as decorators
import core_explore_keyword_app.permissions.rights as rights
from django.urls import reverse_lazy, reverse


f=open( os.path.join(os.path.dirname(__file__), "POSCAR"),'r')
poscar_example=f.read()
f.close()

f=open( os.path.join(os.path.dirname(__file__), "POSCAR.xyz"),'r')
xyz_example=f.read()
f.close()

f=open( os.path.join(os.path.dirname(__file__), "POSCAR.cif"),'r')
cif_example=f.read()
f.close()

f=open( os.path.join(os.path.dirname(__file__), "pdb101d.ent"),'r')
pdb_example=f.read()
f.close()


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
    form1 = ContactForm1({"body":poscar_example})
    form2 = ContactForm2({"body":xyz_example})
    form3 = ContactForm3({"body":cif_example})
    form4 = ContactForm4({"body":pdb_example})

    result = ""
    xyz = ""
    cif = ""
    pos = ""
    if request.method == "POST":

        form1 = ContactForm1(request.POST)
        form2 = ContactForm2(request.POST)
        form3 = ContactForm3(request.POST)
        form4 = ContactForm4(request.POST)
        try:
            if form1.is_valid() and "poscar" in request.POST:
                body = form1.cleaned_data["body"]
                mat = Poscar.from_string(body).atoms
                xyz="'"+str(mat.get_xyz_string)+"'"
                form2 = ContactForm2({"body":xyz_example})
                form3 = ContactForm3({"body":cif_example})
                form4 = ContactForm4({"body":pdb_example})
            elif form2.is_valid() and "xyz" in request.POST:
                body = form2.cleaned_data["body"]
                new_file, filename = tempfile.mkstemp()
                body = form2.cleaned_data["body"]
                f=open(filename,'w')
                f.write(body)
                f.close()
                p=Atoms.from_xyz(filename)
                xyz="'"+str(p.get_xyz_string)+"'"
                form1 = ContactForm1({"body":poscar_example})
                form3 = ContactForm3({"body":cif_example})
                form4 = ContactForm4({"body":pdb_example})
            elif form3.is_valid() and "cif" in request.POST:
                new_file, filename = tempfile.mkstemp()
                body = form3.cleaned_data["body"]
                f=open(filename,'w')
                f.write(body)
                f.close()
                p=Atoms.from_cif(filename)
                xyz="'"+str(p.get_xyz_string)+"'"
                form1 = ContactForm2({"body":poscar_example})
                form2 = ContactForm3({"body":xyz_example})
                form4 = ContactForm4({"body":pdb_example})
            elif form4.is_valid() and "pdb" in request.POST:
                new_file, filename = tempfile.mkstemp()
                body = form4.cleaned_data["body"]
                f=open(filename,'w')
                f.write(body)
                f.close()
                p=Atoms.from_pdb(filename)
                #p=read_pdb(filename)
                xyz="'"+str(p.get_xyz_string)+"'"
                form1 = ContactForm2({"body":poscar_example})
                form2 = ContactForm3({"body":xyz_example})
                form3 = ContactForm4({"body":cif_example})
            else:
                print ('IDK')
        except Exception as exp:
            print("Cannot run JARVISML.",exp)
            pass
    return render(
            request, "jarvisviz/jarvisviz.html", {"form1": form1,"form2":form2,"form3":form3,"form4":form4, "xyz":xyz.replace('\n','\\n'), "result": result}
    )
    # return render(request, "jarvisml/jarvisml.html", context={"form": form, "result": result})
