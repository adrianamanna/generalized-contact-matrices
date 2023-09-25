import matplotlib.pyplot as plt
import numpy as np

#from utils.epi_tools import *
from utils.LABS import *

ticks_L = range(8)
ticks_L1 = np.arange(1,8*3, 3)
ticks_L2 = np.arange(0,8*3, 1)
L2 = ['1','2','3']*8
L3 = ['1','2','3']


ticks_L3 = np.arange(0,8*3,1)

d_x= 0.085
d_y= 0.1


def plot_d1_matrix(fig, ax, M, pos,cmap='YlGnBu_r'):
    r,c =pos
    box = ax.get_position()
    box.x1 = box.x1+(d_x*c)
    box.x0 = box.x0+(d_x*c)
    box.y1 = box.y1-(d_y*r)
    box.y0 = box.y0-(d_y*r)
    ax.set_position(box)

    ticks_L = range(8)

    contours = ax.imshow(M.values,cmap=cmap)
    ax.invert_yaxis()

   #ax.set_title('$C_{ij}$', loc  = 'left', size = 11)
   # ax.text(0.05,0.88, r'$\rho(C_{ij}):$ '+str(round(eig_leading(M.values),2)),
   #              color = 'w',#'lightgreen',
   #              horizontalalignment='left',
   #              verticalalignment='bottom',
   #              transform=ax.transAxes,fontsize = 10)

    ax.set_yticks(ticks_L)
    ax.set_yticklabels([LAB_AGE[tck] for tck in ticks_L ], fontsize = 8)
    ax.set_xticks(ticks_L)
    ax.set_xticklabels([LAB_AGE[tck] for tck in ticks_L ], fontsize = 8, rotation = 90)
    ax.set_xlabel(r'age class $i$',fontsize = 11)
    ax.set_ylabel(r'age class $j$',fontsize = 11)

    box = ax.get_position()
    cax = fig.add_axes([box.x1+.011, box.y0, .005, box.y1-box.y0])
    fig.colorbar(contours, cax=cax, shrink=0.9)#, ticks = np.arange(0,17,1))# font_size = 10)
    return

def plot_d2_matrix(fig, ax, M, pos,cmap='YlGnBu_r'):
    r,c =pos

    box = ax.get_position()
    box.x1 = box.x1+(d_x*c)
    box.x0 = box.x0+(d_x*c)
    box.y1 = box.y1-(d_y*r)
    box.y0 = box.y0-(d_y*r)
    ax.set_position(box)

    contours = ax.imshow(M.values,cmap=cmap)
    ax.invert_yaxis()

   # ax.text(0.05,0.88, r'$\rho(C_{\alpha\beta}):$ '+str(round(eig_leading(M.values),2)),
   #              color = 'w',#'lightgreen',
   #              horizontalalignment='left',
   #              verticalalignment='bottom',
   #              transform=ax.transAxes,fontsize = 10)

    ax.set_yticks([0,1,2])
    ax.set_yticklabels(L3, fontsize = 8)
    ax.set_xticks([0,1,2])
    ax.set_xticklabels(L3, fontsize = 8)#, rotation = 90)
    ax.set_xlabel(r'dim2 $\alpha$',fontsize = 11)
    ax.set_ylabel(r'dim2 $\beta$',fontsize = 11)

    box = ax.get_position()
    cax = fig.add_axes([box.x1+.011, box.y0, .005, box.y1-box.y0])
    fig.colorbar(contours, cax=cax, shrink=0.9)
    return



