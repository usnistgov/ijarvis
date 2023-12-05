from ase.build import bulk
from ase.calculators.emt import EMT
#from .phonons import Phonons
from ase.phonons import Phonons
import matplotlib.pyplot as plt  # noqa
from alignn.ff.ff import AlignnAtomwiseCalculator, default_path, ev_curve
from jarvis.analysis.structure.spacegroup import (
    Spacegroup3D,
    symmetrically_distinct_miller_indices,
)
import tempfile
import base64
from jarvis.core.atoms import Atoms as JarvisAtoms
from jarvis.db.figshare import get_jid_data
from ase.cell import Cell
import numpy as np
from jarvis.analysis.thermodynamics.energetics import get_optb88vdw_energy
import torch,io,os
plt.switch_backend("agg")

torch.cuda.is_available = lambda : False

model_path = os.path.join(os.path.dirname(__file__), "extras","phonon")

calc = AlignnAtomwiseCalculator(path=model_path)


def ase_phonon(
    atoms=[],
    N=2,
    path=[],
    jid=None,
    npoints=100,
    dataset="dft_3d",
    delta=0.01,
    emin=-0.01,
    use_cvn=True,
    filename="Al_phonon.png",
    ev_file=None,
):
    # Setup crystal and EMT calculator
    # atoms = bulk("Al", "fcc", a=4.05)

    # Phonon calculator
    # N = 7
    temp_dir = tempfile.TemporaryDirectory()
    img = io.BytesIO()
    if jid is not None:
        atoms = JarvisAtoms.from_dict(
            get_jid_data(jid=jid, dataset=dataset)["atoms"]
        )
        filename = (
            jid + "_" + atoms.composition.reduced_formula + "_phonon.png"
        )
    filename=img
    if use_cvn:
        # atoms = JarvisAtoms.from_dict(get_jid_data(jid="JVASP-816", dataset="dft_3d")["atoms"])
        spg = Spacegroup3D(atoms)
        atoms_cvn = spg.conventional_standard_structure
        lat_sys = spg.lattice_system
    else:
        atoms_cvn = atoms
    if ev_file is not None:
        ev_curve(
            atoms=atoms_cvn,
            fig_name=ev_file,
            model_path=model_path,
            dx=np.arange(-0.05, 0.05, 0.01),
            #dx=np.arange(-0.2, 0.2, 0.05),
        )
        plt.clf()
        plt.close()
    cell = Cell(atoms_cvn.lattice_mat)
    path = cell.bandpath(npoints=npoints)
    print(path)
    atoms = atoms_cvn.ase_converter()
    print(temp_dir.name)

    ph = Phonons(atoms, calc, supercell=(N, N, N), delta=delta,name=temp_dir.name)
    # ph = Phonons(atoms, EMT(), supercell=(N, N, N), delta=0.05)
    ph.run()

    # Read forces and assemble the dynamical matrix
    print('ph read')
    ph.read(acoustic=True)
    print('ph clean')
    ph.clean()
    print('ph bs')

    # path = atoms.cell.bandpath("GXULGK", npoints=100)
    bs = ph.get_band_structure(path)

    dos = ph.get_dos(kpts=(20, 20, 20)).sample_grid(npts=npoints, width=1e-3)

    if os.path.exists(temp_dir.name):
       os.removedirs(temp_dir.name)
    temp_dir.cleanup()
    # Plot the band structure and DOS:
    fig = plt.figure(1, figsize=(7, 4))
    ax = fig.add_axes([0.12, 0.07, 0.67, 0.85])
    # ax = fig.add_axes([0.12, 0.07, 0.67, 0.85])
    # print (bs)
    emax = max(bs.energies.flatten()) + 0.01  # 0.1  # 0.035
    bs.plot(ax=ax, emin=emin, emax=emax, color="blue")
    print('plotting dos')
    dosax = fig.add_axes([0.8, 0.07, 0.17, 0.85])
    dosax.fill_between(
        dos.get_weights(),
        dos.get_energies(),
        y2=0,
        color=(0.2, 0.4, 0.6, 0.6),
        # color="grey",
        edgecolor="blue",
        lw=1,
        where=dos.get_energies() >= emin,
    )
    dosax.set_ylim(emin, emax)
    dosax.set_yticks([])
    dosax.set_xticks([])
    dosax.set_xlabel("DOS", fontsize=18)
    fig.savefig(filename)
    img.seek(0)  
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    #if os.path.exists(temp_dir.name):
    #   os.removedirs(temp_dir.name)
    #temp_dir.cleanup()
    return plot_url


if __name__ == "__main__":
    bs = ase_phonon(jid="JVASP-32", ev_file=None)
    for i in jids:
        try:
            ev_file = i + "_ev.png"
            bs = ase_phonon(jid=i, ev_file=None)
        except:
            pass
    # bs = ase_phonon(jid="JVASP-21195", ev_file="ev.png")
    # bs = ase_phonon(jid="JVASP-943", ev_file="ev.png")
    # bs = ase_phonon(jid="JVASP-1002", ev_file="ev.png")
    # bs = ase_phonon(jid="JVASP-816", ev_file="ev.png")
# bs = ase_phonon(jid="JVASP-1002")
