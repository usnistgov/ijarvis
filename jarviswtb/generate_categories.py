from jarvis.db.jsonutils import loadjson,dumpjson
from jarvis.db.figshare import data
import os
from jarvis.analysis.structure.spacegroup import Spacegroup3D
from jarvis.core.atoms import Atoms
dat = loadjson(os.path.join(os.path.dirname(__file__), "all_wanns.json"))


"""
#Generate options
import glob
from jarvis.analysis.structure.spacegroup import Spacegroup3D
from jarvis.io.vasp.inputs import Poscar
dat2='C:\\Users\\kamal\\Downloads\\JARVIS-WannierDB\\STORE4\\V1\\Wannier2D'
dat3='C:\\Users\\kamal\\Downloads\\JARVIS-WannierDB\\STORE4\\V1\\Wannier3D'
mem=[]
for i in glob.glob(dat3+'\JVASP*'):
    try:
        pos=Poscar.from_file(i+'\\POSCAR')
        spg=Spacegroup3D(pos.atoms).space_group_symbol
        formula=pos.atoms.composition.reduced_formula
        dim='3D'
        jid=i.split('\\')[-1]
        line=formula+'_'+dim+'_{'+spg+'}['+jid+']'
        mem.append(line)
    except:
        print ('failed for',i)
        pass
for i in glob.glob(dat2+'\JVASP*'):
    try:
        pos=Poscar.from_file(i+'\\POSCAR')
        spg=Spacegroup3D(pos.atoms).space_group_symbol
        formula=pos.atoms.composition.reduced_formula
        dim='2D'
        jid=i.split('\\')[-1]
        line=formula+'_'+dim+'_{'+spg+'}['+jid+']'
        mem.append(line)  
    except:
        print ('failed for',i)
        pass
from jarvis.db.jsonutils import loadjson,dumpjson
dumpjson(data=mem,filename='options.json')
"""
d3d=data('dft_3d')
d2d=data('dft_2d')
mem=[]
for i in d3d:
  info={}
  info['jid']=i['jid']
  info['atoms']=i['atoms']
  info['dim']='3D'
  mem.append(info)
for i in d2d:
  info={}
  info['jid']=i['jid']
  info['atoms']=i['atoms']
  info['dim']='2D'
  mem.append(info)
dumpjson(data=mem,filename='combined.json')
comb=loadjson('combined.json')
#print ('Going to options.')
def get_cat(jid='JVASP-1002'):
    for i in comb:
        if i['jid']==jid:
            at=Atoms.from_dict(i['atoms'])
            spg=Spacegroup3D(at).space_group_symbol
            formula=at.composition.reduced_formula
            dim=i['dim']
            line=formula+'_'+dim+'_{'+spg+'}['+i['jid']+']'
            return line
mem=[]
for i in dat:
  if i['maxdiff_bz']<=0.1:
    jid=i['jid']
    line=get_cat(jid)
    mem.append(line)
x=[]
for i in mem:
    if i is not None:
       x.append([i.split('_')[0],i])
y=sorted(x)
new_x=['Si_3D_{Fd-3m}[JVASP-1002]']
for i in y:
  if i!='Si_3D_{Fd-3m}[JVASP-1002]':
    new_x.append(i[1])
dumpjson(data=new_x,filename='options.json')
