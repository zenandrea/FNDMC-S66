#! /usr/bin/env python3

import os
import pyblock
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

makeplot = True 
viewplot = False # makeplot
verbose = False

c = 627.503   # Ha to kcal/mol
#c = 27.21138505 * 1e3  # Ha to meV


systs = [ 'AB', 'A' ]
dim = systs[0]
Nmol = len(systs)-1
print('Nmol = ',Nmol)

Dmethods = {}
Dmethods['tm5_JoptLA_']  = 'TM_lim5_JoptLA'
Dmethods['tm5_']         = 'TM_lim5_Jopt'
Dmethods['dla5_']        = 'DLA_lim5_Jdim'
Dmethods['dla5_Jopt_']   = 'DLA_lim5_Jopt'

methods = list( Dmethods.keys() )

if os.path.isdir('./EneDiff'):
    pass
elif os.path.isfile('./EneDiff'):
    print('WARNING: ./EneDiff is a file! Exit')
    exit
else:
    print('WARNING: creating the directory ./EneDiff')
    os.mkdir( './EneDiff' )

for method in methods:
  try:
    print(f'*** {Dmethods[method]} : {method}')
    dfs = {}
    for s in systs:
      csvfile = f'energy_{s}_{Dmethods[method]}.csv'
      if (method=='dla5_' and s=='AB'): csvfile = f'energy_AB_DLA_lim5_Jopt.csv'
      print( f'> method={method} s={s} : Reading {csvfile}' )
      if os.path.isfile( csvfile ):
        dfs[s] = pd.read_csv( csvfile, names=['tau','ene','err'], decimal='.', header=None, index_col='tau')  
        if verbose: print( dfs[s] )
      else:
        dfs[s] = pd.DataFrame({},columns=['tau','ene','err'])
    if (Nmol == 1):
        mon = systs[1]
        Eb     = c * ( dfs[dim].ene - 2 * dfs[mon].ene )
        Eb_err = c * ( dfs[dim].err**2  + 4 * dfs[mon].err**2 )**0.5
    elif (Nmol == 2):
        mon1 = systs[1]
        mon2 = systs[2]
        Eb     = c * ( dfs[dim].ene - dfs[mon1].ene - dfs[mon2].ene )
        Eb_err = c * ( dfs[dim].err**2  + dfs[mon1].err**2 + dfs[mon2].err**2 )**0.5
    df_Eb = pd.DataFrame([Eb, Eb_err]).T
    df_Eb.sort_index(inplace=True, ascending=False)
    df_Eb.dropna(axis = 0, inplace=True)
    print(f'Binding Energy {Dmethods[method]}:\n{df_Eb}\n' )
    if len( df_Eb ) > 0:
        df_Eb.to_csv( f'EneDiff/Eb_{Dmethods[method]}.csv' )

    if makeplot and ( len( df_Eb ) > 0 or len( df_Ebsc ) > 0 ):
        plt.figure()
        s = dim.split('/')[0]
        plt.title(f'{s}')
        plt.errorbar(df_Eb.index, df_Eb.ene, df_Eb.err, fmt='^b', label=f'{Dmethods[method]}')
        #plt.xlim(0,None)
        plt.xlim(0,0.103)
        plt.xlabel(f'{df_Eb.index.name} /a.u.')
        plt.ylabel('Binding energy /meV')
        plt.legend()
        plt.tight_layout()
        plt.savefig(f'EneDiff/Fig_Eb_{Dmethods[method]}.png')
        if viewplot: plt.show()
        # plot total energies
        plt.figure()
        s = dim.split('/')[0]
        plt.title(f'{Dmethods[method]}')
        plt.errorbar(dfs[dim].index, dfs[dim].ene, dfs[dim].err, fmt='vb', label=f'AB')
        if (Nmol == 1):
            plt.errorbar(dfs[mon].index, 2*dfs[mon].ene, 2*dfs[mon].err, fmt='^r', label=f'2 x A')
        #elif (Nmol == 2):
        #    plt.errorbar(dfs[mon1].index, dfs[mon1].ene, dfs[mon1].err, fmt='+r', label=f'A')
        #    plt.errorbar(dfs[mon2].index, dfs[mon2].ene, dfs[mon2].err, fmt='*g', label=f'B')
        #plt.xlim(0,None)
        plt.xlim(0,0.103)
        plt.xlabel(f'{df_Eb.index.name} /a.u.')
        plt.ylabel('Energy /a.u.')
        plt.legend()
        plt.tight_layout()
        plt.savefig(f'Fig_Ene_{Dmethods[method]}.png')
        if viewplot: plt.show()
  except:
    print(f'WARNING: Missing data for {s} {method}!')

