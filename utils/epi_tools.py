#import numpy as np
#import pandas as pd
import scipy.linalg as la

#from utils.SEIR import *


def eig_leading(M):
    eigvals, eigvecs = la.eig(M)
    leading=max(eigvals.real)#.real[0]
    return leading

def get_beta(M,R0, mu_val):
    eigvals, eigvecs = la.eig(M)
    leading=eigvals.real[0]
    
    beta_val=mu_val*R0/(leading)
    return beta_val







