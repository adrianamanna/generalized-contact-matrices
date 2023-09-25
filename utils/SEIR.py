import numpy as np
import pandas as pd


def run_epi(pop,key_seed,
            seeds:int, M,
            beta_val:float,
            mu_val:float, 
            eps_val:float, 
            stop:int, NPI=False, M_npi=None, T_npi=None):
    '''
    pop: population vecotr
         dict {key: pop_key}
         
    key_seed: key of the infected compartment at time 0
              touple/int
    
    seeds: number of infected individuald at time I0
           int
    M:   contact matrix
         dict {key:{key1:c_val, key2:c_val}}
    
    beta_val: infection probability 
    mu_val:   recovery rate (1/d , d:generation time)
    eps_val:  probability to become infectious
    
    stop:   number of timesteps to simulate
    '''
    #. set initial compartments
    #  compartment = [var1,var2][time]
    S,E,I,R = {},{},{},{}
    I_new_ ={}
    
    for i,key in enumerate(pop):        
            
        S.setdefault(key,{})
        E.setdefault(key,{})
        I.setdefault(key,{})
        R.setdefault(key,{})

        I_new_.setdefault(key,{})
        
        if key == key_seed:
            Ii = seeds
        else:
            Ii = 0

   
        S[key][0]= pop[key] - Ii
        E[key][0]= 0
        I[key][0]= Ii
        R[key][0]= 0

        I_new_[key][0]= Ii
    
    # . controlli
    keys  = pop.keys()
    keys1 = M.keys()
    
    if keys!= keys1:
        raise 'Population vector and Contact matrix must have same keys!'

    # . running the epidemic
    for t in range(1,stop):
        if NPI == True:
            if t > T_npi:
                M= M_npi.copy()
        #print('t_{} '.format(t), end = '\r')        
        
        for m_key in keys:
            
            C_key = M[m_key]
            cc = []
            for kc in C_key:
                cc.append(C_key[kc]*(I[kc][t-1]/pop[kc]))

            lambda_val = beta_val*sum(cc)
            

            new_E = np.random.binomial(S[m_key][t-1] ,1.-np.exp(-lambda_val))
            new_I = np.random.binomial(E[m_key][t-1] , eps_val)
            new_R = np.random.binomial(I[m_key][t-1] , mu_val)                
                
            S[m_key][t] =  S[m_key][t-1] -  new_E
            E[m_key][t] =  E[m_key][t-1] +  new_E -  new_I
            
            I[m_key][t] =  I[m_key][t-1] +  new_I -  new_R
            R[m_key][t] =  R[m_key][t-1] +  new_R


            I_new_[m_key][t] = new_I
        
        totI = sum([I[key][t] for key in keys])
        
        #if (t >300) and (totI < 1):
        #    break
                 
    return S,E, I,R, t, I_new_


# Accounting for stoch and groupping 
#----------------------------------------
#def group_C(C):
#   C_d1 = pd.DataFrame(C).T.groupby(level=[0]).sum().T
#    C_d2 = pd.DataFrame(C).T.groupby(level=[1]).sum().T
#    return C_d1, C_d2

def group_C(C, max_dim):
    C_d = []
    for i in range(max_dim):
        C_d.append(pd.DataFrame(C).T.groupby(level=[i]).sum().T)
    return C_d


def M1_stoc_ar(n_dim1, N_iter,N_d1, seed, M_d1, beta_val_d1,   mu_val, eps_val, stop):
    ARs, ARs_age = [],[]
    N= sum(N_d1.values())
     
    for iter_ in range(N_iter):
        print('        M1-iter:', iter_,end = '\r')
        key_seed_d1 = np.random.choice(list(N_d1.keys()))#np.random.randint(n_dim1)
        S_M1, E_M1, I_M1, R_M1, t1 , new_I_M1=  run_epi(  N_d1, 
                                                key_seed_d1, 
                                                seed, 
                                                M_d1,   
                                                beta_val_d1,   
                                                mu_val, 
                                                eps_val, 
                                                stop)
        
        #. overall
        R_T =pd.DataFrame(R_M1).sum(axis = 1)[t1]
        AR = R_T/N
        ARs.append(AR)
        
        # . by age
        R_Tage = dict(pd.DataFrame(R_M1).loc[t1])
        AR_age = {key:R_Tage[key]/N_d1[key] for key in R_Tage}
        ARs_age.append(AR_age)
    return ARs, ARs_age


def M2_stoc_ar(n_dim1, n_dim2,N_d1,N_d2,N_iter,N_d1d2, seed, M_d1d2,  beta_val_d1d2, mu_val, eps_val, stop): 
    N= sum(N_d1.values())
    ARs, ARs_age, ARs_dim2 = [],[],[]

    lev_d1= np.unique([ _[0] for _ in list(N_d1d2.keys())])
    lev_d2= np.unique([ _[1] for _ in list(N_d1d2.keys())])

    for iter_ in range(N_iter):
        print('        M2-iter:', iter_,end = '\r')
        key_seed_d1d2 = (np.random.choice(lev_d1),np.random.choice(lev_d2))
        S_M2, E_M2, I_M2, R_M2, t2, new_I_M2 =  run_epi(N_d1d2 ,
                                              key_seed_d1d2,
                                              seed, M_d1d2,
                                              beta_val_d1d2,
                                              mu_val,
                                              eps_val,
                                              stop)

        #. overall 
        R_T =pd.DataFrame(R_M2).sum(axis = 1)[t2]
        AR = R_T/N
        ARs.append(AR)


        #. grouping
        Rd1_M2, Rd2_M2 = group_C(R_M2,2)

        #. by age
        R_Tage = dict(Rd1_M2.iloc[t2])
        AR_age = {key:R_Tage[key]/N_d1[key] for key in R_Tage}
        ARs_age.append(AR_age)

        #. by dim1
        R_Tdim2 = dict(Rd2_M2.iloc[t2])
        AR_dim2 = {key:R_Tdim2[key]/N_d2[key] for key in R_Tdim2}
        ARs_dim2.append(AR_dim2)
        
    return ARs, ARs_age, ARs_dim2






