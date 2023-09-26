# Generalized contact matrices for epidemic modeling


## I. CONTENT 

- **config_matrix.yaml**: configuration file to run the script run_generate_sy_matrix.
- **config_epi.yaml**: configuration file to run the script run_epi.

- **run_generate_sy_matrix.py**: phyton script to build generalized contact matrices starting from an age contact matrix.
- **run_epi.py**: phyton script to simulate a SEIR model. Implementing:
    - i. age-contact matrices ($C_{ij}$).
    - ii. dim2 - contact matrices ($C_{\alpha\beta}$).
    - iii. generalized contact matrices stratified by age and dim 2 ($G_{\math{a}\math{b}}$).

- **run_plot_matrices.py**: phyton script to plot the three matrices.
- **run_plot_epi_curves.py**: phyton script to process and plot the results of the epidemic simulations.

In the **data** folder:
- data.pkl
    - 'country': name of the country
    - 'N': population distribution by age classes as in the survey. 
    - 'M': age-contact matrix
    - 'tot_N_pop': total population in the country


In the **utils**:
- *data_tools.py*: functions to manipulate the output of the epidemic simulations 
- *epi_tools.py*: functions to compute the eigenvalue and the beta given the R0 and the contact matrix
- *LABS.py*: lists of labels
- *matrix_tools.py*: functions to build the synthetic generalized contact matrix
- *plot_matrices.py*: functions to plot the contact matrices
- *SEIR.py*: epidemiological model


The code will create the following paths: 
- *'./res/matrices'*: where it stores the matrices,
- *'./res/population'*: where it stores the populations distributions,
- *'./res/epi'*: where it stores the results of the epidemic,
- *'./fig'*: where it stores the figures.



## II. INSTRUCTIONS

### STEP 1: BUILD THE GENERALIZED AGE-CONTACT MATRICES

1. In the config_matrix.yaml you can set the parameters to build the generalized contact matrix starting from the age-contact matrix of a given country. The parameters you can set are the following:
    - `country`: the country can be selected among the following: Zimbabwe - Peru - Vietnam - Hungary
    - `dist_Pd2`: distribution of the population in the three levels of the second dimension
    - `mixing_type`: random_mixing or assortative_mixing
    
    if \textt{assortative_mixing} is selected:
        - `r`: assortativity of each group
        - `ds`: 
        - `activity`: relative activity of each group (has to sum up to 1)



2. Run 'python run_generate_sy_matrix.py' This script computes and stores the generalized contact matrix in the 'res/matrices' folder.

3. Run 'python run_plot_matrices.py' This script plots the decoupled matrices and stores the figures in the 'figs' folder.



### STEP 2: SIMULATE THE EPIDEMIC

1. In the config_epi.yaml you can set the epidemiological parameter.
    - `N_iter`: number of iterations
    - `seed`: number of initial infected individuals
    - `mu_val`: recovery rate
    - `eps_val`: incubation rate
    - `stop`: number of times steps to run 
    - `r0`: basic reproductive number

2. Run 'python run_epi.py' This script runs the simulations of the epidemic model and stores the results in the 'res/epi' folder.

3. Run 'python run_plot_epi.py' This script processes the output of the simulation and plots the infection curves. The plot is then stored in the 'figs' folder.


________________________

## SIV. PACKAGES VERSIONS**

json5                     0.9.6              pyhd3eb1b0_0  
matplotlib                3.5.2            py39h06a4308_0  
matplotlib-base           3.5.2            py39hf590b9c_0  
matplotlib-inline         0.1.6            py39h06a4308_0  
numpy                     1.21.5           py39h6c91a56_3  
numpy-base                1.21.5           py39ha15fc14_3 
pandas                    1.4.4            py39h6a678d5_0   
pickleshare               0.7.5           pyhd3eb1b0_1003  
scipy                     1.9.1            py39h14f4228_0  
yaml                      0.2.5                h7b6447c_0 

________________________

- The installation on a normal desktop computer requires less than a minute.
- The installation does not require any non-standard hardware.

________________________

Link to the arxive https://doi.org/10.48550/arXiv.2306.17250



 

