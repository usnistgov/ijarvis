from jarvis.db.figshare import data
import pandas as pd

d2 = data("dft_2d")
d3 = data("dft_3d")
df1 = pd.DataFrame(d3)
df1['type']='3D'
df2 = pd.DataFrame(d2)
df2['type']='2D'
keys = [
    "jid",
    "search",
    "formula",
    "spg_symbol",
    "spg_number",
    "crys",
    "func",
    "formation_energy_peratom",
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
df3 = pd.concat([df1[keys], df2[keys]])
df3.to_csv("extras/search.csv", index=False)