def M3_stoc_ar(n_dim1, n_dim2,n_dim3,N_d1,N_d2,N_d3,N_iter,N_d1d2d3, seed, M_d1d2d3,  beta_val_d1d2d3, mu_val, eps_val, stop):
    
    N= sum(N_d1.values())
    ARs, ARs_age, ARs_dim2,ARs_dim3= [],[],[],[]

    for iter_ in range(N_iter):
        print('        M3-iter:', iter_,end = '\r')
        key_seed_d1d2d3 = (np.random.randint(n_dim1),np.random.randint(n_dim2),np.random.randint(n_dim3))
        
        S_M3, E_M3, I_M3, R_M3, t3, new_I_M3 =  run_epi(N_d1d2d3 ,
                                              key_seed_d1d2d3,
                                              seed, M_d1d2d3,
                                              beta_val_d1d2d3,
                                              mu_val,
                                              eps_val,
                                              stop)

        #. overall 
        R_T =pd.DataFrame(R_M3).sum(axis = 1)[t3]
        AR = R_T/N
        ARs.append(AR)


        #. grouping
        Rd1_M3, Rd2_M3, Rd3_M3 = group_C(R_M3,3)

        #. by age
        R_Tage = dict(Rd1_M3.iloc[t3])
        AR_age = {key:R_Tage[key]/N_d1[key] for key in R_Tage}
        ARs_age.append(AR_age)

        #. by dim2
        R_Tdim2 = dict(Rd2_M3.iloc[t3])
        AR_dim2 = {key:R_Tdim2[key]/N_d2[key] for key in R_Tdim2}
        ARs_dim2.append(AR_dim2)
        
        
        # by dim3 
        R_Tdim3 = dict(Rd3_M3.iloc[t3])
        AR_dim3 = {key:R_Tdim3[key]/N_d3[key] for key in R_Tdim3}
        ARs_dim3.append(AR_dim3)
        
    return ARs, ARs_age, ARs_dim2,ARs_dim3

#---- 




def M1_stoc(n_dim1, N_iter,N_d1, seed, M_d1, beta_val_d1,   mu_val, eps_val, stop):

    S_M1_s, E_M1_s, I_M1_s, R_M1_s = {},{},{},{}

    for iter_ in range(N_iter):
        print('        iter:', iter_,end = '\r')
        key_seed_d1 = np.random.randint(n_dim1)
        S_M1, E_M1, I_M1, R_M1, t1 =  run_epi(N_d1, key_seed_d1, seed, M_d1,    beta_val_d1,   mu_val, eps_val, stop)

        #if S_M1[0][t2-1] != S_M1[0][0]: 
        S_M1_s[iter_] = S_M1
        E_M1_s[iter_] = E_M1
        I_M1_s[iter_] = I_M1
        R_M1_s[iter_] = R_M1
    
    RES_M1 = [S_M1_s, E_M1_s, I_M1_s, R_M1_s]

    return RES_M1


def M2_stoc(n_dim1, n_dim2, N_iter,N_d1d2, seed, M_d1d2,  beta_val_d1d2, mu_val, eps_val, stop):
    
    Sd1_M2_s, Ed1_M2_s, Id1_M2_s, Rd1_M2_s = {},{},{},{}
    Sd2_M2_s, Ed2_M2_s, Id2_M2_s, Rd2_M2_s = {},{},{},{}

    for iter_ in range(N_iter):
        print('        iter:', iter_,end = '\r')
        key_seed_d1d2 = (np.random.randint(n_dim1),np.random.randint(n_dim2))
        S_M2, E_M2, I_M2, R_M2, t2 =  run_epi(N_d1d2 , key_seed_d1d2, seed, M_d1d2,  beta_val_d1d2, mu_val, eps_val, stop)
                    
        Sd1_M2, Sd2_M2 = group_C(S_M2)
        Ed1_M2, Ed2_M2 = group_C(E_M2)
        Id1_M2, Id2_M2 = group_C(I_M2)
        Rd1_M2, Rd2_M2 = group_C(R_M2)

        #if Sd1_M2[0][t1-1] != Sd1_M2[0][0]:  #<- not consider when epi didn't started

        Sd1_M2_s[iter_] = Sd1_M2
        Ed1_M2_s[iter_] = Ed1_M2
        Id1_M2_s[iter_] = Id1_M2
        Rd1_M2_s[iter_] = Rd1_M2

        Sd2_M2_s[iter_] = Sd2_M2
        Ed2_M2_s[iter_] = Ed2_M2
        Id2_M2_s[iter_] = Id2_M2
        Rd2_M2_s[iter_] = Rd2_M2
            
    RESd1_M2 = [Sd1_M2_s, Ed1_M2_s, Id1_M2_s, Rd1_M2_s]
    RESd2_M2 = [Sd2_M2_s, Ed2_M2_s, Id2_M2_s, Rd2_M2_s]
    
    return RESd1_M2, RESd2_M2