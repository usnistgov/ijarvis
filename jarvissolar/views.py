import tempfile, requests, zipfile, os
from jarvis.io.vasp.outputs import Vasprun
import numpy as np
from jarvis.analysis.solarefficiency.solar import SolarEfficiency
import io
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

import requests,zipfile,io,tempfile,os
plt.switch_backend("agg")
from matplotlib.gridspec import GridSpec

from numpy import linalg as LA
from jarvis.io.vasp.inputs import Kpoints

# from jarvis.core.kpoints import Kpoints3D as Kpoints
from jarvis.db.jsonutils import loadjson

# opts=loadjson('options.json')

from jarvis.db.figshare import data
# fls = data('raw_files')
fls = loadjson(os.path.join(os.path.dirname(__file__), "fileinfo.json"))
# new_file, filename = tempfile.mkstemp()
def get_tbmbj_vasprun(jid="JVASP-1002"):
    for i in fls["TBMBJ"]:
        if i["name"].split(".zip")[0] == jid:
            return i


def saturation_point(arr, tol=1):
    # assuming monotonic array
    maxa = max(arr)
    mina = min(arr)
    for i, ii in enumerate(arr):
        if abs(maxa - arr[i]) <= tol:
            return i


import numpy as np
import os
from scipy.interpolate import interp1d
from numpy import interp
import scipy.constants as constants
from scipy.integrate import simps


