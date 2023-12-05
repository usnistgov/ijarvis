import numpy as np
import pandas as pd
import json,pickle,joblib
import lightgbm as lgb
import pandas as pd
import json
from jarvis.db.figshare import data
d=data('cfid_3d')
#f=open('/users/knc6/Software/jarvis/jarvis/jarvis/db/jml_3d-4-26-2020.json','r')
#d=json.load(f)
#f.close()
df=pd.DataFrame(d)
typical_data_ranges = {'formation_energy_peratom': [-5, 5], 'optb88vdw_bandgap': [0, 10], 'mbj_bandgap': [0, 10], 'bulk_modulus_kv': [0, 250], 'shear_modulus_gv': [0, 250], 'epsx': [0, 60], 'epsy': [0, 60], 'epsz': [0, 60], 'mepsx': [0, 60], 'mepsy': [0, 60], 'mepsz': [0, 60], 'n-Seebeck': [-600, 10], 'n-powerfact': [0, 5000], 'p-Seebeck': [-10, 600], 'p-powerfact': [0, 5000], 'slme': [0, 40], 'spillage': [0, 4], 'encut': [0, 2000], 'kpoint_length_unit': [0, 200], 'dfpt_piezo_max_dielectric': [0, 100], 'dfpt_piezo_max_dij': [0, 3000], 'dfpt_piezo_max_eij': [0, 10], 'ehull': [0, 1], 'electron_avg_effective_masses_300K': [0, 3], 'hole_avg_effective_masses_300K': [0, 3], 'exfoliation_energy': [0, 1000], 'magmom_oszicar': [0, 10], 'max_ir_mode': [0, 4000], 'total_energy_per_atom': [-10, 3]}



def form_en():
        property = 'formation_energy_peratom'
        df2=df[['desc',property]].replace('na',np.nan).dropna()
        x=[]
        y=[]
        max_range=typical_data_ranges[property][1]
        min_range=typical_data_ranges[property][0]
        for i,j in zip(df2['desc'].values,df2[property].values):
           if len(i)==1557 and j!=float('inf') and j>=min_range and j<=max_range:
             x.append(i)
             y.append(j)
        x=np.array(x,dtype='float')
        y=np.array(y,dtype='float')
        print (x.shape)
        print (y.shape)
        print ('property',property)

        lgbm = lgb.LGBMRegressor()
        f=open('/cluster/users/knc6/JARVIS-ML/QuickReRrun/extras/pickle2-main_reg2_form_enp.pk','rb')
        pkl=pickle.load(f,encoding="latin1")
        f.close()
        model = pkl.fit(x,y)
        filename=str('pickle_form_enp.pk')
        pickle.dump( model, open( filename, "wb" ) )
        filename=str('joblib_form_enp.jb')
        joblib.dump(model, filename)


def optrelax():
        #df1=pd.read_csv('jv.csv')
        #df2=pd.read_csv('Eg_relax.csv')
        #df3=pd.merge(df1,df2,on='jid')
        #x = df3.iloc[:,2:1559].values
        #y = df3['Eg_relax'].values

        property = 'optb88vdw_bandgap'
        df2=df[['desc',property]].replace('na',np.nan).dropna()
        x=[]
        y=[]
        max_range=typical_data_ranges[property][1]
        min_range=typical_data_ranges[property][0]
        for i,j in zip(df2['desc'].values,df2[property].values):
           if len(i)==1557 and j!=float('inf') and j>=min_range and j<=max_range:
             x.append(i)
             y.append(j)
        x=np.array(x,dtype='float')
        y=np.array(y,dtype='float')
        print (x.shape)
        print (y.shape)
        print ('property',property)






        lgbm = lgb.LGBMRegressor()
        f=open('/cluster/users/knc6/JARVIS-ML/QuickReRrun/extras/pickle2-main_reg3b_op_gap.pk','rb')
        pkl=pickle.load(f,encoding="latin1")
        f.close()
        model = pkl.fit(x,y)
        filename=str('pickle_op_gap.pk')
        pickle.dump( model, open( filename, "wb" ) )
        filename=str('joblib_op_gap.jb')
        joblib.dump(model, filename)

