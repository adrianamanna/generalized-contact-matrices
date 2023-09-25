from utils.plot_matrices import *
import pickle
import yaml
import pandas as pd
import os

plt.rcParams.update({'font.size': 11, 'font.style': 'normal', 'font.family':'serif'})

if not os.path.exists("./_figs"):
    os.makedirs("./figs")

with open("./config_matrix.yaml", "rb") as fp:
    config=yaml.load(fp, Loader=yaml.SafeLoader)

with open(f'./res/matrices/Ms_'+config['mixing_type']+'.pkl',  'rb') as f:
    Ms= pickle.load(f)

M_d1_tot, M_d1 = Ms['tot_d1'],Ms['d1']
M_d2_tot, M_d2 = Ms['tot_d2'],Ms['d2']
M_d1d2_tot, M_d1d2 = Ms['tot_d1d2'],Ms['d1d2']


nrows,ncols=1,3
fig, axs = plt.subplots(nrows, ncols, figsize =(3.3*ncols, 3*nrows))

plot_d1_matrix(fig,axs[0], pd.DataFrame(M_d1).copy(),(0,0),cmap='YlGnBu_r')
plot_d2_matrix(fig,axs[1], pd.DataFrame(M_d2).copy(),(0,1),cmap='YlGnBu_r')
plot_d1d2_matrix(fig,axs[2], pd.DataFrame(M_d1d2).copy(),(0,2),cmap='YlGnBu_r')

plt.savefig('./figs/matrices.pdf', bbox_inches = 'tight',  transparent=True)
