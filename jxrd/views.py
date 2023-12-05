# from core_main_app.utils.rendering import render
from django.shortcuts import render
from .forms import ContactForm
from django.http import HttpResponse
from jarvis.io.vasp.inputs import Poscar

# from jarvis.ai.descriptors.cfid import CFID
import matplotlib.pyplot as plt

plt.switch_backend("agg")
import numpy as np
import os, io
import base64
#from jarvis.core.graphs import Graph
#from alignn.models.alignn import ALIGNN, ALIGNNConfig
#import torch
#from jarvis.core.kpoints import Kpoints3D as Kpoints
# import joblib, pickle
from numpy import linalg as LA
#from jarvis.core.kpoints import Kpoints3D
#from alignn.ff.ff import AlignnAtomwiseCalculator, default_path, ForceField
#from . import plot_phonons_ff  # plot_phonons_ff.import ase_phonon
#from ase import Atoms as AseAtoms
from matplotlib.gridspec import GridSpec


from django.utils.decorators import method_decorator
import core_main_app.utils.decorators as decorators
import core_explore_keyword_app.permissions.rights as rights
from django.urls import reverse_lazy, reverse
from jarvis.core.atoms import Atoms
from jarvis.analysis.diffraction.xrd import XRD

def xrd(
    atoms=None,
    wavelength=1.54184,
    thetas=[0, 180],
    scaling_factor=100,
    two_theta_tol=1e-5,
    intensity_tol=0.5,
    max_index=5,
):
    """Make Phonon calculation setup."""

    plt.rcParams.update({"font.size": 18})
    plt.figure(figsize=(10, 5))
    two_thetas, d_hkls, intensities = XRD().simulate(atoms=atoms)
    plt.bar(two_thetas,intensities)
    plt.xlabel('2$\theta$')
    plt.ylabel('Intensity')
    
    plt.tight_layout()
    img = io.BytesIO()
    plt.savefig(img)
    img.seek(0)
    plot_url_xrd = base64.b64encode(img.getvalue()).decode()
    plt.close()
    # print('freqs',freqs)
    # print('ds',ds)
    # print('tods',tdos.get_dos())
    # dosfig = phonon.plot_total_dos()
    # dosfig.savefig(phonopy_dos_figname)
    # dosfig.close()

    return plot_url_xrd
    #return phonon



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
    form = ContactForm(
        {
            "body": "FCC Al\n1.0\n4.06741 0.0 0.0\n0.0 4.06741 0.0\n0.0 0.0 4.06741\nAl\n4\ndirect\n0.0 0.0 0.0 \n0.0 0.5 0.5 \n0.5 0.0 0.5 \n0.5 0.5 0.0 \n",
        }
    )
    result = ""
    plot_url_xrd = False
    if request.method == "POST":
        #calc_phonon = AlignnAtomwiseCalculator(path=base_path, device=device)
        #calc_deafult = AlignnAtomwiseCalculator(path=def_path, device=device)
        try:
            form = ContactForm(request.POST)
            if form.is_valid():
                body = form.cleaned_data["body"]
                mat = Poscar.from_string(body).atoms

                if len(body) < 20000:
                    #plot_url = plot_phonons_ff.ase_phonon(atoms=opt)
                    plot_url_xrd = xrd(atoms=mat)



        except Exception as exp:
            print("Cannot run JARVIS-XRD.", exp)
            result = "Error:" + str(exp)
            pass
    return render(
        request,
        "jxrd/jxrd.html",
        {
            "form": form,
            "result": result,
            "plot_url_xrd": plot_url_xrd,
        },
    )
    # return render(request, "jalignnff/jalignnff.html", context={"form": form, "result": result})
