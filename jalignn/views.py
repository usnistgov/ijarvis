# from core_main_app.utils.rendering import render
from django.shortcuts import render
from .forms import ContactForm
from django.http import HttpResponse
from jarvis.io.vasp.inputs import Poscar

# from jarvis.ai.descriptors.cfid import CFID
import numpy as np
import os
from jarvis.core.graphs import Graph
from alignn.models.alignn import ALIGNN
import torch

# import joblib, pickle
from numpy import linalg as LA
from jarvis.core.kpoints import Kpoints3D

device = "cpu"
# if torch.cuda.is_available():
#        device = torch.device("cuda")


base_path = os.path.join(os.path.dirname(__file__), "extras")
#"""
fen_path = os.path.join(base_path, "JV15_55k_form_enp.pt")

form_file = ALIGNN()
form_file.load_state_dict(torch.load(fen_path, map_location=device)["model"])
form_file.to(device)
form_file.eval()

bg_path = os.path.join(base_path, "JV15_55k_optgap.pt")
bg_file = ALIGNN()
bg_file.load_state_dict(torch.load(bg_path, map_location=device)["model"])
bg_file.to(device)
bg_file.eval()


eng_path = os.path.join(base_path, "JV15_55k_total_energy.pt")
eng_file = ALIGNN()
eng_file.load_state_dict(torch.load(eng_path, map_location=device)["model"])
eng_file.to(device)
eng_file.eval()
#"""

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
    form = ContactForm(
        {
            "body": "Mo1 Se2\n1.0\n1.661759 -2.878250 0.000000\n1.661759 2.878250 0.000000\n0.000000 0.000000 35.451423\nMo Se\n1 2\ndirect\n0.666667 0.333333 0.326886 Mo\n0.333333 0.666667 0.374080 Se\n0.333333 0.666667 0.279691 Se"
        }
    )
    result = ""
    if request.method == "POST":
        """
        fen_path = os.path.join(base_path, "JV15_55k_form_enp.pt")

        form_file = ALIGNN()
        form_file.load_state_dict(
            torch.load(fen_path, map_location=device)["model"]
        )
        form_file.to(device)
        form_file.eval()

        bg_path = os.path.join(base_path, "JV15_55k_optgap.pt")
        bg_file = ALIGNN()
        bg_file.load_state_dict(
            torch.load(bg_path, map_location=device)["model"]
        )
        bg_file.to(device)
        bg_file.eval()

        eng_path = os.path.join(base_path, "JV15_55k_total_energy.pt")
        eng_file = ALIGNN()
        eng_file.load_state_dict(
            torch.load(eng_path, map_location=device)["model"]
        )
        eng_file.to(device)
        eng_file.eval()
        """
        try:
            form = ContactForm(request.POST)
            if form.is_valid():
                body = form.cleaned_data["body"]
                mat = Poscar.from_string(body).atoms

                if len(body) < 20000:
                    g, lg = Graph.atom_dgl_multigraph(mat)
                    f_en = (
                        form_file([g.to(device), lg.to(device)])
                        .detach()
                        .cpu()
                        .numpy()
                        .flatten()
                        .tolist()[0]
                    )
                    f_en = round(float(f_en), 3)

                    bg = (
                        bg_file([g.to(device), lg.to(device)])
                        .detach()
                        .cpu()
                        .numpy()
                        .flatten()
                        .tolist()[0]
                    )
                    bg = round(float(bg), 3)
                    if bg < 0:
                        bg = 0
                    eng = (
                        eng_file([g.to(device), lg.to(device)])
                        .detach()
                        .cpu()
                        .numpy()
                        .flatten()
                        .tolist()[0]
                    )
                    eng = round(float(eng), 3)
                    result = (
                        "Formation energy/atom (eV):"
                        + str(f_en)
                        + "\nBandgap OptB88vdW (eV): "
                        + str(bg)
                        + "\nEnergy/atom (eV): "
                        + str(eng)
                        + "\n\n input"
                        + str("\n" + body)
                        + "\n"
                    )

        except Exception as exp:
            print("Cannot run JARVIS-ALIGNN.", exp)
            pass
    return render(
        request, "jalignn/alignn.html", {"form": form, "result": result}
    )
    # return render(request, "jarvisml/jarvisml.html", context={"form": form, "result": result})