def mbjrelax():
        #df1=pd.read_csv('jv.csv')
        #df2=pd.read_csv('Eg_mbj.csv')
        #df3=pd.merge(df1,df2,on='jid')
        #x = df3.iloc[:,2:1559].values
        #y = df3['Eg_mbj'].values
        property = 'mbj_bandgap'
        df2=df[['desc',property]].replace('na',np.nan).dropna()
        x=[]
        y=[]
        max_range=typical_data_ranges[property][1]
        min_range=typical_data_ranges[property][0]
        for i,j in zip(df2['desc'].values,df2[property].values):
           if len(i)==1557 and j!=float('inf') and j>=min_range and j<=max_range:
             x.append(i)
             y.append(j)
        x=np.array(x,dtype='float')
        y=np.array(y,dtype='float')
        print (x.shape)
        print (y.shape)
        print ('property',property)







        lgbm = lgb.LGBMRegressor()
        f=open('/cluster/users/knc6/JARVIS-ML/QuickReRrun/extras/pickle2-main_reg_mbj_gap.pk','rb')
        pkl=pickle.load(f,encoding="latin1")
        f.close()
        model = pkl.fit(x,y)
        filename=str('pickle_mbj_gap.pk')
        pickle.dump( model, open( filename, "wb" ) )
        filename=str('joblib_mbj_gap.jb')
        joblib.dump(model, filename)

def encut():
        #df1=pd.read_csv('jv.csv')
        #df2=pd.read_csv('Encut.csv')
        #df3=pd.merge(df1,df2,on='jid')
        #x = df3.iloc[:,2:1559].values
        #y = df3['Encut'].values

        property = 'encut'
        df2=df[['desc',property]].replace('na',np.nan).dropna()
        x=[]
        y=[]
        max_range=typical_data_ranges[property][1]
        min_range=typical_data_ranges[property][0]
        for i,j in zip(df2['desc'].values,df2[property].values):
           if len(i)==1557 and j!=float('inf') and j>=min_range and j<=max_range:
             x.append(i)
             y.append(j)
        x=np.array(x,dtype='float')
        y=np.array(y,dtype='float')
        print (x.shape)
        print (y.shape)
        print ('property',property)









        lgbm = lgb.LGBMRegressor()
        f=open('/cluster/users/knc6/JARVIS-ML/QuickReRrun/extras/pickle2-main_reg_less_lrn_encut.pk','rb')
        pkl=pickle.load(f,encoding="latin1")
        f.close()
        model = pkl.fit(x,y)
        filename=str('pickle_encut.pk')
        pickle.dump( model, open( filename, "wb" ) )
        filename=str('joblib_encut.jb')
        joblib.dump(model, filename)

def kpoint():
        #df1=pd.read_csv('jv.csv')
        #df2=pd.read_csv('Kpoint.csv')
        #df3=pd.merge(df1,df2,on='jid')
        #x = df3.iloc[:,2:1559].values
        #y = df3['Kpoint'].values
        property = 'kpoint_length_unit'
        df2=df[['desc',property]].replace('na',np.nan).dropna()
        x=[]
        y=[]
        max_range=typical_data_ranges[property][1]
        min_range=typical_data_ranges[property][0]
        for i,j in zip(df2['desc'].values,df2[property].values):
           if len(i)==1557 and j!=float('inf') and j>=min_range and j<=max_range:
             x.append(i)
             y.append(j)
        x=np.array(x,dtype='float')
        y=np.array(y,dtype='float')
        print (x.shape)
        print (y.shape)
        print ('property',property)







        lgbm = lgb.LGBMRegressor()
        f=open('/cluster/users/knc6/JARVIS-ML/QuickReRrun/extras/pickle2-main_reg_less_lrn_kp_leng.pk','rb')
        pkl=pickle.load(f,encoding="latin1")
        f.close()
        model = pkl.fit(x,y)
        filename=str('pickle_kpoint.pk')
        pickle.dump( model, open( filename, "wb" ) )
        filename=str('joblib_kpoint.jb')
        joblib.dump(model, filename)


