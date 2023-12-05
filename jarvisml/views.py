# from core_main_app.utils.rendering import render
from django.urls import reverse_lazy, reverse
import core_explore_keyword_app.permissions.rights as rights
import core_main_app.utils.decorators as decorators
from django.utils.decorators import method_decorator
from django.shortcuts import render
from .forms import ContactForm
from django.http import HttpResponse
from jarvis.io.vasp.inputs import Poscar
from jarvis.ai.descriptors.cfid import CFID
import numpy as np
import os
import joblib
import pickle
from numpy import linalg as LA
from jarvis.core.kpoints import Kpoints3D

base_path = os.path.join(os.path.dirname(__file__), "extras")
#"""
fen_path = os.path.join(base_path, "formation_energy_peratom.pkl")
form_file = joblib.load(
    open(fen_path, "rb"),
)


bg_path = os.path.join(base_path, "optb88vdw_bandgap.pkl")
bg_file = joblib.load(
    open(bg_path, "rb"),
)


mbj_path = os.path.join(base_path, "mbj_bandgap.pkl")
mbj_file = joblib.load(
    open(mbj_path, "rb"),
)

kv_path = os.path.join(base_path, "bulk_modulus_kv.pkl")
kv_file = joblib.load(
    open(kv_path, "rb"),
)


gv_path = os.path.join(base_path, "shear_modulus_gv.pkl")
gv_file = joblib.load(
    open(gv_path, "rb"),
)


kp_path = os.path.join(base_path, "kpoint_length_unit.pkl")
kp_file = joblib.load(
    open(kp_path, "rb"),
)

enc_path = os.path.join(base_path, "encut.pkl")
enc_file = joblib.load(
    open(enc_path, "rb"),
)

epsx_path = os.path.join(base_path, "epsx.pkl")
epsx_file = joblib.load(
    open(epsx_path, "rb"),
)

epsy_path = os.path.join(base_path, "epsy.pkl")
epsy_file = joblib.load(
    open(epsy_path, "rb"),
)

epsz_path = os.path.join(base_path, "epsz.pkl")
epsz_file = joblib.load(
    open(epsz_path, "rb"),
)


mepsx_path = os.path.join(base_path, "mepsx.pkl")
mepsx_file = joblib.load(
    open(mepsx_path, "rb"),
)

mepsy_path = os.path.join(base_path, "mepsy.pkl")
mepsy_file = joblib.load(
    open(mepsy_path, "rb"),
)

mepsz_path = os.path.join(base_path, "mepsz.pkl")
mepsz_file = joblib.load(
    open(mepsz_path, "rb"),
)
#"""


"""
p="Mo1 Se2\n1.0\n1.661759 -2.878250 0.000000\n1.661759 2.878250 0.000000\n0.000000 0.000000 35.451423\nMo Se\n1 2\ndirect\n0.666667 0.333333 0.326886 Mo\n0.333333 0.666667 0.374080 Se\n0.333333 0.666667 0.279691 Se"
mat=Poscar.from_string(p).atoms
ent_X = np.array([CFID(mat).get_comp_descp()])
print ('ent_X ',ent_X )
f_en = round(float(form_file.predict(ent_X)[0]), 3)
print ('fen',f_en)
f_en = round(float(bg_file.predict(ent_X)[0]), 3)
print ('fen',f_en)
"""


