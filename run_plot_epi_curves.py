import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 11, 'font.style': 'normal', 'font.family':'serif'})

from utils.LABS import *
from utils.data_tools import *

import pickle
import os


if not os.path.exists("./_figs"):
    os.makedirs("./figs")


#. uploading data
with open('./res/epi/epi_M1.pkl',  'rb') as f:
    epi_M1 =pickle.load(f)

with open('./res/epi/epi_M2.pkl',  'rb') as f:
    epi_M2 =pickle.load(f)
    
with open('./res/epi/epi_M3.pkl',  'rb') as f:
    epi_M3 =pickle.load(f)

with open('./res/population/Ns.pkl',  'rb') as f:
    Ns= pickle.load(f)


#. data manipulation
N_pop= Ns['N_pop']
N_d2= Ns['d2']

I_M1= des_epi_all(epi_M1,'I').T
I_M2= des_epi_all(epi_M2,'I').T
I_M3= des_epi_all(epi_M3,'I').T

res_epi_ses = des_epi(epi_M3, [0,1,2], 'I')


#. init labs and colors
colors =['#1b9e77','#d95f02','#7570b3']
cs_M = ['#1b9e77', 'grey','darkred']
labs_M = [r'w/$G_{\mathbf{a}\mathbf{b}}$', r'w/$C_{ij}$', r'w/$C_{\alpha \beta}$']


#. plottinng
fig, axs = plt.subplots(1, 2, figsize =(3.4*2, 2.4*1), sharey= True)
ax=axs[0]
ax.set_title('By dimention ('+ r'w/$G_{\mathbf{a}\mathbf{b}}$'+')')
ax.set_xlabel('time',fontsize = 11)
ax.set_ylabel('% infected',fontsize = 11)

for _,res in enumerate(res_epi_ses):
    res =res.T.copy()
    y  = res['50%']/N_d2[_]
    y1 = res['25%']/N_d2[_]
    y2 = res['75%']/N_d2[_]
    x = range(len(y))

    ax.plot(x, y,lw =1.2, ls = '-', c = colors[_], alpha = 1, label = LAB_SES_sy[_]) 
    ax.fill_between(x, y1, y2,color = colors[_], alpha = 0.25)
ax.legend(loc = 'lower right', frameon = False,fontsize=11, title = 'dim2',columnspacing=0.5, handletextpad=0.1, labelspacing=0.1)

ax=axs[1]
ax.set_title('Overall')
ax.set_xlabel('time',fontsize = 11)
for i, I in enumerate([I_M3, I_M1, I_M2]):
    y, y_l, y_u = I['mean']/N_pop, I['25%']/N_pop , I['75%']/N_pop
    x = range(len(y))
    ax.plot(x,y, lw =0.9, ls = '-',  c = cs_M[i], alpha = 0.9, label = labs_M[i]) 
    ax.fill_between(x,y_l, y_u, color = cs_M[i], alpha = 0.15)
ax.legend(loc = 'upper right', frameon = False,fontsize=11,columnspacing=0.5, handletextpad=0.1, labelspacing=0.1)

plt.savefig('./figs/epi_curves.pdf', bbox_inches = 'tight',  transparent=True)