def kv():
        #df1=pd.read_csv('jv.csv')
        #df2=pd.read_csv('KV.csv')
        #df3=pd.merge(df1,df2,on='jid')
        #x = df3.iloc[:,2:1559].values
        #y = df3['KV_y'].values
        property = 'bulk_modulus_kv'
        df2=df[['desc',property]].replace('na',np.nan).dropna()
        x=[]
        y=[]
        max_range=typical_data_ranges[property][1]
        min_range=typical_data_ranges[property][0]
        for i,j in zip(df2['desc'].values,df2[property].values):
           if len(i)==1557 and j!=float('inf') and j>=min_range and j<=max_range:
             x.append(i)
             y.append(j)
        x=np.array(x,dtype='float')
        y=np.array(y,dtype='float')
        print (x.shape)
        print (y.shape)
        print ('property',property)








        lgbm = lgb.LGBMRegressor()
        #f=open('pickle2-main_reg_less_lrn_kv.pk','rb')
        f=open('/cluster/users/knc6/JARVIS-ML/QuickReRrun/extras/pickle2-main_reg_less_lrn_kv.pk','rb')
        pkl=pickle.load(f, encoding="latin1")
        f.close()
        #f=open('/cluster/users/knc6/JARVIS-ML/QuickReRrun/joblib_kv.jb','rb')
        #jbl=joblib.load(f)
        #f.close()
        model = pkl.fit(x,y)
        filename=str('pickle_kv.pk')
        pickle.dump( model, open( filename, "wb" ) )
        filename=str('joblib_kv.jb')
        joblib.dump(model, filename)

def gv():
        #df1=pd.read_csv('jv.csv')
        #df2=pd.read_csv('GV.csv')
        #df3=pd.merge(df1,df2,on='jid')
        #x = df3.iloc[:,2:1559].values
        #y = df3['GV_y'].values
        property = 'shear_modulus_gv'
        df2=df[['desc',property]].replace('na',np.nan).dropna()
        x=[]
        y=[]
        max_range=typical_data_ranges[property][1]
        min_range=typical_data_ranges[property][0]
        for i,j in zip(df2['desc'].values,df2[property].values):
           if len(i)==1557 and j!=float('inf') and j>=min_range and j<=max_range:
             x.append(i)
             y.append(j)
        x=np.array(x,dtype='float')
        y=np.array(y,dtype='float')
        print (x.shape)
        print (y.shape)
        print ('property',property)








        lgbm = lgb.LGBMRegressor()
        f=open('/cluster/users/knc6/JARVIS-ML/QuickReRrun/extras/pickle2-main_reg_less_lrn_gv.pk','rb')
        pkl=pickle.load(f,encoding="latin1")
        f.close()
        model = pkl.fit(x,y)
        filename=str('pickle_gv.pk')
        pickle.dump( model, open( filename, "wb" ) )
        filename=str('joblib_gv.jb')
        joblib.dump(model, filename)




def opt_diele_x():
        #df1=pd.read_csv('jv.csv')
        #df2=pd.read_csv('Diel_opt_gga_0.csv')
        #df3=pd.merge(df1,df2,on='jid')
        #x = df3.iloc[:,2:1559].values
        #y = np.sqrt(df3['Diel_opt_gga_0'].values)
        property = 'epsx'
        df2=df[['desc',property]].replace('na',np.nan).dropna()
        x=[]
        y=[]
        max_range=typical_data_ranges[property][1]
        min_range=typical_data_ranges[property][0]
        for i,j in zip(df2['desc'].values,df2[property].values):
           if len(i)==1557 and j!=float('inf') and j>=min_range and j<=max_range:
             x.append(i)
             y.append(j)
        x=np.array(x,dtype='float')
        y=np.array(y,dtype='float')
        print (x.shape)
        print (y.shape)
        print ('property',property)








        lgbm = lgb.LGBMRegressor()
        f=open('/cluster/users/knc6/JARVIS-ML/QuickReRrun/extras/pickle2-main_reg_less_lrn_epsx.pk','rb')
        pkl=pickle.load(f,encoding="latin1")
        f.close()
        model = pkl.fit(x,y)
        filename=str('pickle_opt_gga_0.pk')
        pickle.dump( model, open( filename, "wb" ) )
        filename=str('joblib_opt_gga_0.jb')
        joblib.dump(model, filename)


