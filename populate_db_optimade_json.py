# export DJANGO_SETTINGS_MODULE=mdcs.dev_settings
# python manage.py makemigrations --settings=mdcs.dev_settings optimade
# python manage.py migrate --settings=mdcs.dev_settings
# python populate_db_optimade_json.py
import django
import logging
import os
import sys
import json
import zipfile
from jarvis.db.jsonutils import loadjson, dumpjson

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mdcs.settings")
sys.path.append(
    os.path.join(os.path.realpath(os.path.dirname(__file__)), "..", "..")
)
django.setup()
from optimade.models import Optimade
from jarvis.core.atoms import Atoms as JAtoms
from optimade.atoms import OptimadeAdaptor

# from jarvis.core.atoms import OptimadeAdaptor
from jarvis.db.figshare import data
from django.core import management
import random

# create = False
rand_ints = [
    1000000,
    563728,
    97623847,
    435267819,
    95548723,
    435627,
    92837211,
    4637782121,
    4537782121,
    4637582121,
    1000001,
    1000004,
    100000006,
    5463782910,
    192837645,
    23456098,
    872662718928,
    852662718928,
    852632718928,
    952662718928,
    92662718928,
    192662718928,
    1992718928,
    5992718928,
    6992718928,
    7992718928,
    8992718928,
    8792718928,
    8692718928,
]
# from random import randrange
# create = False

use_jarvis_tools = True
# Keep it false for production
# cdcs doesnt like download
# data from figshare

"""
if use_jarvis_tools:
    dft_2d_data = data("dft_2d")
    dft_3d_data = data("dft_3d")
else:
    root_path = os.path.join(os.path.dirname(__file__))
    dft_2d = os.path.join(
        os.path.dirname(__file__), "optimade", "d2-3-12-2021.json.zip"
    )
    dft_2d_zip = (
        zipfile.ZipFile(dft_2d).read("d2-3-12-2021.json").decode("utf-8")
    )
    # fd, path = tempfile.mkstemp()
    # with os.fdopen(fd, "w") as tmp:
    #    tmp.write(dft_2d_zip)
    # dft_2d_data = loadjson(path)
    dft_2d_data = json.loads(dft_2d_zip)

    dft_3d = os.path.join(
        os.path.dirname(__file__), "optimade", "jdft_3d-8-18-2021.json.zip"
    )
    dft_3d_zip = (
        zipfile.ZipFile(dft_3d).read("jdft_3d-8-18-2021.json").decode("utf-8")
    )
    # fd, path = tempfile.mkstemp()
    # with os.fdopen(fd, "w") as tmp:
    #    tmp.write(dft_3d_zip)
    # dft_3d_data = loadjson(path)
    dft_3d_data = json.loads(dft_3d_zip)

"""


