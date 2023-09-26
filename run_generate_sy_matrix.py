import numpy as np
import pandas as pd
import yaml
import pickle
import os

from utils.matrix_tools_sy import *
from copy import deepcopy

if not os.path.exists("./res"):
    os.makedirs("./res")
    os.makedirs("./res/matrices")
    os.makedirs("./res/population")

with open("./config_matrix.yaml", "rb") as fp:
    config=yaml.load(fp, Loader=yaml.SafeLoader)

if __name__== '__main__':
    print(config)


#.data
data = pd.read_pickle('./data/data.pkl')

P_d1, N_pop,  M_d1 , M_d1_tot = get_Pd1_Md1(data, config['country'])
P_d1d2 = get_P_d1d2(P_d1,config['n_dim2'],config['dist_Pd2'])
P_d2 =  {key: config['dist_Pd2'][key] for key in range(len(config['dist_Pd2']))}

N_d1 = {key: P_d1[key]*N_pop for key in P_d1.keys()}
N_d2 = {key: config['dist_Pd2'][key]*N_pop for key in range(len(config['dist_Pd2']))}
N_d1d2 = {key: P_d1d2[key]*N_pop for key in P_d1d2.keys()}

Ps_dict ={'d1': P_d1,'d2': P_d2,'d1d2': P_d1d2}
Ns_dict ={'d1': N_d1,'d2': N_d2,'d1d2': N_d1d2, 'N_pop':N_pop}




    
with open("./res/population/Ps.pkl", 'wb') as handle:
     pickle.dump(Ps_dict, handle)
        
with open("./res/population/Ns.pkl", 'wb') as handle:
    pickle.dump(Ns_dict, handle)



# assortative splitting
if config['mixing_type']== 'assortative_mixing':
    m_diag, m_off_diag=assortative_mixing(config['r'],config['activity'], config['ds'])

    if np.any(np.array(m_diag)<0) or np.any(np.array(m_off_diag)<0):
        raise ValueError(f'Non-physical solution:: negative values in the ASS matrices \n:{m_diag, m_off_diag}')
    
else:
    m = random_mixing(config['dist_Pd2'])
    m_diag, m_off_diag =m.copy(), m.copy()



M_d1d2_tot, M_d1d2 = get_M_d1d2(M_d1_tot, config['n_dim2'], N_d1d2, m_diag, m_off_diag)

M_d1_tot, M_d1 = get_C_from_G_sy(M_d1d2_tot,N_d1, 'd1')
M_d2_tot, M_d2 = get_C_from_G_sy(M_d1d2_tot,N_d2, 'd2')


Ms ={ 'd1': M_d1,    'tot_d1': M_d1_tot,
      'd2': M_d2,    'tot_d2': M_d2_tot,
      'd1d2': M_d1d2,'tot_d1d2': M_d1d2_tot}
    
with open('./res/matrices/Ms_{}.pkl'.format(config['mixing_type']), 'wb') as handle:
    pickle.dump(Ms, handle)


