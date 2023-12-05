from jarvis.ai.pkgs.lgbm.regression import parameters_dict
from scipy.stats import median_absolute_deviation as mad
from jarvis.ai.pkgs.utils import get_ml_data
import lightgbm as lgb
import numpy as np
from sklearn.model_selection import train_test_split
from jarvis.ai.pkgs.utils import regr_scores
import joblib

params = parameters_dict()

print (params)



mem=[]
for i,j in params.items():
    name=str(i)+'.pkl'
    print (i)
    print (name)
    X,y,jid=get_ml_data(dataset="cfid_3d", ml_property=i)
    lgbm = lgb.LGBMRegressor(n_estimators= j['n_estimators'],learning_rate= j['learning_rate'],num_leaves= j['num_leaves'])
    if 'eps' in i:#fit refractive index, not dielectric constant
      y=np.sqrt(y)
    X_train, X_test, y_train, y_test, jid_train, jid_test = train_test_split(X, y, jid, random_state=1, test_size=.1)
    lgbm.fit(X_train,y_train)
    pred = lgbm.predict(X_test)
    joblib.dump(lgbm, name)
    reg_sc = regr_scores(y_test, pred)
    mae=reg_sc['mae'] #mean absolute error
    madev=mad(y) #mean absolute deviation
    #mae_over_madev=float(mae)/float(madev)
    mem.append([i,len(X),mae,madev])
    print ('Property,Length, MAE,MAD', i,len(X),mae,madev)
    print ()
    print ()

