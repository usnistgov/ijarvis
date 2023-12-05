# from core_main_app.utils.rendering import render
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
import pandas as pd

# pd.options.html.border = 0
import django
import logging
import os
import sys
import json
import zipfile
from jarvis.db.jsonutils import loadjson, dumpjson

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mdcs.settings")
# sys.path.append(
#    os.path.join(os.path.realpath(os.path.dirname(__file__)), "..", "..")
# )
# django.setup()


base_path = os.path.join(os.path.dirname(__file__), "extras")

# dft3d_path = os.path.join(base_path, "jdft_3d-12-12-2022.json.zip")
# json_name = "jdft_3d-12-12-2022.json"
# dft3d = zipfile.ZipFile(dft3d_path).read(json_name).decode("utf-8")
# dft3d = json.loads(dft3d)

# dft2d_path = os.path.join(base_path, "d2-3-12-2021.json.zip")
# json_name = "d2-3-12-2021.json"
# dft2d = zipfile.ZipFile(dft2d_path).read(json_name).decode("utf-8")
# dft2d = json.loads(dft2d)
# print("formula", formula)
csv_path = os.path.join(base_path, "search.csv")
df = pd.read_csv(csv_path)


def get_chem_data(formula=None, search=None, jid=None):
    # dft3d = data("dft_3d")
    # dft2d = data("dft_2d")
    # base_path = os.path.join(os.path.dirname(__file__), "extras")

    # dft3d_path = os.path.join(base_path, "jdft_3d-12-12-2022.json.zip")
    # json_name = "jdft_3d-12-12-2022.json"
    # dft3d = zipfile.ZipFile(dft3d_path).read(json_name).decode("utf-8")
    # dft3d = json.loads(dft3d)

    # dft2d_path = os.path.join(base_path, "d2-3-12-2021.json.zip")
    # json_name = "d2-3-12-2021.json"
    # dft2d = zipfile.ZipFile(dft2d_path).read(json_name).decode("utf-8")
    # dft2d = json.loads(dft2d)
    # print("formula", formula)
    mem = []
    alias = {
        "formation_energy_peratom": "E_form",
        "optb88vdw_bandgap": "OPT_gap",
        "mbj_bandgap": "MBJ_gap",
        "magmom_oszicar": "mag",
        "bulk_modulus_kv": "Kv",
        "shear_modulus_gv": "Gv",
        "spg_number": "SpgNum",
        "spg_symbol": "Spg",
    }
    keys = [
        "jid",
        "formula",
        "spg_symbol",
        "spg_number",
        "crys",
        "func",
        "formation_energy_peratom",
        # "ehull",
        "optb88vdw_bandgap",
        "mbj_bandgap",
        "hse_gap",
        "bulk_modulus_kv",
        "shear_modulus_gv",
        "poisson",
        "spillage",
        "slme",
        "magmom_oszicar",
        "type",
    ]
    if search is not None:
        print(df)
        df1 = df[df["search"] == search]
        """
        for i in dft3d:
            if i["search"] == search:
                info = {}
                for j in keys:
                    if j in alias:

                        info[alias[j]] = i[j]
                    else:
                        info[j] = i[j]
                info["type"] = "3D"
                mem.append(info)
        for i in dft2d:
            if i["search"] == search:
                info = {}
                for j in keys:
                    if j in alias:

                        info[alias[j]] = i[j]
                    else:
                        info[j] = i[j]
                info["type"] = "2D"
                mem.append(info)
        """

    elif formula is not None:
        formula = Composition.from_string(formula).reduced_formula
        df1 = df[df["formula"] == formula]
        """
        for i in dft3d:
            if i["formula"] == formula:
                info = {}
                for j in keys:
                    if j in alias:

                        info[alias[j]] = i[j]
                    else:
                        info[j] = i[j]
                info["type"] = "3D"

                mem.append(info)
        for i in dft2d:
            if i["formula"] == formula:
                info = {}
                for j in keys:
                    if j in alias:

                        info[alias[j]] = i[j]
                    else:
                        info[j] = i[j]
                info["type"] = "2D"

                mem.append(info)
        """
    elif jid is not None:
        df1 = df[df["jid"] == jid]
        """
        for i in dft3d:
            if i["jid"] == jid:
                info = {}
                for j in keys:
                    if j in alias:

                        info[alias[j]] = i[j]
                    else:
                        info[j] = i[j]
                info["type"] = "3D"

                mem.append(info)
        for i in dft2d:
            if i["jid"] == jid:
                info = {}
                for j in keys:
                    if j in alias:

                        info[alias[j]] = i[j]
                    else:
                        info[j] = i[j]
                info["type"] = "2D"

                mem.append(info)
        """
    else:
        df1 = pd.DataFrame()
        # mem = []
    df1.pop('search')
    df1 = df1.rename(columns=alias)
    return df1
    # return mem


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
    result_table = ""  # Turn to True if django form is needed/enabled
    if request.method == "POST":
        try:
            form = ContactForm(request.POST)
            if form.is_valid():
                chem_form = str(form.cleaned_data["element_input"])
                print("input", chem_form, type(chem_form))
                if "-" in chem_form and "JVASP" not in chem_form:
                    sch = []
                    tmp = chem_form.split("-")
                    for ii in tmp:
                        if ii != "-":
                            sch.append(ii)
                    sch = "-".join(sorted(sch))
                    tmp_dat = get_chem_data(search=sch)
                elif "JVASP-" in chem_form:
                    tmp_dat = get_chem_data(jid=chem_form)

                else:
                    tmp_dat = get_chem_data(formula=chem_form)
                # df = pd.DataFrame(tmp_dat)
                df = tmp_dat.replace("na", "-")
                # df = df.replace("na", "-")
                df["jid"] = (
                    "<a href="
                    + "https://www.ctcms.nist.gov/~knc6/static/JARVIS-DFT/"
                    + df["jid"]
                    + ".xml"
                    + " target='_blank'>"
                    + df["jid"]
                    + "</a>"
                )
                result_table = df.to_html(
                    index=False,
                    table_id="table_res",
                    justify="left",
                    # classes="display",
                    # classes="table table-striped",
                    classes="table table-striped display compact",
                    header="true",
                    render_links="True",
                    escape=False,
                    # border = "0",
                )
                # print("dft is valid", pd.DataFrame(tmp_dat))
                # print("htm", result_table)
        except Exception as exp:
            print("Exp", exp)
            pass
    # result = "Jamura naach"
    return render(
        request,
        "jarvisdft/dft.html",
        {"form": form, "result_table": result_table},
    )
