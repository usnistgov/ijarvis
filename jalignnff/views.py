# from core_main_app.utils.rendering import render
from django.shortcuts import render
from .forms import ContactForm
from django.http import HttpResponse
from jarvis.io.vasp.inputs import Poscar

# from jarvis.ai.descriptors.cfid import CFID
import matplotlib.pyplot as plt

plt.switch_backend("agg")
import numpy as np
import os, io
import base64
from jarvis.core.graphs import Graph
from alignn.models.alignn import ALIGNN, ALIGNNConfig
import torch
from jarvis.core.kpoints import Kpoints3D as Kpoints
# import joblib, pickle
from numpy import linalg as LA
from jarvis.core.kpoints import Kpoints3D
from alignn.ff.ff import AlignnAtomwiseCalculator, ForceField
#from . import plot_phonons_ff  # plot_phonons_ff.import ase_phonon
from ase import Atoms as AseAtoms
from matplotlib.gridspec import GridSpec
device = "cpu"
# if torch.cuda.is_available():
#        device = torch.device("cuda")
import torch

torch.cuda.is_available = lambda: False

base_path = os.path.join(os.path.dirname(__file__), "extras", "phonon")
def_path = os.path.join(os.path.dirname(__file__), "extras", "wt10") #default_path()
calc_phonon = AlignnAtomwiseCalculator(path=base_path,device=device)
calc_deafult = AlignnAtomwiseCalculator(path=def_path,device=device)


from django.utils.decorators import method_decorator
import core_main_app.utils.decorators as decorators
import core_explore_keyword_app.permissions.rights as rights
from django.urls import reverse_lazy, reverse


def phonons(
    atoms=None,
    enforce_c_size=8,
    line_density=5,
    model_path=".",
    model_filename="best_model.pt",
    on_relaxed_struct=False,
    dim=[2, 2, 2],
    freq_conversion_factor=333.566830/2,  # ThztoCm-1
    phonopy_bands_figname="phonopy_bands.png",
    # phonopy_dos_figname="phonopy_dos.png",
    write_fc=False,
):
    """Make Phonon calculation setup."""
    calc = AlignnAtomwiseCalculator(
        path=model_path,
        force_mult_natoms=False,
        force_multiplier=1,
        stress_wt=-4800,
    )

    from phonopy import Phonopy
    from phonopy.file_IO import (
        write_FORCE_CONSTANTS,
    )

    kpoints = Kpoints().kpath(atoms, line_density=line_density)
    bulk = atoms.phonopy_converter()
    phonon = Phonopy(bulk, [[dim[0], 0, 0], [0, dim[1], 0], [0, 0, dim[2]]])
    phonon.generate_displacements(distance=0.01)
    # print("Len dis", len(phonon.supercells_with_displacements))
    supercells = phonon.get_supercells_with_displacements()
    # Force calculations by calculator
    set_of_forces = []
    disp = 0

    for scell in supercells:
        ase_atoms = AseAtoms(
            symbols=scell.get_chemical_symbols(),
            scaled_positions=scell.get_scaled_positions(),
            cell=scell.get_cell(),
            pbc=True,
        )
        ase_atoms.calc = calc
        # energy = ase_atoms.get_potential_energy()
        forces = np.array(ase_atoms.get_forces())
        disp = disp + 1

        drift_force = forces.sum(axis=0)
        for force in forces:
            force -= drift_force / forces.shape[0]
        set_of_forces.append(forces)
    phonon.produce_force_constants(forces=set_of_forces)
    if write_fc:
        write_FORCE_CONSTANTS(
            phonon.get_force_constants(), filename="FORCE_CONSTANTS"
        )

    lbls = kpoints.labels
    lbls_ticks = []
    freqs = []
    tmp_kp = []
    lbls_x = []
    count = 0
    for ii, k in enumerate(kpoints.kpts):
        k_str = ",".join(map(str, k))
        if ii == 0:
            tmp = []
            for i, freq in enumerate(phonon.get_frequencies(k)):
                tmp.append(freq)
            freqs.append(tmp)
            tmp_kp.append(k_str)
            lbl = "$" + str(lbls[ii]) + "$"
            lbls_ticks.append(lbl)
            lbls_x.append(count)
            count += 1
            # lbls_x.append(ii)
        elif k_str != tmp_kp[-1]:
            tmp_kp.append(k_str)
            tmp = []
            for i, freq in enumerate(phonon.get_frequencies(k)):
                tmp.append(freq)
            freqs.append(tmp)
            lbl = lbls[ii]
            if lbl != "":
                lbl = "$" + str(lbl) + "$"
                lbls_ticks.append(lbl)
                # lbls_x.append(ii)
                lbls_x.append(count)
            count += 1
    # lbls_x = np.arange(len(lbls_ticks))

    freqs = np.array(freqs)
    freqs = freqs * freq_conversion_factor
    # print('freqs',freqs,freqs.shape)
    the_grid = GridSpec(1, 2, width_ratios=[3, 1], wspace=0.0)
    plt.rcParams.update({"font.size": 18})
    plt.figure(figsize=(10, 5))
    plt.subplot(the_grid[0])
    for i in range(freqs.shape[1]):
        plt.plot(freqs[:, i], lw=2, c="b")
    for i in lbls_x:
        plt.axvline(x=i, c="black")
    plt.xticks(lbls_x, lbls_ticks)
    # print('lbls_x',lbls_x,len(lbls_x))
    # print('lbls_ticks',lbls_ticks,len(lbls_ticks))
    plt.ylabel("Frequency (cm$^{-1}$)")
    plt.xlim([0, max(lbls_x)])

    phonon.run_mesh([40, 40, 40], is_gamma_center=True, is_mesh_symmetry=False)
    phonon.run_total_dos()
    tdos = phonon._total_dos

    # print('tods',tdos._frequencies.shape)
    freqs, ds = tdos.get_dos()
    freqs = np.array(freqs)
    freqs = freqs * freq_conversion_factor
    min_freq = -0.05 * freq_conversion_factor
    max_freq = max(freqs)
    plt.ylim([min_freq, max_freq])

    plt.subplot(the_grid[1])
    plt.fill_between(
        ds, freqs, color=(0.2, 0.4, 0.6, 0.6), edgecolor="k", lw=1, y2=0
    )
    plt.xlabel("DOS")
    # plt.plot(ds,freqs)
    plt.yticks([])
    plt.xticks([])
    plt.ylim([min_freq, max_freq])
    plt.xlim([0, max(ds)])
    plt.tight_layout()
    img = io.BytesIO()
    plt.savefig(img)
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    # print('freqs',freqs)
    # print('ds',ds)
    # print('tods',tdos.get_dos())
    # dosfig = phonon.plot_total_dos()
    # dosfig.savefig(phonopy_dos_figname)
    # dosfig.close()

    return plot_url
    #return phonon

