#! /usr/bin/env python3

import pyblock
import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt

c = 627.503   # Ha to kcal/mol
#c = 27.21138505 * 1e3  # Ha to meV

ntaus = ['0.3','0.25','0.2','0.16','0.13','0.10',
         '0.08','0.06','0.05','0.04','0.03','0.02','0.01',
         '0.006','0.003'] 
taus = [ float(tau) for tau in ntaus ]

print( f'Timesteps: {taus}' ) 

systs = [ 'Mol_AcOH_20_1/DLTM' ]

Dmethods = {}
Dmethods['dltm5_Jopt_']        = 'DLTM_lim5_Jopt'
methods = list( Dmethods.keys() )


DATA='/Users/zen/Dropbox/WORK/2021_S66/DATA_Flaviano'

for isyst, syst in enumerate(systs):
    print(f'{isyst}: System {syst}')
    for method in methods:
        datadir_notau = f'{DATA}/{syst}/DMC{method}'
        print(f'\n*** {method}  {datadir_notau}TAU ***')
        res = {}
        for i, tau in enumerate(taus):
            dmcdir = f'{datadir_notau}{ntaus[i]}'
            filename = f'{dmcdir}/dmc.hist'
            try:
                dmc = np.loadtxt( filename )
                equilibration = int(10.0 / tau)
                data = dmc[equilibration:,3]   # Eloc is on 4th colums, so number 3 for python
                reblock_data = pyblock.blocking.reblock( data )
                opt = pyblock.blocking.find_optimal_block( len(data), reblock_data )
                #print(f'  {syst} ',reblock_data[opt[0]])
                block_size = 2**reblock_data[opt[0]][0]
                energy = reblock_data[0][2]   # use all data
                energy_error = reblock_data[opt[0]][4]
                energy_error_error = reblock_data[opt[0]][5]
                print(f'{tau:8.5f} \t {energy} \t {energy_error} \t {energy_error_error}')
                if ( energy_error < 1.e-1 ):
                    res[tau] = { 'ene': energy, 'err': energy_error }
                else:
                    print(f'Error is too large for tau={tau} in {filename}!')
            except:
                print(f'     Error with {tau}, file {filename}')
                #break
        df = pd.DataFrame( res ).T
        df.sort_index(inplace=True, ascending=False)
        #print(df)
        #s = syst.split('/')[0]
        s = 'A'
        df.to_csv(f'energy_{s}_{Dmethods[method]}.csv', header=False)

