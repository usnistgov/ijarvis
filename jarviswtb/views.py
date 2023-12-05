# from core_main_app.utils.rendering import render
from django.shortcuts import render
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

from numpy import linalg as LA
from jarvis.io.vasp.inputs import Kpoints

# from jarvis.core.kpoints import Kpoints3D as Kpoints
from jarvis.db.jsonutils import loadjson

# opts=loadjson('options.json')
root_path = os.path.join(os.path.dirname(__file__))

all_wanns = loadjson(os.path.join(os.path.dirname(__file__), "all_wanns.json"))

fls = loadjson(
    os.path.join(
        os.path.dirname(__file__), "..", "jarvissolar", "fileinfo.json"
    )
)


def get_wann_url(jid="JVASP-1002"):
    for i in fls["WANN"]:
        if i["name"].split(".zip")[0] == jid:
            return i["download_url"]


def band_diagram(eigs=[], labels=[], en_dos=[], dos=[], pdos=[]):
    img = io.BytesIO()

    fig = plt.figure(figsize=(20, 10))
    plt.rcParams.update({"font.size": 22})
    the_grid = GridSpec(1, 2)
    plt.subplot(the_grid[0])
    plt.title("Bandstructure")
    for i, ii in enumerate(eigs):
        plt.plot(ii, color="b")

    if labels != []:
        kp_labels_points = []
        kp_labels = []
        for k, kk in enumerate(labels):
            if kk != "":
                kp_labels_points.append(k)
                kp_labels.append(kk)
        plt.xticks(kp_labels_points, kp_labels)
    plt.ylabel("Energy (E-E$_f$) (eV)")
    plt.xlim([0, eigs.shape[1] - 1])
    plt.ylim([-4, 4])
    # plt.axhline(y=0,linestyle='-.',c='g')

    plt.subplot(the_grid[1])
    # plt.axvline(y=0,linestyle='-.',c='g')
    plt.title("Density of states")
    plt.plot(en_dos, dos)
    plt.ylim(0, max(dos))
    plt.xlim([-4, 4])
    plt.xlabel("Energy(eV)")
    plt.ylabel("DOS")

    plt.tight_layout()
    plt.savefig(img, format="png")
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    return plot_url  #'<img src="data:image/png;base64,{}">'.format(plot_url)


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
    plot_url = False
    maxdiff_bz = False
    result = ""
    zip_file_url = ""
    maxdiff_mesh = ""
    selected_mat = ""
    nwan = ""
    total_time = ""
    spg = ""
    efermi = ""
    total_time = ""
    formula = ""
    jid = ""
    calc_type = "Bandstructure and DOS"
    if request.method == "POST":
        try:
            form = ContactForm(request.POST)
            if form.is_valid():
                mat = form.cleaned_data["category"]
                # kpoints = str(form.cleaned_data["kpoints"]).split("\n")
                kpoints = [
                    i.strip("\r")
                    for i in str(form.cleaned_data["kpoints"]).split("\n")
                ]
                formula = mat.split("_")[0]
                spg = mat.split("{")[1].split("[")[0]
                jid = mat.split("[")[1].split("]")[0]
                jid = str(jid).strip()
                kp = Kpoints.read(kpoints)
                labels = kp.labels
                kpts = kp.kpts
                mat_url = (
                    str(formula) + str("{") + str(spg) + str("}")
                )  # +str('[')+str('<a href=https://www.ctcms.nist.gov/~knc6/jsmol/')+str(jid1)+str('.html')+str(' target="_blank" >')+str(jid1)+str('</a>')
                # print ('all_kps',all_kps)
                # efermi = 5.5
                for i in all_wanns:
                    strp = jid.strip()
                    # print ('jid3',i['jid'])
                    if i["jid"] == strp:
                        zip_file_url = get_wann_url(i["jid"])
                        # dat_path=os.path.join(root_path,i['jid']+'.zip')
                        # zip_file_url = (
                        #    str(
                        #        "https://www.ctcms.nist.gov/~knc6/static/WannierWeb/"
                        #    )
                        #    + str(i["jid"])
                        #    + str(".zip")
                        # )

                        r = requests.get(zip_file_url)
                        # archive = zipfile.ZipFile(dat_path, 'r')
                        z = zipfile.ZipFile(io.BytesIO(r.content))
                        wdat = z.read("wannier90_hr.dat").decode("utf-8")
                        fd, path = tempfile.mkstemp()
                        with os.fdopen(fd, "w") as tmp:
                            tmp.write(wdat)

                        # wdat=os.path.join(root_path,i['jid'],'wannier90_hr.dat')
                        maxdiff_bz = round(i["maxdiff_bz"], 3)
                        maxdiff_mesh = round(i["maxdiff_mesh"], 3)
                        efermi = i["efermi"]
                        break

            if wdat != None:
                t1 = time.time()
                # fp.seek(0)
                w = WannierHam(filename=path)
                os.remove(path)
                nwan = w.nwan
                eigs = w.band_structure_eigs(kpath=kpts, efermi=efermi).T
                en_dos, dos, pdos = w.dos(
                    kpoints=kpts, efermi=efermi, sig=0.1, nenergy=1000
                )
                t2 = time.time()
                total_time = round(t2 - t1, 4)
                wdat_path = wdat

                plot_url = band_diagram(
                    eigs=eigs, labels=labels, en_dos=en_dos, dos=dos, pdos=pdos
                )
                png = str(strp) + str(".png")
                comp_url = os.path.join(root_path, strp, png)
                selected_mat = str(mat).replace("{", "(").replace("}", ")")
        except Exception:
            print("Cannot run Wannier tight binding.")
            pass

    return render(
        request,
        "jarviswtb/wtb.html",
        {
            "form": form,
            "plot_url": plot_url,
            "maxdiff_bz": maxdiff_bz,
            "maxdiff_mesh": maxdiff_mesh,
            "selected_mat": selected_mat,
            "download_link": zip_file_url,
            "nwan": nwan,
            "total_time ": total_time,
            "spg": spg.split("}")[0],
            "efermi": efermi,
            "calc_type": calc_type,
            "total_time": total_time,
            "formula": formula + " ",
            "jid": jid,
        },
    )