#@decorators.permission_required(
#    content_type=rights.explore_keyword_content_type,
#    permission=rights.explore_keyword_access,
#    login_url=reverse_lazy("core_main_app_login"),
#    raise_exception=False,
#)
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
        fen_path = os.path.join(base_path, "formation_energy_peratom.pkl")
        form_file = joblib.load(
            open(fen_path, "rb"),
        )

        bg_path = os.path.join(base_path, "optb88vdw_bandgap.pkl")
        bg_file = joblib.load(
            open(bg_path, "rb"),
        )

        mbj_path = os.path.join(base_path, "mbj_bandgap.pkl")
        mbj_file = joblib.load(
            open(mbj_path, "rb"),
        )

        kv_path = os.path.join(base_path, "bulk_modulus_kv.pkl")
        kv_file = joblib.load(
            open(kv_path, "rb"),
        )

        gv_path = os.path.join(base_path, "shear_modulus_gv.pkl")
        gv_file = joblib.load(
            open(gv_path, "rb"),
        )

        kp_path = os.path.join(base_path, "kpoint_length_unit.pkl")
        kp_file = joblib.load(
            open(kp_path, "rb"),
        )

        enc_path = os.path.join(base_path, "encut.pkl")
        enc_file = joblib.load(
            open(enc_path, "rb"),
        )

        epsx_path = os.path.join(base_path, "epsx.pkl")
        epsx_file = joblib.load(
            open(epsx_path, "rb"),
        )

        epsy_path = os.path.join(base_path, "epsy.pkl")
        epsy_file = joblib.load(
            open(epsy_path, "rb"),
        )

        epsz_path = os.path.join(base_path, "epsz.pkl")
        epsz_file = joblib.load(
            open(epsz_path, "rb"),
        )

        mepsx_path = os.path.join(base_path, "mepsx.pkl")
        mepsx_file = joblib.load(
            open(mepsx_path, "rb"),
        )

        mepsy_path = os.path.join(base_path, "mepsy.pkl")
        mepsy_file = joblib.load(
            open(mepsy_path, "rb"),
        )

        mepsz_path = os.path.join(base_path, "mepsz.pkl")
        mepsz_file = joblib.load(
            open(mepsz_path, "rb"),
        )
        """
        try:
            form = ContactForm(request.POST)
            if form.is_valid():
                body = form.cleaned_data["body"]
                mat = Poscar.from_string(body).atoms

                if len(body) < 20000:
                    ent_X = np.array([CFID(mat).get_comp_descp()])
                    # print ('ent_X',ent_X)
                    f_en = round(float(form_file.predict(ent_X)[0]), 3)
                    bg = round(float(bg_file.predict(ent_X)[0]), 2)
                    length = round(float(kp_file.predict(ent_X)[0]), 2)
                    kp = (
                        Kpoints3D()
                        .automatic_length_mesh(
                            lattice_mat=mat.lattice_mat, length=length
                        )
                        .kpts
                    )
                    kpoint = (
                        str(kp[0][0])
                        + str("x")
                        + str(kp[0][1])
                        + str("x")
                        + str(kp[0][2])
                    )

                    encut = max(
                        round(float(enc_file.predict(ent_X)[0]), 2), 500.0
                    )

                    slme_pred = "NA"
                    slme_path = str("{0}/pickle2-slme.pk".format(base_path))
                    slme_file = pickle.load(
                        open(slme_path, "rb"), encoding="latin1"
                    )
                    slme_true = slme_file.predict(ent_X)[0][0]
                    if slme_true == 1:
                        slme_pred = "True"
                    else:
                        slme_pred = "False"

                    nzt_pred = "NA"
                    nzt_path = str("{0}/pickle2-n-ZT.pk".format(base_path))
                    nzt_file = pickle.load(
                        open(nzt_path, "rb"), encoding="latin1"
                    )
                    nzt_true = nzt_file.predict(ent_X)[0][0]
                    if nzt_true == 1:
                        nzt_pred = "True"
                    else:
                        nzt_pred = "False"

                    pzt_pred = "NA"
                    pzt_path = str("{0}/pickle2-p-ZT.pk".format(base_path))
                    pzt_file = pickle.load(
                        open(pzt_path, "rb"), encoding="latin1"
                    )
                    pzt_true = pzt_file.predict(ent_X)[0][0]
                    if pzt_true == 1:
                        pzt_pred = "True"
                    else:
                        pzt_pred = "False"

                    nseeb_pred = "NA"
                    nseeb_path = str(
                        "{0}/pickle2-n-Seebeck.pk".format(base_path)
                    )
                    nseeb_file = pickle.load(
                        open(nseeb_path, "rb"), encoding="latin1"
                    )
                    nseeb_true = nseeb_file.predict(ent_X)[0][0]
                    if nseeb_true == 1:
                        nseeb_pred = "True"
                    else:
                        nseeb_pred = "False"

                    pseeb_pred = "NA"
                    pseeb_path = str(
                        "{0}/pickle2-p-Seebeck.pk".format(base_path)
                    )
                    pseeb_file = pickle.load(
                        open(pseeb_path, "rb"), encoding="latin1"
                    )
                    pseeb_true = pseeb_file.predict(ent_X)[0][0]
                    if pseeb_true == 1:
                        pseeb_pred = "True"
                    else:
                        pseeb_pred = "False"

                    npf_pred = "NA"
                    npf_path = str(
                        "{0}/pickle2-n-powerfact.pk".format(base_path)
                    )
                    npf_file = pickle.load(
                        open(npf_path, "rb"), encoding="latin1"
                    )
                    npf_true = npf_file.predict(ent_X)[0][0]
                    if npf_true == 1:
                        npf_pred = "True"
                    else:
                        npf_pred = "False"

                    ppf_pred = "NA"
                    ppf_path = str(
                        "{0}/pickle2-p-powerfact.pk".format(base_path)
                    )
                    ppf_file = pickle.load(
                        open(ppf_path, "rb"), encoding="latin1"
                    )
                    ppf_true = ppf_file.predict(ent_X)[0][0]
                    if ppf_true == 1:
                        ppf_pred = "True"
                    else:
                        ppf_pred = "False"

                    if bg < 0.0:
                        bg = 0.0
                    mbj = round(float(mbj_file.predict(ent_X)[0]), 2)
                    if mbj < 0.0:
                        mbj = 0.0
                    kv = round(float(kv_file.predict(ent_X)[0]), 2)
                    if kv < 0.0:
                        kv = 0.0
                    gv = round(float(gv_file.predict(ent_X)[0]), 2)
                    ex = "NA for metals"
                    ey = "NA for metals"
                    ez = "NA for metals"
                    mex = "NA for metals"
                    mey = "NA for metals"
                    mez = "NA for metals"
                    if bg > 0.1:

                        ex = round(float(epsx_file.predict(ent_X)[0]), 2)
                        ey = round(float(epsy_file.predict(ent_X)[0]), 2)
                        ez = round(float(epsz_file.predict(ent_X)[0]), 2)

                    if mbj > 0.1:

                        mex = round(float(mepsx_file.predict(ent_X)[0]), 2)
                        mey = round(float(mepsy_file.predict(ent_X)[0]), 2)
                        mez = round(float(mepsz_file.predict(ent_X)[0]), 2)

                    # sgp= ''#str(SpacegroupAnalyzer(struct).get_space_group_symbol())
                    # result = 'Formation energy/atom (eV):'+str(f_en)+'\nKpoint: '+str(kpoint)+str('\nCut-off (eV): ')+str(encut)+'\nBandgap OptB88vdW (eV): '+str(bg)+'\nBandgap TBmBJ (eV):'+str(mbj)+'\nModulus bulk (GPa): '+str(kv)+'\nModulus shear (GPa): '+str(gv)+'\nStatic refractive-index OptB88vdW (x): '+str(ex)+'\nStatic Refractive-index OptB88vdW (y): '+str(ey)+'\nStatic Refractive-index OptB88vdW (z): '+str(ez)+ '\nStatic refractive-index TBmBJ (x): '+str(mex)+'\nStatic Refractive-index TBmBJ (y): '+str(mey)+'\nStatic Refractive-index TBmBJ (z): '+str(mez)+'\nPotential solar-cell: '+str(slme_pred)+'\nPotential high-n-Seebeck: '+str(nseeb_pred)+'\nPotential high-p-Seebeck: '+str(pseeb_pred)+'\nPotential high-n-powerfactor: '+str(npf_pred)+'\nPotential high-p-powerfactor: '+str(ppf_pred)+'\nPotential high-n-ZT: '+str(nzt_pred)+'\nPotential high-p-ZT: '+str(pzt_pred)+'\ninput'+str('\n'+ entry)+'\n'
                    result = (
                        "Formation energy/atom (eV):"
                        + str(f_en)
                        + "\nKpoint: "
                        + str(kpoint)
                        + str("\nCut-off (eV): ")
                        + str(encut)
                        + "\nBandgap OptB88vdW (eV): "
                        + str(bg)
                        + "\nBandgap TBmBJ (eV):"
                        + str(mbj)
                        + "\nModulus bulk (GPa): "
                        + str(kv)
                        + "\nModulus shear (GPa): "
                        + str(gv)
                        + "\nStatic refractive-index OptB88vdW (x): "
                        + str(ex)
                        + "\nStatic Refractive-index OptB88vdW (y): "
                        + str(ey)
                        + "\nStatic Refractive-index OptB88vdW (z): "
                        + str(ez)
                        + "\nStatic refractive-index TBmBJ (x): "
                        + str(mex)
                        + "\nStatic Refractive-index TBmBJ (y): "
                        + str(mey)
                        + "\nStatic Refractive-index TBmBJ (z): "
                        + str(mez)
                        + "\nPotential solar-cell: "
                        + str(slme_pred)
                        + "\nPotential high-n-Seebeck: "
                        + str(nseeb_pred)
                        + "\nPotential high-p-Seebeck: "
                        + str(pseeb_pred)
                        + "\nPotential high-n-powerfactor: "
                        + str(npf_pred)
                        + "\nPotential high-p-powerfactor: "
                        + str(ppf_pred)
                        + "\n input"
                        + str("\n" + body)
                        + "\n"
                    )

        except Exception:
            print("Cannot run JARVISML.")
            pass
    return render(
        request, "jarvisml/jarvisml.html", {"form": form, "result": result}
    )


# return render(request, "jarvisml/jarvisml.html", context={"form": form, "result": result})
