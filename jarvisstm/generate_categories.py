import glob
from jarvis.analysis.stm.tersoff_hamann import TersoffHamannSTM
from jarvis.db.jsonutils import dumpjson
from jarvis.core.atoms import Atoms
from jarvis.analysis.structure.spacegroup import Spacegroup3D

x = []
mem = []
count = 0
jids = ["C_JVASP-667_{P6/mmm}"]
for i in glob.glob("/rk2/knc6/2D_STM/*_PBEBO/MAIN-STM-NEG-*"):
    if ".json" in i:
        tmp = str(i.split(".json")[0]) + str("/PARCHG")
        # print (tmp)
        x.append(tmp)
        pos = str(i.split(".json")[0]) + str("/POSCAR")
        atoms = Atoms.from_poscar(pos)
        jid = i.split("@")[1].split("_")[0]
        spg = Spacegroup3D(atoms).space_group_symbol
        formula = atoms.composition.reduced_formula
        line = formula + "_" + str(jid) + "_{" + str(spg) + "}"
        print(line)
        # TH_STM = TersoffHamannSTM(chg_name=tmp,min_size=0)
        # t1 = TH_STM.constant_height()
        # print (t1)
        if line not in jids:
            jids.append(line)

y = sorted(jids)
new_y = ["C_JVASP-667_{P6/mmm}"]
for i in y:
    if i not in new_y:
        new_y.append(i)
dumpjson(filename="all_stm.json", data=new_y)
print(len(y))