def plot_d1d2_matrix(fig, ax, M, pos,cmap='YlGnBu_r'):
    r,c =pos

    box = ax.get_position()
    box.x1 = box.x1+(d_x*c)
    box.x0 = box.x0+(d_x*c)
    box.y1 = box.y1-(d_y*r)
    box.y0 = box.y0-(d_y*r)
    ax.set_position(box)

    contours = ax.imshow(M.values,cmap=cmap)#,norm=LogNorm(vmin=0.05, vmax=30))#vmin = 0, vmax=30)
    ax.invert_yaxis()
    #ax.text(0.05,0.88, r'$\rho(G_{\mathbf{a}\mathbf{b}}):$'+str(round(eig_leading(M.values),2)),
    #             color = 'w',#'lightgreen',
    #             horizontalalignment='left', verticalalignment='bottom',transform=ax.transAxes,fontsize = 10)
    
    ax.set_yticks(ticks_L1)
    ax.set_yticklabels([LAB_AGE[it]+r'   ' for it,tck in enumerate(ticks_L1) ], fontsize = 8)
    ax.set_xticks(ticks_L1)
    ax.set_xticklabels([LAB_AGE[it]+r'   '  for it,tck in enumerate(ticks_L1) ], fontsize = 8, rotation = 90)
    ax.xaxis.set_ticks_position('none') 
    ax.yaxis.set_ticks_position('none') 

    #ax.set_title('$ G_{\mathbf{a}\mathbf{b}}$', loc = 'left', size = 11)
    ax.set_ylabel(r'age class $j$, dim2 $\beta$',fontsize = 11)
    ax.set_xlabel(r'age class $i$, dim2 $\alpha$',fontsize = 11)

    box = ax.get_position()
    cax = fig.add_axes([box.x1+.011, box.y0, .005, box.y1-box.y0])
    fig.colorbar(contours, cax=cax, shrink=0.5)#, ticks = np.arange(0,17,1))# font_size = 10)
        
    cax = fig.add_axes(box)
    contours = cax.imshow(M.values,cmap=cmap, alpha = 0)#,norm=LogNorm(vmin=0.05, vmax=30))#vmin = 0, vmax=30)
    cax.invert_yaxis()
    cax.set_yticks(ticks_L2)
    cax.set_yticklabels(L2, fontsize = 5)
    cax.set_xticks(ticks_L2)
    cax.set_xticklabels(L2, fontsize = 5)
    cax.set(facecolor = 'none')
    
    
    return


ticks_L1_d3 = np.arange(5,8*3*3, 3*3)
ticks_L3_d3 = np.arange(0,8*3*3, 1)

L2_d3 = ['1  ','2  ','3  ']*8
L3_d3 = ['1','2','3']*8*3


def plot_d1d2d3_matrix(fig, ax, M, M_d1,pos):

    r,c =pos

    box = ax.get_position()
    box.x1 = box.x1+(d_x*c)
    box.x0 = box.x0+(d_x*c)
    box.y1 = box.y1-(d_y*r)
    box.y0 = box.y0-(d_y*r)
    ax.set_position(box)

    contours = ax.imshow(M.values,cmap='YlGnBu_r')
    ax.invert_yaxis()
    ax.set_yticks(ticks_L1_d3)
    ax.set_yticklabels([LAB_AGE[it]+r'     ' for it,tck in enumerate(ticks_L1_d3) ], fontsize = 8)
    ax.set_xticks(ticks_L1_d3)
    ax.set_xticklabels([LAB_AGE[it]+r'     '  for it,tck in enumerate(ticks_L1_d3) ], fontsize = 8, rotation = 90)
    ax.xaxis.set_ticks_position('none') 
    ax.yaxis.set_ticks_position('none') 

    ax.set_ylabel(r'age class $j$, dim2 $\beta$, dim3 $\delta$',fontsize = 11)
    ax.set_xlabel(r'age class $i$, dim2 $\alpha$, dim3 $\gamma$',fontsize = 11)

    #ax.text(0.05,0.88, r'$\rho(G_{\mathbf{a}\mathbf{b}}):$'+str(round(eig_leading(M.values),2)),
    #             color = 'w',#'lightgreen',
    #             horizontalalignment='left',
    #             verticalalignment='bottom',
    #             transform=ax.transAxes,fontsize = 10)
    

 

    cax = fig.add_axes([box.x1+.011, box.y0, .005, box.y1-box.y0])
    fig.colorbar(contours, cax=cax, shrink=0.9)#, ticks = np.arange(0,17,1))# font_size = 10)

    cax = fig.add_axes(box)
    contours = cax.imshow(M_d1.values,cmap='YlGnBu_r', alpha = 0)
    cax.set_yticks(ticks_L2)
    cax.set_yticklabels(L2_d3, fontsize = 5.5)
    cax.set_xticks(ticks_L2)
    cax.set_xticklabels(L2_d3, fontsize = 5.5, rotation =90)
    cax.set(facecolor = 'none')
    cax.xaxis.set_ticks_position('none') 
    cax.yaxis.set_ticks_position('none') 

    for pos in ['top', 'right', 'left', 'bottom']:
        cax.spines[pos].set_visible(False)

    cax = fig.add_axes(box)
    contours = cax.imshow(M.values,cmap='YlGnBu_r', alpha = 0)
    cax.set_yticks(ticks_L3_d3)
    cax.set_yticklabels(L3_d3, fontsize = 2.2)
    cax.set_xticks(ticks_L3_d3)
    cax.set_xticklabels(L3_d3, fontsize = 2.2, rotation =90)
    cax.set(facecolor = 'none')


    for pos in ['top', 'right', 'left', 'bottom']:
        cax.spines[pos].set_visible(False)

    return