def ev_curve(
    atoms=None,
    dx=np.arange(-0.05, 0.05, 0.01),
    model_path=".",
    model_filename="best_model.pt",
    fig_name="eos.png",
    on_relaxed_struct=False,
):
    """Get EV curve."""
    if on_relaxed_struct:
        ff = ForceField(
            jarvis_atoms=atoms,
            model_path=model_path,
            model_filename=model_filename,
        )
        relaxed, en, fs = ff.optimize_atoms(logfile=None)
    else:
        relaxed = atoms
    y = []
    vol = []
    for i in dx:
        s1 = relaxed.strain_atoms(i)
        ff = ForceField(
            jarvis_atoms=s1,
            model_path=model_path,
            model_filename=model_filename,
        )
        energy, fs = ff.unrelaxed_atoms()
        y.append(energy)
        vol.append(s1.volume)
    x = np.array(dx)
    y = np.array(y)
    # eos = EquationOfState(vol, y, eos="murnaghan")
    # v0, e0, B = eos.fit()
    # kv = B / kJ * 1.0e24  # , 'GPa')
    # print("KV", kv)
    # eos.plot(show=True)
    # eos.plot(fig_name)
    print("E", y)
    print("V", vol)
    return vol, y  # , eos, kv
    # return x, y #, eos, kv


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
            "body": "FCC Al\n1.0\n4.06741 0.0 0.0\n0.0 4.06741 0.0\n0.0 0.0 4.06741\nAl\n4\ndirect\n0.0 0.0 0.0 \n0.0 0.5 0.5 \n0.5 0.0 0.5 \n0.5 0.5 0.0 \n",
        }
    )
    result = ""
    plot_url = False
    plot_url2 = False
    if request.method == "POST":
        #calc_phonon = AlignnAtomwiseCalculator(path=base_path, device=device)
        #calc_deafult = AlignnAtomwiseCalculator(path=def_path, device=device)
        try:
            form = ContactForm(request.POST)
            if form.is_valid():
                body = form.cleaned_data["body"]
                mat = Poscar.from_string(body).atoms

                if len(body) < 20000:
                    ff = ForceField(
                        jarvis_atoms=mat, model_path=def_path, stress_wt=0.1
                    )
                    # ff = ForceField(jarvis_atoms=mat,model_path=def_path,stress_wt=10.0,force_mult_natoms=False)
                    opt, en, fs = ff.optimize_atoms(logfile=None)
                    opt_pos = Poscar(opt).to_string()
                    result = (
                        "Energy(eV):" + str(round(en, 5)) + "\n"
                        "Optimized structure:\n"
                        + str(opt_pos)
                        + "\n"
                        + "\n\n input"
                        + str("\n" + body)
                        + "\n"
                    )
                    #plot_url = plot_phonons_ff.ase_phonon(atoms=opt)
                    plot_url = phonons(atoms=opt,model_path=base_path)



                    plt.close()
                    plt.clf()
                    img2 = io.BytesIO()
                    x, y = ev_curve(atoms=opt, model_path=def_path)
                    plt.plot(x, y, "-o")
                    plt.xlabel("Vol ($\AA$$^3$)")
                    plt.ylabel("Energy (eV/atom)")
                    plt.tight_layout()
                    plt.savefig(img2, format="png")
                    img2.seek(0)
                    plot_url2 = base64.b64encode(img2.getvalue()).decode()
                    plt.clf()
                    plt.close()
        except Exception as exp:
            print("Cannot run JARVIS-ALIGNN.", exp)
            result = "Error:" + str(exp)
            pass
    return render(
        request,
        "jalignnff/jalignnff.html",
        {
            "form": form,
            "result": result,
            "plot_url": plot_url,
            "plot_url2": plot_url2,
        },
    )
    # return render(request, "jalignnff/jalignnff.html", context={"form": form, "result": result})
