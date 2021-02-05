import sklearn as sk
import pandas as pd
from sklearn.metrics import mean_squared_error, accuracy_score
import numpy as np 

def get_score(file_path_ref,file_path_sub,is_classification=False):
    print(file_path_ref)
    print(file_path_sub)
    df_ref = pd.read_csv(file_path_ref,header=None)
    df_sub = pd.read_csv(file_path_sub,header=None)
    if is_classification:
        res = 1-accuracy_score(df_ref[0],df_sub[0],normalize=True)
    else:
        res =  np.sqrt(mean_squared_error(df_ref[0],df_sub[0]))
    return res
    
