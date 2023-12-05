# from core_main_app.utils.rendering import render
from django.shortcuts import render
from .forms import ContactForm
from django.http import HttpResponse
from jarvis.io.vasp.inputs import Poscar

# from jarvis.ai.descriptors.cfid import CFID
import matplotlib.pyplot as plt

plt.switch_backend("agg")
import numpy as np
import os, io, json
import base64
from jarvis.core.graphs import Graph
from alignn.models.alignn import ALIGNN, ALIGNNConfig
import torch

# import joblib, pickle
from numpy import linalg as LA
from jarvis.core.kpoints import Kpoints3D
from alignn.ff.ff import AlignnAtomwiseCalculator, default_path, ForceField
from .stemconv import STEMConv
import sys
import argparse
from jarvis.core.atoms import Atoms
import matplotlib.pyplot as plt
from jarvis.analysis.defects.surface import Surface

# device = "cpu"
# if torch.cuda.is_available():
#        device = torch.device("cuda")


from django.utils.decorators import method_decorator
import core_main_app.utils.decorators as decorators
import core_explore_keyword_app.permissions.rights as rights
from django.urls import reverse_lazy, reverse


def make_image(
    atoms=[],
    output_size="",
    power_factor="",
    px_scale="",
    surface_layers="",
    miller_index="",
):
    # file_format = str(args.file_format)

    miller_index = [int(i) for i in (miller_index).split("_")]
    # if file_format == "poscar":
    #    atoms = Atoms.from_poscar(file_path)
    # elif file_format == "cif":
    #    atoms = Atoms.from_cif(file_path)
    # elif file_format == "xyz":
    #    # Note using 500 angstrom as box size
    #    atoms = Atoms.from_xyz(file_path, box_size=500)
    # elif file_format == "pdb":
    #    # Note using 500 angstrom as box size
    #    # Recommended install pytraj
    #    # conda install -c ambermd pytraj
    #    atoms = Atoms.from_pdb(file_path, max_lat=500)
    # else:
    #    raise NotImplementedError("File format not implemented", file_format)
    img = io.BytesIO()
    surface = Surface(
        atoms=atoms, indices=miller_index, layers=surface_layers
    ).make_surface()
    out = STEMConv(
        output_size=[output_size, output_size], power_factor=power_factor
    ).simulate_surface(surface, px_scale=px_scale)

    plt.imshow(out[0], cmap="gray")
    plt.xticks([])
    plt.yticks([])
    plt.savefig(img)
    plt.close()

    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    return plot_url


# "body": "{'output':256,'n_layers':1,'power_factor':1.7,miller':'0_0_1'}\n1.0\n1.2320971008984494 -2.1340542301747005 0.0\n1.2320971008984494 2.1340542301747005 0.0\n0.0 0.0 30.803073\nC\n2\ndirect\n0.0 0.0 0.0633300000000006 \n0.3333330000000032 0.6666669999999968 0.0633300000000006 \n",
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
            "body": '{"output":256,"scale":0.2,"layers":1,"power":1.7,"miller":"0_0_1"}\n1.0\n1.2320971008984494 -2.1340542301747005 0.0\n1.2320971008984494 2.1340542301747005 0.0\n0.0 0.0 30.803073\nC\n2\ndirect\n0.0 0.0 0.0633300000000006 \n0.3333330000000032 0.6666669999999968 0.0633300000000006 \n',
        }
    )
    result = ""
    plot_url_stem = False
    # plot_url2 = False
    if request.method == "POST":
     try:
        form = ContactForm(request.POST)
        if form.is_valid():
            body = form.cleaned_data["body"]
            pos = Poscar.from_string(body)
            comment = pos.comment
            info = json.loads(comment)
            print("info", info)

            atoms = pos.atoms
            print("atoms", atoms)
            if len(body) < 20000:
                plot_url_stem = make_image(
                    atoms=atoms,
                    output_size=info["output"],
                    power_factor=info["power"],
                    px_scale=info["scale"],
                    surface_layers=info["layers"],
                    miller_index=info["miller"],
                )

     except Exception as exp:
        print("Cannot run JARVIS-ALIGNN.",exp)
        pass
    return render(
        request,
        "jstem/jstem.html",
        {"form": form, "result": result, "plot_url_stem": plot_url_stem},
    )
    # return render(request, "jalignnff/jalignnff.html", context={"form": form, "result": result})
