# from core_main_app.utils.rendering import render
from django.shortcuts import render
from .forms import ContactForm, ContactForm2
from django.http import HttpResponse
from jarvis.io.vasp.inputs import Poscar
from jarvis.ai.descriptors.cfid import CFID
import numpy as np
import os, requests, io, tempfile
import pickle, zipfile, time
from jarvis.io.wannier.outputs import WannierHam
import base64
import matplotlib.pyplot as plt
from jarvis.analysis.interface.zur import (
    ZSLGenerator,
    mismatch_strts,
    get_hetero,
    get_hetero_type,
    make_interface,
)
from jarvis.core.atoms import Atoms

plt.switch_backend("agg")
from matplotlib.gridspec import GridSpec

from numpy import linalg as LA
from jarvis.io.vasp.inputs import Kpoints
from math import floor

# from jarvis.core.kpoints import Kpoints3D as Kpoints
from jarvis.db.jsonutils import loadjson
from jarvis.analysis.interface.zur import get_hetero_type

# opts=loadjson('options.json')
root_path = os.path.join(os.path.dirname(__file__))

jpath = os.path.join(os.path.dirname(__file__), "monolayer_data.json")


def band_alignment_diagram(vbms=[], cbms=[], labels=[]):
    img = io.BytesIO()
    x = np.arange(len(vbms)) + 0.5
    emin = floor(min(vbms)) - 1.0

    fig = plt.figure(figsize=(10, 8))

    plt.rcParams.update({"font.size": 22})
    plt.bar(x, np.array(vbms) - emin, bottom=emin, width=0.2)
    plt.bar(x, -np.array(cbms), bottom=cbms, width=0.2)
    plt.xlim(0, len(labels))
    plt.ylim(emin, 0)
    plt.xticks(x, labels)
    # plt.labels(labels, rotation=90)
    plt.axhline(y=-4.5, linestyle="-.")
    plt.axhline(y=-5.73, linestyle="-.")
    plt.text(1, -4, "${H^+}/{H_2}$")
    plt.text(1, -6.2, "${O_2}/{H_2O}$")
    # plt.title("2D: Positions of VBM and CBM")
    plt.ylabel("Energy relative to vacuum [eV]")
    plt.tight_layout()
    plt.savefig(img, format="png")
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    return plot_url  #'<img src="data:image/png;base64,{}">'.format(plot_url)


