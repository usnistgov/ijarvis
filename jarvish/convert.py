import json,joblib
from jarvis.core.atoms import Atoms
import jarvis
from jarvis.db.jsonutils import loadjson,dumpjson
from jarvis.analysis.structure.spacegroup import Spacegroup3D

def monty_to_joblib(
    read_file="/cluster/users/knc6/JARVIS-DFT1/mem-dir1L-8-22-2019.json",
    target_file="test.json",
):
    from monty.serialization import loadfn, MontyDecoder
    d = loadfn(read_file, cls=MontyDecoder)
    mem = []
    for i in d:
        info = {}
        jid = i["jid"]
        strt = i["data"][0]["contcar"]
        lattice = strt.lattice.matrix
        fracs = strt.frac_coords
        elements = [j.symbol for j in strt.species]
        atms = Atoms(lattice_mat=lattice, coords=fracs, elements=elements)
        phi = i["phi"]

        info["phi"] = phi
        info["atoms"] = atms.to_dict()
        info["jid"] = jid
        mem.append(info)
    #f = open("MonolayersJOBLIB", "wb")
    #joblib.dump(mem, f, protocol=2)
    #f.close()

    f = open("monolayer_data.json", "w")
    f.write(json.dumps(mem))
    f.close()

def make_options():
    data=loadjson('monolayer_data.json')
    mem=[]
    for i in data:
        atoms=Atoms.from_dict(i['atoms'])
        formula=atoms.composition.reduced_formula
        spg=Spacegroup3D(atoms).space_group_symbol
        jid=i['jid']
        line=formula+'{'+spg+'}['+jid+']'
        mem.append(line)
    dumpjson(data=mem,filename='het_options.json')
#monty_to_joblib()
make_options()