def optimade_data(
    data_array=[],
    source="JARVIS-DFT-2D",
    create=False,
    id_tag="jid",
    na_padding=-99999,
    json_name="optimade/dft_2d.json.zip",
):
    count = 0

    fields = (
        id_tag,
        "nelements",
        "nsites",
        "chemical_formula_reduced",
        "elements",
        "crys",
        "ehull",
        "spg_number",
        "formation_energy_peratom",
        "optb88vdw_total_energy",
        "optb88vdw_bandgap",
        "mbj_bandgap",
        "hse_gap",
        "magmom_oszicar",
        "spillage",
        "slme",
        "encut",
        "kpoint_length_unit",
        "icsd",
        "exfoliation_energy",
        "bulk_modulus_kv",
        "shear_modulus_gv",
    )
    if create:
        zip_name = json_name + ".zip"
        print("zip_name", zip_name)
        if create and not os.path.exists(zip_name):
            print("Making", zip_name, os.path.exists(zip_name))
            print("Creating DB and making json file", zip_name)
            if source == "JARVIS-DFT-2D":
                dft_2d_data = data("dft_2d")
            elif source == "JARVIS-DFT-3D":
                dft_3d_data = data("dft_3d")
            else:
                print("Check DB exists.", source)
            # Migrate
            print("HERE1")
            jids = []
            unique_jids = []
            dat = dft_2d_data
            data_array = dft_2d_data
            for i in data_array:
                if i[id_tag] not in jids:
                    jids.append(i[id_tag])
                    unique_jids.append(i[id_tag])
                else:
                    print("error", i[id_tag])
                    i["jid"] = "JVASP-" + str(rand_ints[count])
                    count += 1
            management.call_command("migrate", no_input=True)
            # x = OptimadeAdaptor(JAtoms.from_dict(dat[0]['atoms'])).to_optimade(idx='xxx')
            # x['attributes']['elements']=x['attributes']['elements'].tolist()
            # x['attributes']['species_at_sites']=x['attributes']['species_at_sites'].tolist()
            # mat1 = Atomss.objects.create(attributes=x)
            jids = []
            mem = []
            for i in data_array:
                for j in fields:
                    try:
                        if i[j] == "na":
                            i[j] = na_padding
                    except:
                        pass
                mem.append(i)

            mem2 = []
            for ii, i in enumerate(mem):
                if i["jid"] in unique_jids:  # and ii<10:
                    # if i['jid'] not in jids: # and ii<10:
                    jids.append(i["jid"])
                    x = OptimadeAdaptor(
                        JAtoms.from_dict(i["atoms"])
                    ).to_optimade(idx=i["jid"])
                    x["attributes"]["source"] = source
                    x["attributes"]["_jarvis_source"] = source
                    x["attributes"]["elements"] = x["attributes"][
                        "elements"
                    ].tolist()
                    x["attributes"]["species_at_sites"] = x["attributes"][
                        "species_at_sites"
                    ].tolist()
                    # print (i['jid'])
                    # else:
                    #    print ('error',i['jid'])
                    #    i['jid']='JVASP-999999'
                    tmp = i["search"].split("-")
                    tmp.remove("")
                    tmp = sorted(tmp)
                    info = {}
                    # print (i,i.keys())
                    info["id"] = i["jid"].split("-")[1]
                    info["nelements"] = (
                        len(i["search"].split("-")) - 1
                    )  # i["nelements"] #len(list(set(i["atoms"]["elements"])))
                    print(
                        'info["nelements"]',
                        info["nelements"],
                        i["atoms"]["elements"],
                    )
                    info["source"] = source
                    info["attributes"] = x["attributes"]
                    info["nsites"] = i["nat"]
                    info["atoms"] = i["atoms"]
                    info["jid"] = i["jid"]
                    info["type"] = "structures"
                    info["chemical_formula_reduced"] = x["attributes"][
                        "chemical_formula_anonymous"
                    ]
                    info["chemical_formula_anonymous"] = x["attributes"][
                        "chemical_formula_anonymous"
                    ]
                    info["elements"] = i["search"]
                    info["crys"] = i["crys"]
                    info["ehull"] = i["ehull"]
                    info["spg_number"] = int(i["spg_number"])
                    info["formation_energy_peratom"] = i[
                        "formation_energy_peratom"
                    ]
                    info["optb88vdw_total_energy"] = i[
                        "optb88vdw_total_energy"
                    ]
                    info["optb88vdw_bandgap"] = i["optb88vdw_bandgap"]
                    info["mbj_bandgap"] = i["mbj_bandgap"]
                    info["hse_gap"] = i["hse_gap"]
                    info["magmom_oszicar"] = i["magmom_oszicar"]
                    info["spillage"] = i["spillage"]
                    info["slme"] = i["slme"]
                    info["encut"] = i["encut"]
                    info["kpoint_length_unit"] = i["kpoint_length_unit"]
                    info["icsd"] = i["icsd"]
                    info["exfoliation_energy"] = i["exfoliation_energy"]
                    info["bulk_modulus_kv"] = i["bulk_modulus_kv"]
                    info["shear_modulus_gv"] = i["shear_modulus_gv"]
                    mem2.append(info)
            dumpjson(data=mem2, filename=json_name)
            print("Do zip dft2d.json.zip dft2d.json")
        elif create and os.path.exists(zip_name):
            print("Creating DB with json file", json_name)
            root_path = os.path.join(os.path.dirname(__file__))
            zip_name = json_name + ".zip"
            dft_d = os.path.join(
                os.path.dirname(__file__),
                zip_name
                # os.path.dirname(__file__), "optimade", zip_name
            )
            dft_d_zip = (
                zipfile.ZipFile(dft_d)
                .read(json_name.split("/")[-1])
                .decode("utf-8")
            )
            mem2 = json.loads(dft_d_zip)
            # mem2 = loadjson(json_name)

        for ii, i in enumerate(mem2):
            # if i['jid'] not in jids: # and ii<10:
            x = OptimadeAdaptor(JAtoms.from_dict(i["atoms"])).to_optimade(
                idx=i[id_tag]
            )
            x["attributes"]["source"] = source
            x["attributes"]["elements"] = x["attributes"]["elements"].tolist()
            x["attributes"]["species_at_sites"] = x["attributes"][
                "species_at_sites"
            ].tolist()
            # print (i['jid'])
            # else:
            #    print ('error',i['jid'])
            #    i['jid']='JVASP-999999'
            tmp = i["elements"].split("-")
            tmp.remove("")
            tmp = sorted(tmp)
            # print ('tmp',tmp)

            Optimade.objects.create(
                attributes=x["attributes"],
                nelements=i[
                    "nelements"
                ],  # len(list(set(i["atoms"]["elements"]))),
                nsites=i["nsites"],
                jid=i[id_tag],
                id=i[id_tag].split("-")[1],
                type="structures",
                chemical_formula_reduced=x["attributes"][
                    "chemical_formula_reduced"
                ],
                chemical_formula_anonymous=x["attributes"][
                    "chemical_formula_anonymous"
                ],
                # elements=tmp, #i["search"],
                # elements=i["search"],
                elements=i["elements"],
                # search=i["search"],
                crys=i["crys"],
                ehull=i["ehull"],
                spg_number=int(i["spg_number"]),
                formation_energy_peratom=i["formation_energy_peratom"],
                optb88vdw_total_energy=i["optb88vdw_total_energy"],
                optb88vdw_bandgap=i["optb88vdw_bandgap"],
                mbj_bandgap=i["mbj_bandgap"],
                hse_gap=i["hse_gap"],
                magmom_oszicar=i["magmom_oszicar"],
                spillage=i["spillage"],
                slme=i["slme"],
                encut=i["encut"],
                kpoint_length_unit=i["kpoint_length_unit"],
                icsd=i["icsd"],
                exfoliation_energy=i["exfoliation_energy"],
                bulk_modulus_kv=i["bulk_modulus_kv"],
                shear_modulus_gv=i["shear_modulus_gv"],
                source=i["source"],
            )
            # print (i['source'])

        logging.info("Database populated with dummy data.")
    else:
        print("Deleting DB")
        Optimade.objects.all().delete()


if __name__ == "__main__":
    try:
        create = False
        optimade_data(
            source="JARVIS-DFT-2D",
            create=create,
            json_name="optimade/dft2d.json",
        )
    except Exception as exp:
        print("exp", exp)
        pass
    create = True  # False
    optimade_data(
        source="JARVIS-DFT-2D",
        create=create,
        json_name="optimade/dft2d.json",
    )

    # optimade_data(
    #   source="JARVIS-DFT-2D",
    #   create=create,
    #   json_name="optimade/dft3d.json",
    # )
