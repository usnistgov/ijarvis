# from core_main_app.utils.rendering import render
from django.shortcuts import render
from jarvis.analysis.stm.tersoff_hamann import TersoffHamannSTM
from .forms import ContactForm
from django.http import HttpResponse
from jarvis.io.vasp.inputs import Poscar
from jarvis.ai.descriptors.cfid import CFID
import numpy as np
import os, requests, io, tempfile
import pickle, zipfile, time
from jarvis.io.wannier.outputs import WannierHam
import base64
import matplotlib.pyplot as plt
plt.switch_backend("agg")
from matplotlib.gridspec import GridSpec
from django.utils.decorators import method_decorator
import core_main_app.utils.decorators as decorators
import core_explore_keyword_app.permissions.rights as rights
from django.urls import reverse_lazy, reverse
from numpy import linalg as LA
from jarvis.io.vasp.inputs import Kpoints
# from jarvis.core.kpoints import Kpoints3D as Kpoints
from jarvis.db.jsonutils import loadjson
# opts=loadjson('options.json')
root_path = os.path.join(os.path.dirname(__file__))
all_stm = loadjson(os.path.join(os.path.dirname(__file__), "all_stm.json"))






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
    form = ContactForm(initial={"min_size": 20.0, "ext": 0.15})
    plot_url = False
    material = False
    bias_type = False
    stm_type = False
    spg = ""
    total_time = ""
    formula = ""
    jid = ""
    zcut = None
    min_size = False
    if request.method == "POST":
        try:
            form = ContactForm(request.POST)
            if form.is_valid():
                mat = form.cleaned_data["material"]
                formula = mat.split("_")[0]
                jid = mat.split("_")[1]
                bias_type = form.cleaned_data["bias_type"]
                stm_type = form.cleaned_data["stm_type"]
                print("min_size", min_size)
                min_size = float(form.cleaned_data["min_size"])
                ext = float(form.cleaned_data["ext"])
                try:
                    zcut = float(form.cleaned_data["zcut"])
                except Exception:
                    print("No zcut")
                    pass
                for i in all_stm:

                    # dat_path=os.path.join(root_path,i['jid']+'.zip')
                    if bias_type == "Positive":
                        zip_file_url = (
                            str(
                                "https://www.ctcms.nist.gov/~knc6/static/JARVIS-DFT-STM/Positive_bias/"
                            )
                            + str(jid)
                            + str("_Positive.zip")
                        )
                    elif bias_type == "Negative":
                        zip_file_url = (
                            str(
                                "https://www.ctcms.nist.gov/~knc6/static/JARVIS-DFT-STM/Negative_bias/"
                            )
                            + str(jid)
                            + str("_Negative.zip")
                        )
                    else:
                        print("Unknown bias type", bias_type, type(bias_type))
                    print("zip_file_url", zip_file_url)
                    r = requests.get(zip_file_url)
                    # archive = zipfile.ZipFile(dat_path, 'r')
                    z = zipfile.ZipFile(io.BytesIO(r.content))
                    pchg = z.read("PARCHG").decode("utf-8")
                    fd, path = tempfile.mkstemp()
                    with os.fdopen(fd, "w") as tmp:
                        tmp.write(pchg)

                    # wdat=os.path.join(root_path,i['jid'],'wannier90_hr.dat')
                    break

            if pchg != None:
                t1 = time.time()
                # fp.seek(0)
                if zcut is not None:
                    TH_STM = TersoffHamannSTM(
                        chg_name=path, min_size=min_size, zcut=zcut
                    )
                    zcut1 = int((zcut + 2) / TH_STM.c * TH_STM.nz)
                    TH_STM = TersoffHamannSTM(
                        chg_name=path, min_size=min_size, zcut=zcut1
                    )
                else:
                    TH_STM = TersoffHamannSTM(
                        chg_name=path, min_size=min_size, zcut=None
                    )

                img = io.BytesIO()
                if stm_type == "Constant height":
                    t_height = TH_STM.constant_height(filename=img)
                elif stm_type == "Constant current":
                    t_height = TH_STM.constant_current(filename=img, ext=ext)
                else:
                    print("Cannot find STM type.", stm_type)
                img.seek(0)
                plot_url = base64.b64encode(img.getvalue()).decode()
                # vals=t_height['img_ext']
                os.remove(path)
                t2 = time.time()
                total_time = round(t2 - t1, 4)

                # plot_url = stm_diagram(
                #    arr=vals,
                # )
                png = str(jid) + str(".png")
                comp_url = os.path.join(root_path, jid, png)
                material = str(mat)  # .replace("{", "(").replace("}", ")")
        except Exception as ex:
            print("Cannot run STM image.", ex)
            pass

    return render(
        request,
        "jarvisstm/stm.html",
        {
            "form": form,
            "plot_url": plot_url,
            "material": material,
            "total_time ": total_time,
            "formula": formula + " ",
            "jid": jid,
        },
    )