def tmp_slme(
    material_energy_for_absorbance_data,
    material_absorbance_data,
    material_direct_allowed_gap,
    material_indirect_gap,
    thickness=50e-6,
    temperature=293.15,
    absorbance_in_inverse_centimeters=False,
    cut_off_absorbance_below_direct_allowed_gap=True,
    plot_current_voltage=False,
    filename="slme.png",
):
    """
    Calculate spectroscopic limited maximum efficiency.
    Reuires more info than SQ.
    Args:
        material_energy_for_absorbance_data:
        energy grid for absorbance data
        material_absorbance_data: absorption coefficient in m^-1
        material_direct_allowed_gap: direct bandgap in eV
        material_indirect_gap: indirect bandgap in eV
        thickness: thickness of the material in m
        temperature: working temperature in K
        absorbance_in_inverse_centimeters:
        whether the absorbance data is in the unit of cm^-1
        cut_off_absorbance_below_direct_allowed_gap:
        whether to discard all absorption below bandgap
        plot_current_voltage: whether to plot the current-voltage curve
    Returns:
        The calculated maximum efficiency.
    """
    # Defining constants for tidy equations
    c = constants.c  # speed of light, m/s
    h = constants.h  # Planck's constant J*s (W)
    h_e = constants.h / constants.e  # Planck's constant eV*s
    k = constants.k  # Boltzmann's constant J/K
    k_e = constants.k / constants.e  # Boltzmann's constant eV/K
    e = constants.e  # Coulomb

    # Make sure the absorption coefficient has the right units (m^{-1})
    if absorbance_in_inverse_centimeters:
        material_absorbance_data = material_absorbance_data * 100

    # Load the Air Mass 1.5 Global tilt solar spectrum
    solar_spectrum_data_file = str(
        os.path.join(os.path.dirname(__file__), "am1.5G.dat")
    )

    solar_spectra_wavelength, solar_spectra_irradiance = np.loadtxt(
        solar_spectrum_data_file, usecols=[0, 1], unpack=True, skiprows=2
    )

    solar_spectra_wavelength_meters = solar_spectra_wavelength * 1e-9

    delta = material_direct_allowed_gap - material_indirect_gap
    fr = np.exp(-delta / (k_e * temperature))

    # need to convert solar irradiance from Power/m**2(nm) into
    # photon#/s*m**2(nm) power is Watt, which is Joule / s
    # E = hc/wavelength
    # at each wavelength, Power * (wavelength(m)/(h(Js)*c(m/s))) = ph#/s
    solar_spectra_photon_flux = solar_spectra_irradiance * (
        solar_spectra_wavelength_meters / (h * c)
    )

    # Calculation of total solar power incoming
    power_in = simps(solar_spectra_irradiance, solar_spectra_wavelength)

    # calculation of blackbody irradiance spectra
    # units of W/(m**3), different than solar_spectra_irradiance!!! (This
    # is intentional, it is for convenience)
    blackbody_irradiance = (
        2.0 * h * c ** 2 / (solar_spectra_wavelength_meters ** 5)
    ) * (
        1.0
        / (
            (
                np.exp(
                    h * c / (solar_spectra_wavelength_meters * k * temperature)
                )
            )
            - 1.0
        )
    )

    # I've removed a pi in the equation above - Marnik Bercx

    # Convert the irradiance from Power/m**2(m) into photon#/s*m**2(m)
    blackbody_photon_flux = blackbody_irradiance * (
        solar_spectra_wavelength_meters / (h * c)
    )

    # units of nm
    material_wavelength_for_absorbance_data = (
        (c * h_e) / (material_energy_for_absorbance_data + 0.00000001)
    ) * 10 ** 9

    # absorbance interpolation onto each solar spectrum wavelength

    # creates cubic spline interpolating function, set up to use end values
    #  as the guesses if leaving the region where data exists
    material_absorbance = interp1d(
        material_wavelength_for_absorbance_data,
        material_absorbance_data,
        kind="cubic",
        fill_value=(
            material_absorbance_data[0],
            material_absorbance_data[-1],
        ),
        bounds_error=False,
    )

    material_interpolated_absorbance = np.zeros(
        len(solar_spectra_wavelength_meters)
    )
    for i in range(0, len(solar_spectra_wavelength_meters)):
        # Cutting off absorption data below the gap. This is done to deal
        # with VASPs broadening of the calculated absorption data

        if (
            solar_spectra_wavelength[i]
            < 1e9 * ((c * h_e) / material_direct_allowed_gap)
            or not cut_off_absorbance_below_direct_allowed_gap
        ):
            material_interpolated_absorbance[i] = material_absorbance(
                solar_spectra_wavelength[i]
            )

    absorbed_by_wavelength = 1.0 - np.exp(
        -2.0 * material_interpolated_absorbance * thickness
    )

    #  Numerically integrating irradiance over wavelength array
    # Note: elementary charge, not math e!  ## units of A/m**2   W/(V*m**2)
    J_0_r = (
        e
        * np.pi
        * simps(
            blackbody_photon_flux * absorbed_by_wavelength,
            solar_spectra_wavelength_meters,
        )
    )

    J_0 = J_0_r / fr

    #  Numerically integrating irradiance over wavelength array
    # elementary charge, not math e!  ### units of A/m**2   W/(V*m**2)
    J_sc = e * simps(
        solar_spectra_photon_flux * absorbed_by_wavelength,
        solar_spectra_wavelength,
    )

    #    J[i] = J_sc - J_0*(1 - exp( e*V[i]/(k*T) ) )
    #   #This formula from the original paper has a typo!!
    #    J[i] = J_sc - J_0*(exp( e*V[i]/(k*T) ) - 1)
    #   #Bercx chapter and papers have the correct formula (well,
    #   the correction on one paper)
    def J(V):
        J = J_sc - J_0 * (np.exp(e * V / (k * temperature)) - 1.0)
        return np.array(J)

    def power(V):
        p = np.array(J(V)) * V
        return p

    # A more primitive, but perfectly robust way of getting a reasonable
    # estimate for the maximum power.
    test_voltage = 0
    voltage_step = 0.001
    while power(test_voltage + voltage_step) > power(test_voltage):
        test_voltage += voltage_step

    max_power = power(test_voltage)

    # Calculate the maximized efficience
    efficiency = max_power / power_in

    # This segment isn't needed for functionality at all, but can display a
    # plot showing how the maximization of power by choosing the optimal
    # voltage value works
    V = np.linspace(0, 2, 200)
    JV = J(V)
    PV = power(V)
    # print('efficiency',efficiency)
    # print ('V',V)
    # print('JV',JV)
    # print ('PV',PV)
    info = dict()
    info["efficiency"] = 100 * efficiency
    info["V"] = V
    info["JV"] = JV
    info["PV"] = PV
    return info