def opt_diele_y():
        #df1=pd.read_csv('jv.csv')
        #df2=pd.read_csv('Diel_opt_gga_1.csv')
        #df3=pd.merge(df1,df2,on='jid')
        #x = df3.iloc[:,2:1559].values
        #y = np.sqrt(df3['Diel_opt_gga_1'].values)
        property = 'epsy'
        df2=df[['desc',property]].replace('na',np.nan).dropna()
        x=[]
        y=[]
        max_range=typical_data_ranges[property][1]
        min_range=typical_data_ranges[property][0]
        for i,j in zip(df2['desc'].values,df2[property].values):
           if len(i)==1557 and j!=float('inf') and j>=min_range and j<=max_range:
             x.append(i)
             y.append(j)
        x=np.array(x,dtype='float')
        y=np.array(y,dtype='float')
        print (x.shape)
        print (y.shape)
        print ('property',property)







        lgbm = lgb.LGBMRegressor()
        f=open('/cluster/users/knc6/JARVIS-ML/QuickReRrun/extras/pickle2-main_reg_less_lrn_epsy.pk','rb')
        pkl=pickle.load(f,encoding="latin1")
        f.close()
        model = pkl.fit(x,y)
        filename=str('pickle_opt_gga_1.pk')
        pickle.dump( model, open( filename, "wb" ) )
        filename=str('joblib_opt_gga_1.jb')
        joblib.dump(model, filename)

def opt_diele_z():
        #df1=pd.read_csv('jv.csv')
        #df2=pd.read_csv('Diel_opt_gga_2.csv')
        #df3=pd.merge(df1,df2,on='jid')
        #x = df3.iloc[:,2:1559].values
        #y = np.sqrt(df3['Diel_opt_gga_2'].values)
        property = 'epsz'
        df2=df[['desc',property]].replace('na',np.nan).dropna()
        x=[]
        y=[]
        max_range=typical_data_ranges[property][1]
        min_range=typical_data_ranges[property][0]
        for i,j in zip(df2['desc'].values,df2[property].values):
           if len(i)==1557 and j!=float('inf') and j>=min_range and j<=max_range:
             x.append(i)
             y.append(j)
        x=np.array(x,dtype='float')
        y=np.array(y,dtype='float')
        print (x.shape)
        print (y.shape)
        print ('property',property)








        lgbm = lgb.LGBMRegressor()
        f=open('/cluster/users/knc6/JARVIS-ML/QuickReRrun/extras/pickle2-main_reg_less_lrn_epsz.pk','rb')
        pkl=pickle.load(f,encoding="latin1")
        f.close()
        model = pkl.fit(x,y)
        filename=str('pickle_opt_gga_2.pk')
        pickle.dump( model, open( filename, "wb" ) )
        filename=str('joblib_opt_gga_2.jb')
        joblib.dump(model, filename)



def mbj_diele_x():
        #df1=pd.read_csv('jv.csv')
        #df2=pd.read_csv('Diel_opt_mbj_0.csv')
        #df3=pd.merge(df1,df2,on='jid')
        #x = df3.iloc[:,2:1559].values
        #y = np.sqrt(df3['Diel_opt_mbj_0'].values)
        property = 'mepsx'
        df2=df[['desc',property]].replace('na',np.nan).dropna()
        x=[]
        y=[]
        max_range=typical_data_ranges[property][1]
        min_range=typical_data_ranges[property][0]
        for i,j in zip(df2['desc'].values,df2[property].values):
           if len(i)==1557 and j!=float('inf') and j>=min_range and j<=max_range:
             x.append(i)
             y.append(j)
        x=np.array(x,dtype='float')
        y=np.array(y,dtype='float')
        print (x.shape)
        print (y.shape)
        print ('property',property)









        lgbm = lgb.LGBMRegressor()
        f=open('/cluster/users/knc6/JARVIS-ML/QuickReRrun/extras/pickle2-main_reg_less_lrn_mepsx.pk','rb')
        pkl=pickle.load(f,encoding="latin1")
        f.close()
        model = pkl.fit(x,y)
        filename=str('pickle_opt_mbj_0.pk')
        pickle.dump( model, open( filename, "wb" ) )
        filename=str('joblib_opt_mbj_0.jb')
        joblib.dump(model, filename)


