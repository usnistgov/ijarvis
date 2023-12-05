from jarvis.db.jsonutils import loadjson, dumpjson
from jarvis.db.figshare import data
import os
from jarvis.analysis.structure.spacegroup import Spacegroup3D
from jarvis.core.atoms import Atoms

from jarvis.core.atoms import Atoms
from jarvis.analysis.structure.spacegroup import Spacegroup3D
from jarvis.db.figshare import data

d3d = data("dft_3d")

fls = data("raw_files")
tb_links = []
for i in fls["TBMBJ"]:
    jid = i["name"].split(".zip")[0]
    tb_links.append(jid)


options = []
for i in d3d:
    if (
        i["mbj_bandgap"] != "na"
        and i["mbj_bandgap"] >= 0.5
        and i["jid"] in tb_links
    ):
        at = Atoms.from_dict(i["atoms"])
        spg = Spacegroup3D(at).space_group_symbol
        formula = at.composition.reduced_formula
        line = formula + "{" + spg + "}[" + i["jid"] + "]"
        options.append(line)
print("len=", len(options))
y = sorted(options)
new_x = ["Si{Fd-3m}[JVASP-1002]"]
for i in y:
    if i != "Si{Fd-3m}[JVASP-1002]":
        new_x.append(i)
dumpjson(data=new_x, filename="options.json")