def jid_plot(jid="JVASP-1002"):
    the_grid = GridSpec(1, 2)
    plt.rcParams.update({"font.size": 20})
    plt.figure(figsize=(20, 10))

    x = get_tbmbj_vasprun(jid=jid)
    zip_file_url=x["download_url"]
    print('zip_file_url',zip_file_url)
    r = requests.get(zip_file_url)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    wdat = z.read("vasprun.xml").decode("utf-8")
    fd, path = tempfile.mkstemp()
    with os.fdopen(fd, "w") as tmp:
        tmp.write(wdat)
        v=Vasprun(path)

    dirgap = v.get_dir_gap
    indirgap = v.get_indir_gap[0]
    en, abz = v.avg_absorption_coefficient
    abz = np.array(abz) * 100
    thickness = np.arange(1e-8, 5e-6, 1e-8)
    effs = []
    for i in thickness:

        info = tmp_slme(
            en, abz, dirgap, indirgap, plot_current_voltage=False, thickness=i,
            #en, abz, dirgap, indirgap, plot_current_voltage=False, thickness=i,
        )
        eff = info["efficiency"]
        effs.append(eff)
    optm = saturation_point(effs)
    opt_thickness = thickness[optm]
    opt_eff = effs[optm]

    img = io.BytesIO()
    plt.subplot(the_grid[0])
    plt.title("(a)")
    plt.xlabel("Thickness(m)")
    plt.ylabel("SLME(%)")
    plt.plot(thickness, effs, ".")
    plt.scatter([opt_thickness], [opt_eff], s=100, color="g")

    plt.subplot(the_grid[1])
    plt.title("(b)")
    # temperatures=np.arange(10,100,5)
    # effs=[]
    # for t in temperatures:
    #     info = tmp_slme(en, abz, indirgap, indirgap, plot_current_voltage=False,thickness=opt_thickness,temperature=t)
    #     eff=info['efficiency']
    #     effs.append(eff)
    # optm=saturation_point(effs)
    # opt_temp=temperatures[optm]
    # opt_eff=effs[optm]
    # plt.plot(temperatures,effs,'.')
    # plt.scatter([opt_thickness],[opt_eff],s=100,color='g')
    info = tmp_slme(
        en,
        abz,
        dirgap,
        indirgap,
        plot_current_voltage=False,
        thickness=opt_thickness,
    )
    plt.plot(info["V"], info["JV"])
    plt.ylabel("J (arb. unit)")
    plt.xlabel("Voltage(V)")
    # plt.plot(info['V'],info['PV'],linestyle="--",label='PV')
    # plt.legend()

    plt.tight_layout()
    # plt.show()
    plt.savefig(img, format="png")
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    print("opt_thickness,opt_eff", opt_thickness, opt_eff)

    return plot_url


