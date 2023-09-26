from utils.SEIR import *
from utils.epi_tools import *
import yaml
import pickle
import os

if not os.path.exists("./res/epi"):
    os.makedirs("./res/epi")


if __name__== '__main__':
    print('running epidemic')

with open("./config_matrix.yaml", "rb") as fp:
    config_mat=yaml.load(fp, Loader=yaml.SafeLoader)

with open("./config_epi.yaml", "rb") as fp:
    config=yaml.load(fp, Loader=yaml.SafeLoader)

with open(f'./res/matrices/Ms_'+config_mat['mixing_type']+'.pkl',  'rb') as f:
    Ms= pickle.load(f)

with open('./res/population/Ns.pkl',  'rb') as f:
    Ns= pickle.load(f)



#. init matrices
M_d1_tot, M_d1 = Ms['tot_d1'],Ms['d1']
M_d2_tot, M_d2 = Ms['tot_d2'],Ms['d2']
M_d1d2_tot, M_d1d2 = Ms['tot_d1d2'],Ms['d1d2']

#. init population distributions
N_d1 = Ns['d1']
N_d2  = Ns['d2']
N_d1d2= Ns['d1d2']

lev_d1= np.unique([ _[0] for _ in list(N_d1d2.keys())])
lev_d2= np.unique([ _[1] for _ in list(N_d1d2.keys())])

#. computing beta
TAB = pd.DataFrame(M_d1d2).copy() 
beta_val_d1d2 = get_beta(TAB, config['r0'], config['mu_val'])
print('beta:', beta_val_d1d2)

# M3 model with Md1d2
print('Model d1d2')
results =[]
key_seed_d1d2_list = [(np.random.choice(lev_d1),np.random.choice(lev_d2)) for _ in range(config['N_iter'])]

for key_seed_d1d2 in key_seed_d1d2_list:
    results.append(run_epi(N_d1d2,
    key_seed_d1d2,
    config['seed'],
    M_d1d2,
    beta_val_d1d2,
    config['mu_val'],
    config['eps_val'],
    config['stop'],
    False,
    None,
    None))

RES = pd.DataFrame(results)
RES.columns=['S', 'E', 'I', 'R', 't', 'new_I']
with open('./res/epi/epi_M3.pkl', 'wb') as handle:
    pickle.dump(RES, handle)

del RES
del results

# M1 model with Md1
print('Model d1')
results =[]
key_seed_d1_list = [np.random.choice(lev_d1) for _ in range(config['N_iter'])]
for key_seed_d1 in key_seed_d1_list:
    results.append(run_epi(N_d1,
    key_seed_d1,
    config['seed'],
    M_d1,
    beta_val_d1d2,
    config['mu_val'],
    config['eps_val'],
    config['stop'],
    False,
    None,
    None))

RES = pd.DataFrame(results)
RES.columns=['S', 'E', 'I', 'R', 't','new_I']
with open('./res/epi/epi_M1.pkl', 'wb') as handle:
    pickle.dump(RES, handle)
del RES
del results


# M2 model with Md2
print('Model d2')
results =[]

key_seed_d2_list = [np.random.choice(lev_d2) for _ in range(config['N_iter'])]
for key_seed_d2 in key_seed_d2_list:
    results.append(run_epi(N_d2,
    key_seed_d2,
    config['seed'],
    M_d2,
    beta_val_d1d2,
    config['mu_val'],
    config['eps_val'],
    config['stop'],
    False,
    None,
    None))
    
RES = pd.DataFrame(results)
RES.columns=['S', 'E', 'I', 'R', 't','new_I']
with open('./res/epi/epi_M2.pkl', 'wb') as handle:
    pickle.dump(RES, handle)

del RES
del results


if __name__== '__main__':
    print('DONE')