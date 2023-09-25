import pandas as pd
import numpy as np

def des_epi(epi_df_, ses_labs, C):

    ses1, ses2, ses3 = ses_labs    
    epi_df = epi_df_.copy()

    epi_df['I_ses']=epi_df[C].apply(lambda x: pd.DataFrame(x).groupby(level = 1, axis =1).sum().to_dict())
    epi_df['I_ses1']=epi_df['I_ses'].apply(lambda x: np.array([ _ for _ in x[ses1].values()]).flatten())
    epi_df['I_ses2']=epi_df['I_ses'].apply(lambda x: np.array([ _ for _ in x[ses2].values()]).flatten())
    epi_df['I_ses3']=epi_df['I_ses'].apply(lambda x: np.array([ _ for _ in x[ses3].values()]).flatten())

    res_ses1 = pd.DataFrame(epi_df['I_ses1'].to_list()).describe()
    res_ses2 = pd.DataFrame(epi_df['I_ses2'].to_list()).describe()
    res_ses3 = pd.DataFrame(epi_df['I_ses3'].to_list()).describe()

    return res_ses1, res_ses2, res_ses3


def des_epi_all(epi_df_,C):
    epi_df = epi_df_.copy()

    epi_df['I_ses_all'] = epi_df[C].apply(lambda x: pd.DataFrame(x).sum(axis = 1).to_dict())
    res_ses_all = pd.DataFrame(epi_df['I_ses_all'].to_list()).describe()

    return res_ses_all