def mbj_diele_y():
        #df1=pd.read_csv('jv.csv')
        #df2=pd.read_csv('Diel_opt_mbj_1.csv')
        #df3=pd.merge(df1,df2,on='jid')
        #x = df3.iloc[:,2:1559].values
        #y = np.sqrt(df3['Diel_opt_mbj_1'].values)
        property = 'mepsy'
        df2=df[['desc',property]].replace('na',np.nan).dropna()
        x=[]
        y=[]
        max_range=typical_data_ranges[property][1]
        min_range=typical_data_ranges[property][0]
        for i,j in zip(df2['desc'].values,df2[property].values):
           if len(i)==1557 and j!=float('inf') and j>=min_range and j<=max_range:
             x.append(i)
             y.append(j)
        x=np.array(x,dtype='float')
        y=np.array(y,dtype='float')
        print (x.shape)
        print (y.shape)
        print ('property',property)






        lgbm = lgb.LGBMRegressor()
        f=open('/cluster/users/knc6/JARVIS-ML/QuickReRrun/extras/pickle2-main_reg_less_lrn_mepsy.pk','rb')
        pkl=pickle.load(f,encoding="latin1")
        f.close()
        model = pkl.fit(x,y)
        filename=str('pickle_opt_mbj_1.pk')
        pickle.dump( model, open( filename, "wb" ) )
        filename=str('joblib_opt_mbj_1.jb')
        joblib.dump(model, filename)

def mbj_diele_z():
        #df1=pd.read_csv('jv.csv')
        #df2=pd.read_csv('Diel_opt_mbj_2.csv')
        #df3=pd.merge(df1,df2,on='jid')
        #x = np.sqrt(df3.iloc[:,2:1559].values)
        #y = df3['Diel_opt_mbj_2'].values
        property = 'mepsz'
        df2=df[['desc',property]].replace('na',np.nan).dropna()
        x=[]
        y=[]
        max_range=typical_data_ranges[property][1]
        min_range=typical_data_ranges[property][0]
        for i,j in zip(df2['desc'].values,df2[property].values):
           if len(i)==1557 and j!=float('inf') and j>=min_range and j<=max_range:
             x.append(i)
             y.append(j)
        x=np.array(x,dtype='float')
        y=np.array(y,dtype='float')
        print (x.shape)
        print (y.shape)
        print ('property',property)





        lgbm = lgb.LGBMRegressor()
        f=open('/cluster/users/knc6/JARVIS-ML/QuickReRrun/extras/pickle2-main_reg_less_lrn_mepsz.pk','rb')
        pkl=pickle.load(f,encoding="latin1")
        f.close()
        model = pkl.fit(x,y)
        filename=str('pickle_opt_mbj_2.pk')
        pickle.dump( model, open( filename, "wb" ) )
        filename=str('joblib_opt_mbj_2.jb')
        joblib.dump(model, filename)


def test():
   f=open('/cluster/users/knc6/JARVIS-ML/QuickReRrun/pickle_form_enp.pk','r')
   pkl = pickle.load(f)
   f.close()
   f=open('/rk2/knc6/DB/ML/JV/JVASP-104.json','r')
   x=json.load(f)
   f.close()
   p = pkl.predict([x])
   print (p)


mbjrelax()
import sys
sys.exit()
opt_diele_x()
kv()
gv()
kpoint()
encut()
optrelax()
form_en()
opt_diele_y()
opt_diele_z()
mbj_diele_x()
mbj_diele_y()
mbj_diele_z()





#test()
#form_en()
#optrelax()
mbjrelax()
#encut()
#kpoint()
#kv()
#gv()

#opt_diele_x()
#opt_diele_y()
#opt_diele_z()
#mbj_diele_x()
#mbj_diele_y()
#mbj_diele_z()