def data_plot(dirgap="", indirgap="", en="", abz="", temperature=""):
    img = io.BytesIO()
    the_grid = GridSpec(1, 2)
    plt.rcParams.update({"font.size": 20})
    plt.figure(figsize=(20, 10))

    abz = np.array(abz)
    en = np.array(en)
    thickness = np.arange(1e-8, 5e-6, 1e-8)
    effs = []
    for i in thickness:

        info = tmp_slme(
            en, abz, dirgap, indirgap, plot_current_voltage=False, thickness=i,
        )
        eff = info["efficiency"]
        effs.append(eff)
    optm = saturation_point(effs)
    opt_thickness = thickness[optm]
    opt_eff = effs[optm]

    plt.subplot(the_grid[0])
    plt.title("(a)")
    plt.xlabel("Thickness(m)")
    plt.ylabel("SLME(%)")
    plt.plot(thickness, effs, ".")
    plt.scatter([opt_thickness], [opt_eff], s=100, color="g")

    plt.subplot(the_grid[1])
    plt.title("(b)")
    # temperatures=np.arange(10,100,5)
    # effs=[]
    # for t in temperatures:
    #     info = tmp_slme(en, abz, indirgap, indirgap, plot_current_voltage=False,thickness=opt_thickness,temperature=t)
    #     eff=info['efficiency']
    #     effs.append(eff)
    # optm=saturation_point(effs)
    # opt_temp=temperatures[optm]
    # opt_eff=effs[optm]
    # plt.plot(temperatures,effs,'.')
    # plt.scatter([opt_thickness],[opt_eff],s=100,color='g')
    info = tmp_slme(
        en,
        abz,
        dirgap,
        indirgap,
        plot_current_voltage=False,
        thickness=opt_thickness,
    )
    plt.plot(info["V"], info["JV"])
    plt.ylabel("J (arb. unit)")
    plt.xlabel("Voltage(V)")
    # plt.plot(info['V'],info['PV'],linestyle="--",label='PV')
    # plt.legend()

    plt.tight_layout()
    # plt.show()
    plt.savefig(img, format="png")
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    print("opt_thickness,opt_eff", opt_thickness, opt_eff)
    return plot_url


# jid_plot('JVASP-1002')


# from core_main_app.utils.rendering import render
root_path = os.path.join(os.path.dirname(__file__))


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
    plot_url2 = False
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
        # print ('POST',request.POST)
        try:
            if "Submit" in request.POST:
                form = ContactForm(request.POST)
                # print ('dfghjkl;',form.cleaned_data["category"])
                if form.is_valid():
                    try:
                        t1 = time.time()
                        mat = form.cleaned_data["category"]
                        # kpoints = str(form.cleaned_data["kpoints"]).split("\n")
                        formula = mat.split("_")[0]
                        spg = mat.split("{")[1].split("[")[0]
                        jid = mat.split("[")[1].split("]")[0]
                        jid = str(jid).strip()
                        t2 = time.time()
                        total_time = round(t2 - t1, 4)

                        plot_url = jid_plot(jid=jid)
                    except Exception as exp:
                        print("Cannot run Solar Submit.", exp)
                        pass

                    # png = str(strp) + str(".png")
                    # comp_url = os.path.join(root_path, strp, png)
                    # selected_mat = str(mat).replace("{", "(").replace("}", ")")

            elif "Send" in request.POST:
                form2 = ContactForm2(request.POST)
                if form2.is_valid():
                    # combined_2  = get_hetero(center_around_origin(info_mis_2['subs_sl']),center_around_origin(info_mis_2['film_sl']))
                    # print ('combined_2',combined_2)
                    try:

                        mat1 = form2.cleaned_data["mat1"]
                        lines = mat1.splitlines()

                        tmp = [float(j) for j in lines[1].split(",")]
                        temperature = tmp[2]
                        dirgap = tmp[1]
                        indirgap = tmp[0]
                        en = []
                        abz = []
                        for i in lines[3:-1]:
                            tmp = [float(j) for j in i.split()]
                            en.append(tmp[0])
                            abz.append(tmp[1])
                        en = np.array(en)
                        abz = np.array(abz)
                        plot_url2 = data_plot(
                            dirgap=dirgap,
                            indirgap=indirgap,
                            en=en,
                            abz=abz,
                            temperature=temperature,
                        )
                        # print('tmp=',tmp)
                    except:
                        pass
            else:
                print("IDK")
        except Exception as exp:
            print("Cannot run Solar.", exp)
            pass

    return render(
        request,
        "jarvissolar/jarvissolar.html",
        {
            "form": form,
            "form2": form2,
            "plot_url": plot_url,
            "plot_url2": plot_url2,
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
