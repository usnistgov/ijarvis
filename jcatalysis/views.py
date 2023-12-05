# from core_main_app.utils.rendering import render
from django.shortcuts import render
from .forms import ContactForm
from django.http import HttpResponse
from jarvis.io.vasp.inputs import Poscar

# from jarvis.ai.descriptors.cfid import CFID
import numpy as np
import os
from jarvis.core.graphs import Graph
from alignn.models.alignn import ALIGNN, ALIGNNConfig
import torch

# import joblib, pickle
from numpy import linalg as LA
from jarvis.core.kpoints import Kpoints3D
from alignn.ff.ff import AlignnAtomwiseCalculator, default_path, wt01_path
from jarvis.analysis.thermodynamics.energetics import get_optb88vdw_energy

mu = get_optb88vdw_energy()
device = "cpu"
# if torch.cuda.is_available():
#        device = torch.device("cuda")


base_path = os.path.join(os.path.dirname(__file__), "extras")

fen_path = os.path.join(base_path, "checkpoint_45.pt")
model = ALIGNN(ALIGNNConfig(name="alignn", alignn_layers=2))
model.load_state_dict(torch.load(fen_path, map_location=device)["model"])
model.to(device)
model.eval()
ocp_energy = {"H": -3.477, "O": -7.204, "C": -7.282, "N": -8.083}
model_path =  os.path.join(os.path.dirname(__file__),"extras", "alignnff_wt01") #wt01_path()
calculator = AlignnAtomwiseCalculator(path=model_path, stress_wt=0.3)


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
    substrate = ""
    catalyst = ""
    result = False
    form = ContactForm()
    if request.method == "POST":
        # ocp all model
        """
        fen_path = os.path.join(base_path, "checkpoint_45.pt")
        model = ALIGNN(ALIGNNConfig(name="alignn", alignn_layers=2))
        model.load_state_dict(
            torch.load(fen_path, map_location=device)["model"]
        )
        model.to(device)
        model.eval()
        ocp_energy = {"H": -3.477, "O": -7.204, "C": -7.282, "N": -8.083}
        model_path = wt01_path()
        calculator = AlignnAtomwiseCalculator(path=model_path, stress_wt=0.3)
        """

        def atoms_to_energy(atoms):
            num_atoms = atoms.num_atoms
            atoms = atoms.ase_converter()
            atoms.calc = calculator
            forces = atoms.get_forces()
            energy = atoms.get_potential_energy()
            stress = atoms.get_stress()
            return energy  # ,forces,stress

        try:
            form = ContactForm(request.POST)
            if form.is_valid():
                substrate = form.cleaned_data["substrate"]
                catalyst = form.cleaned_data["catalyst"]
                mat_subs = Poscar.from_string(substrate).atoms
                mat_cat_pos = Poscar.from_string(catalyst)
                comment=mat_cat_pos.comment
                mat_cat = mat_cat_pos.atoms
                print('comment',comment)
                adsorbate_indices = []
                mol_elements=[]
                elements=mat_cat.elements
                for i in comment.split('adsorbate_indices:')[1].split('[')[1].split(']')[0].split(','):
                    if i!='':
                          ind=int(i)-1
                          adsorbate_indices.append(ind)
                          mol_elements.append(elements[ind])
                           
                print('adsorbate_indices',adsorbate_indices)

                if len(catalyst) < 20000:
                    en_subs = atoms_to_energy(mat_subs)
                    en_cat = atoms_to_energy(mat_cat)
                    els_subs = mat_subs.elements
                    els_cat = mat_cat.elements

                    #mol_elements = []  # list(set(els_cat)-set(els_subs))
                    #for i in els_cat:
                    #    if i not in els_subs:
                    #        mol_elements.append(i)
                    chem_pot = 0
                    if mol_elements:
                        for i in mol_elements:
                            chem_pot += mu[i]["energy"]

                    en_cat = round(float(en_cat), 4)
                    en_subs = round(float(en_subs), 4)
                    chem_pot = round(float(chem_pot), 4)
                    ads_en = en_cat - en_subs + chem_pot
                    ads_en = round(float(ads_en), 4)
                    chem_pot_aff = chem_pot

                    # ocp
                    g, lg = Graph.atom_dgl_multigraph(mat_subs)
                    en_subs_2 = (
                        model([g.to(device), lg.to(device)])
                        .detach()
                        .cpu()
                        .numpy()
                        .flatten()
                        .tolist()[0]
                    )

                    g, lg = Graph.atom_dgl_multigraph(mat_cat)
                    en_cat_2 = (
                        model([g.to(device), lg.to(device)])
                        .detach()
                        .cpu()
                        .numpy()
                        .flatten()
                        .tolist()[0]
                    )
                    chem_pot = 0
                    mu_in_ocp = True
                    if mol_elements:
                        for i in mol_elements:
                            if i in ocp_energy:
                                chem_pot += ocp_energy[i]
                            else:
                                mu_in_ocp = False
                    if mu_in_ocp:
                        ads_en2 = en_cat_2 - en_subs_2 + chem_pot
                        ads_en2 = round(float(ads_en2), 4)
                    else:
                        ads_en2 = "na"
                    result = (
                        "Adsorption energy ALIGNN-FF model(eV): "
                        + "\n"
                        + str(ads_en)
                        + "\n"
                        "Substrate energy (eV): " + str(en_subs) + "\n"
                        "Catalyst energy (eV): " + str(en_cat) + "\n"
                        "Chemical potential (eV): " + str(chem_pot_aff) + "\n"
                        "Adsorption energy ocp_all model (eV): "
                        + "\n"
                        + str(ads_en2)
                        + "\n"
                        + "\n\nInput"
                        + str("\n" + catalyst)
                        + "\n"
                    )

        except Exception as exp:
            print("Cannot run JARVIS-ALIGNN.", exp)
            pass
    return render(
        request, "jcatalysis/catalysis.html", {"form": form, "result": result}
    )
    # return render(request, "jarvisml/jarvisml.html", context={"form": form, "result": result})
