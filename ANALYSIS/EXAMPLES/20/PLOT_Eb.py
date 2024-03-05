#! /usr/bin/env python3

import os
import pyblock
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

makeplot = True # False
viewplot = makeplot
makefit = True

c = 627.503   # Ha to kcal/mol
#c = 27.21138505 * 1e3  # Ha to meV

# Hobza http://cuby4.molecular.cz/dataset_s66.html	Hobsa rev CCSD(T)/CBS(haTZ)	Martin newBronze	Martin Silver	Martin Gold	Martin PCCP2022	Nagy 14k-GOLD


Eb_ref = {}
Eb_ref['Hobza']            = -19.09
Eb_ref['Hobza rev']        = -19.41
Eb_ref['Martin newBronze'] = -19.328
Eb_ref['Martin Silver']    = -19.361
Eb_ref['Martin PCCP2022']  = -19.397
Eb_ref['Nagy 14k-GOLD']    = -19.383

sty = {}
sty['Hobza']            = { 'c':'c', 'ls':':' } 
sty['Hobza rev']        = { 'c':'b', 'ls':'-.' }  
sty['Martin newBronze'] = { 'c':'y', 'ls':':' } 
sty['Martin Silver']    = { 'c':'silver', 'ls':'-.' } 
sty['Martin PCCP2022']  = { 'c':'k', 'ls':'--' } 
sty['Nagy 14k-GOLD']    = { 'c':'gold', 'ls':'--' } 

Dmethods = {}
Dmethods['tm5_JoptLA_']  = 'TM_lim5_JoptLA'
Dmethods['tm5_']         = 'TM_lim5_Jopt'
Dmethods['dla5_']        = 'DLA_lim5_Jdim'
Dmethods['dla5_Jopt_']   = 'DLA_lim5_Jopt'

methods = list( Dmethods.keys() )

Dcolor = {}
Dcolor['tm5_JoptLA_']  = 'blueviolet'
Dcolor['tm5_']         = 'cyan'
Dcolor['dla5_']        = 'green'
Dcolor['dla5_Jopt_']   = 'red'

if makefit:
    from scipy.optimize import curve_fit
    def fun_lin( x, a, b ):
        return a + b * x
    def fun_quad( x, a, b, c ):
        return a + b * x + c * x**2
    def fun_cub( x, a, b, c, d ):
        return a + b * x + c * x**2 + d * x**3


if os.path.isdir('./EneDiff'):
    pass
elif os.path.isfile('./EneDiff'):
    print('Warning: ./EneDiff is a file! Exit')
    exit
else:
    print('Warning: ./EneDiff does not exist! Exit')
    exit

plt.figure()
for ref in Eb_ref:
    plt.axhline(y=Eb_ref[ref],c=sty[ref]['c'],linestyle=sty[ref]['ls'],label=ref)
#plt.xlim(0,None)
plt.xlim(0,0.103)
plt.xlabel(f'DMC timestep /a.u.')
plt.ylabel('Binding energy /meV')

for method in methods:
        print(f'*** {Dmethods[method]} : {method}')
        csvfile = f'EneDiff/Eb_{Dmethods[method]}.csv'
        print( csvfile )
        if os.path.isfile( csvfile ):
            df = pd.read_csv( csvfile, decimal='.', index_col='tau') 
            if makefit: linestyle=''
            else: linestyle=':'
            plt.errorbar(df.index, df.ene, df.err, label=f'{Dmethods[method]}',
                         ls=linestyle, c=Dcolor[method], marker='o', mec='k', elinewidth=2, capsize=3)
            print( df,'\n' )
            if makefit:
                print('Fit with quadratic function')
                xdata = df.index.to_numpy()
                ydata = df.ene.to_numpy()
                sigma = df.err.to_numpy()
                popt, pcov = curve_fit( fun_quad, xdata=xdata, ydata=ydata, sigma=sigma )
                xlinspace = np.linspace( 0, 0.103, 100)
                funlinspace = fun_quad( xlinspace, *popt )
                print( f'popt = {popt}' )
                perr = np.sqrt(np.diag(pcov)) 
                print( f'perr = {perr}' )
                print( f'pcov = {pcov}\n' )
                plt.plot( xlinspace, funlinspace, '--', color=Dcolor[method], label=f'{popt[0]:.2f}({perr[0]*100:.0f}) + {popt[1]:.0f}({perr[1]:.0f}) X + {popt[2]:.0f}({perr[2]:.0f}) X^2' )

        else:
            print( f'{csvfile} is not a file' )

plt.legend()
plt.tight_layout()
plt.savefig(f'EneDiff/Fig_Eb.png',dpi=300)
if viewplot: plt.show()