def get_hetero_type(A={}, B={}):
    stack = "na"
    int_type = "na"
    vbm_a1 = A["scf_vbm"] - A["avg_max"]
    vbm_b1 = B["scf_vbm"] - B["avg_max"]
    cbm_a1 = A["scf_cbm"] - A["avg_max"]
    cbm_b1 = B["scf_cbm"] - B["avg_max"]
    try:
        # if A['phi']>B['phi']:
        if A["scf_vbm"] - A["avg_max"] < B["scf_vbm"] - B["avg_max"]:
            stack = "BA"
            print("NOT-SWAPPED")
        else:
            C = A
            D = B
            A = D
            B = C
            stack = "AB"
            print("SWAPPED")
            # tmp=B
            # B=A
            # A=tmp
        vbm_a = A["scf_vbm"] - A["avg_max"]
        vbm_b = B["scf_vbm"] - B["avg_max"]
        cbm_a = A["scf_cbm"] - A["avg_max"]
        cbm_b = B["scf_cbm"] - B["avg_max"]
        #  print ('vbm_a,vbm_b,cbm_b,cbm_a',vbm_a,vbm_b,cbm_b,cbm_a)
        if vbm_a < vbm_b and vbm_b < cbm_b and cbm_b < cbm_a:
            int_type = "I"
        elif vbm_a < vbm_b and vbm_b < cbm_a and cbm_a < cbm_b:
            int_type = "II"
        elif vbm_a < cbm_a and cbm_a < vbm_b and vbm_b < cbm_b:
            int_type = "III"
    except:
        pass
    return int_type, stack, vbm_a1, vbm_b1, cbm_a1, cbm_b1

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
    form2 = ContactForm2()
    plot_url = False
    result = ""
    mat1 = ""
    mat2 = ""
    film = False
    subs = False
    comb = False
    comb_xyz = False
    film_2 = ""
    subs_2 = ""
    comb_2 = False
    int_type=''
    stack=''
    vbm_a=0
    vbm_b=0
    cbm_a=0
    cbm_b=0
    mism_u=0
    mism_v=0
    mism_angle=0

    mism_u_2=0
    mism_v_2=0
    mism_angle_2=0

    label1=''
    label2=''
    if request.method == "POST":
        try:
            # form2 = ContactForm2(request.POST)
            if "Submit" in request.POST:
                form = ContactForm(request.POST)
                if form.is_valid() and "Submit":
                    # print ('Submitting')
                    mat1 = form.cleaned_data["category1"]
                    mat2 = form.cleaned_data["category2"]
                    if mat1 is not None and mat2 is not None:
                        # print("mat1", mat1)
                        # print("mat2", mat2)
                        d = loadjson(jpath)
                        formula1 = mat1.split("{")[0]
                        spg1 = mat1.split("{")[1].split("}")[0]
                        jid1 = mat1.split("[")[1].split("]")[0]
                        formula2 = mat2.split("{")[0]
                        spg2 = mat2.split("{")[1].split("}")[0]
                        jid2 = mat2.split("[")[1].split("]")[0]

                        mat1_url = (
                            str(formula1) + str("{") + str(spg1) + str("}")
                        )

                        mat2_url = (
                            str(formula2) + str("{") + str(spg2) + str("}")
                        )

                        for i in d:
                            if i["jid"] == jid1:
                                strt1 = Atoms.from_dict(i["atoms"])
                                phiA = i["phi"]
                                break
                        for i in d:
                            if i["jid"] == jid2:
                                strt2 = Atoms.from_dict(i["atoms"])
                                phiB = i["phi"]
                                break
                        if strt1 != None and strt2 != None:
                            (
                                int_type,
                                stack,
                                vbm_a,
                                vbm_b,
                                cbm_a,
                                cbm_b,
                            ) = get_hetero_type(A=phiA, B=phiB)
                            vbms = [vbm_b, vbm_a]
                            cbms = [cbm_b, cbm_a]

                            labels = [
                                strt2.composition.reduced_formula,
                                strt1.composition.reduced_formula,
                            ]
                            label2=strt2.composition.reduced_formula+str("(")+str(jid2)+str(")")
                            label1=strt1.composition.reduced_formula+str("(")+str(jid1)+str(")")
                            plot_url = band_alignment_diagram(
                                vbms=vbms, cbms=cbms, labels=labels
                            )

                            film = strt1
                            subs = strt2

                            info_mis = make_interface(film=film, subs=subs)

                            mism_u = round(abs(info_mis["mismatch_u"]), 3)
                            mism_v = round(abs(info_mis["mismatch_v"]), 3)
                            mism_angle = round(
                                abs(info_mis["mismatch_angle"]), 3
                            )

                            try:
                                comb = ""
                                film = ""
                                subs = ""
                                film = "\n" + (strt1).get_string()
                                subs = "\n" + (strt2).get_string()

                                combined = info_mis[
                                    "interface"
                                ].center_around_origin()
                                comb = (combined).get_string()
                                # print ('comb',comb)
                                comb_xyz = combined.get_xyz_string.replace(
                                    "\n", "\\n"
                                )
                                # print ('combxyz',comb_xyz)

                                film = (
                                    "Original film:\n"
                                    + film
                                    + "\nTransformed structure:\n"
                                    + ((info_mis["film_sl"]))
                                    .center_around_origin()
                                    .get_string()
                                )
                                subs = (
                                    "Original substrate:\n"
                                    + subs
                                    + "\nTransformed structure:\n"
                                    + ((info_mis["subs_sl"]))
                                    .center_around_origin()
                                    .get_string()
                                )
                            except:
                                pass
            if "Send" in request.POST:
                form2 = ContactForm2(request.POST)
                if form2.is_valid():
                    # combined_2  = get_hetero(center_around_origin(info_mis_2['subs_sl']),center_around_origin(info_mis_2['film_sl']))
                    # print ('combined_2',combined_2)
                    try:

                        mat1 = form2.cleaned_data["mat1"]
                        mat2 = form2.cleaned_data["mat2"]

                        # print ('request.form',request.form)
                        # entry1 = request.form["message1"]
                        subs_2 = Poscar.from_string(mat1).atoms
                        # entry2 = request.form["message2"]
                        film_2 = Poscar.from_string(mat2).atoms
                        # info_mis_2=mismatch_strts(film=film_2,subs=subs_2)
                        info_mis_2 = make_interface(film=film_2, subs=subs_2)

                        label1=subs_2.composition.reduced_formula
                        label2=film_2.composition.reduced_formula

                        mism_u_2 = round(abs(info_mis_2["mismatch_u"]), 3)
                        mism_v_2 = round(abs(info_mis_2["mismatch_v"]), 3)
                        mism_angle_2 = round(
                            abs(info_mis_2["mismatch_angle"]), 3
                        )
                        combined_2 = info_mis_2[
                            "interface"
                        ].center_around_origin()

                        comb_2 = (combined_2).get_string()

                        film_2 = (
                            "Original film:\n"
                            + entry2
                            + "\nTransformed structure:\n"
                            + ((info_mis_2["film_sl"]))
                            .center_around_origin()
                            .get_string()
                        )
                        subs_2 = (
                            "Original substrate:\n"
                            + entry1
                            + "\nTransformed structure:\n"
                            + ((info_mis_2["subs_sl"]))
                            .center_around_origin()
                            .get_string()
                        )
                    except Exception:
                        pass
                    form2.mat1 = "NA"  # film_2
                    form2.mat2 = "NA"  # subs2_2
                    # form2.save()
                # result = "Jamura naach"
        # print ('comb_xyz',comb_xyz)
        except Exception:
            print("Error running the app.")
            pass
    return render(
        request,
        "jarvish/hetero.html",
        {
            "form": form,
            "form2": form2,
            "plot_url": plot_url,
            "film": film,
            "subs": subs,
            "comb": comb,
            "comb_xyz": comb_xyz,
            "film_2": film_2,
            "subs_2": subs_2,
            "comb_2": comb_2,
            "int_type":int_type,
            "stack":stack,
            "vbm_a":round(vbm_a,3),
            "vbm_b":round(vbm_b,3),
            "cbm_a":round(cbm_a,3),
            "cbm_b":round(cbm_b,3),
            "mism_u":round(mism_u,3),
            "mism_v":round(mism_v,3),
            "mism_angle":round(mism_angle,3),
            "mism_u_2":round(mism_u_2,3),
            "mism_v_2":round(mism_v_2,3),
            "mism_angle_2":round(mism_angle_2,3),
            "label1":label1,
            "label2":label2,
        },
    )
