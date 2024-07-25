import numpy as np
import glob
import os
import re
import pandas as pd
import pyblock
Hartree = 27.2114079527

taumax = 0.1

def x_axis( df, code ):
    x = np.array( df.index )
    if code == 'TurboRVB_LRDMC':
        xnew = x**2
    else:
        xnew = x
    return xnew

def EneDiff(a,b,c=627.503):
    return (a-b)*c


def EneDiffErr(a,b,c=627.503):
    return c*(( a**2 + b**2 )**0.5)


def EneDiffX(a,b,c=627.503):
    return (a.ene-b.ene)*c, c*(( a.err**2 + b.err**2 )**0.5)


def EneDiff_AA(aa,a,c=627.503):
    ene = c*( aa.ene - 2*a.ene )
    err = c*(( aa.err**2 + 4* a.err**2 )**0.5 )
    return ene, err


def gauss (x, a, lista, method, dist_info = False):
    
    # a is the dictionary
    # lista is the list of codes to consider
    # method is the algorithm, eg 'LA'
    import scipy.stats as stats
    gauss = 0
    energy = 0

    for i in lista:
        gauss += stats.norm.pdf(x, a[i][method][0], a[i][method][1])
        energy += a[i][method][0]
    gauss /= len(lista)
    energy /= len(lista)

    error2 = 0


    for i in lista:

        error2 += (a[i][method][1]**2 + a[i][method][0]**2) - energy**2
    
    error = np.sqrt(error2/len(lista))
    
    if dist_info:
        return gauss, energy, error
    else:
        return gauss

def mean_codes(a,lista,method):
    
    energy = 0

    for i in lista:
        energy += a[i][method][0]
    energy /= len(lista)

    error2 = 0


    for i in lista:

        error2 += (a[i][method][1]**2 + a[i][method][0]**2) - energy**2
    
    error = np.sqrt(error2/len(lista))
    
    return energy, error

def mean_codes_unweighted(a,lista,method):
    energy = 0
    norm = 0
    error = 0
    error2 = 0
    
    for i in lista:
        energy += a[i][method][0]
        error2 += a[i][method][1]**2
    
    energy /= len(lista)
    error = np.sqrt(error2/len(lista))
    
    return energy, error

def mean_codes_tot_ene(a,lista,method,syslabel='mw'):
    energy = 0
    norm = 0
    error = 0
    
    for i in lista:
        energy += a[i][method][syslabel][0] * (1/a[i][method][syslabel][1]**2)
        norm += (1/a[i][method][syslabel][1]**2)
    
    energy /= norm
    #error = np.sqrt(1/norm)
    
    for i in lista:
        error += (a[i][method][syslabel][0]-energy)**2 / (len(lista)-1)
    
    error = np.sqrt(error)
    
    return energy, error


def gauss_tau (x, a, lista, tau):
    
    # a is the dictionary
    # lista is the list of codes to consider
    # method is the algorithm, eg 'LA'
    import scipy.stats as stats
    gauss = 0
    energy = 0
    for i in lista:
        gauss += stats.norm.pdf(x, a[i].loc[tau][0], a[i].loc[tau][1])
        energy += a[i].loc[tau][0]
    energy /= len(lista)
    gauss /= len(lista)

    error2 = 0


    for i in lista:
        error2 += (a[i].loc[tau][1]**2 + a[i].loc[tau][0]**2) - energy**2
    
    error = np.sqrt(error2/len(lista))
    return gauss, energy, error

def read_mrcc_output(file_path):
    """From the MRCC output file: Read Energy"""
    with open(file_path) as fd:
        lines = fd.readlines()

    scf_energy = None
    mp2_corr_energy = None
    ccsd_corr_energy = None
    ccsdt_corr_energy = None
    ccsdtq_corr_energy = None
    for line in lines:
        if "FINAL HARTREE-FOCK ENERGY" in line or "FINAL KOHN-SHAM ENERGY" in line:
            scf_energy = float(line.split()[-2]) * Hartree
        elif "MP2 correlation energy" in line:
            mp2_corr_energy = float(line.split()[-1]) * Hartree
        elif "CCSD correlation energy" in line:
            ccsd_corr_energy = float(line.split()[-1]) * Hartree
        elif "CCSD(T) correlation energy" in line:
            ccsdt_corr_energy = float(line.split()[-1]) * Hartree
        elif "Total CCSDT(Q) energy" in line:
            ccsdtq_corr_energy = float(line.split()[-1]) * Hartree - scf_energy
        elif "Total MP2 energy" in line:
            mp2_corr_energy = float(line.split()[-1]) * Hartree - scf_energy
        elif "Total CCSDT energy" in line:
            ccsdt_corr_energy = float(line.split()[-1]) * Hartree - scf_energy

    results = {}

    if scf_energy is not None:
        results["scf_energy"] = scf_energy
        results["energy"] = scf_energy
    if mp2_corr_energy is not None:
        results["mp2_corr_energy"] = mp2_corr_energy
        results["energy"] = scf_energy + mp2_corr_energy
    if ccsd_corr_energy is not None:
        results["ccsd_corr_energy"] = ccsd_corr_energy
        results["energy"] = scf_energy + ccsd_corr_energy
    if ccsdtq_corr_energy is not None:
        results["ccsdtq_corr_energy"] = ccsdtq_corr_energy
        results["energy"] = scf_energy + ccsdtq_corr_energy
        results["ccsdt_corr_energy"] = ccsdt_corr_energy
    elif ccsdt_corr_energy is not None:
        results["ccsd(t)_corr_energy"] = ccsdt_corr_energy
        results["energy"] = scf_energy + ccsdt_corr_energy


    return results

def get_cbs(hf_X, corr_X, hf_Y, corr_Y, X=2, Y=3, family='cc', convert_Hartree=False,shift=0.0,output=True):
    alpha_dict = {
        "def2_2_3": 10.39,
        "def2_3_4": 7.88,
        "cc_2_3": 4.42,
        "cc_3_4": 5.46,
        "cc_4_5": 5.46,
        "acc_2_3": 4.30,
        "acc_3_4": 5.79,
        "acc_4_5": 5.79,
        "mixcc_2_3": 4.36,
        "mixcc_3_4": 5.625,
        "mixcc_4_5": 5.625
    }

    beta_dict = {
        "def2_2_3": 2.40,
        "def2_3_4": 2.97,
        "cc_2_3": 2.46,
        "cc_3_4": 3.05,
        "cc_4_5": 3.05,
        "acc_2_3": 2.51,
        "acc_3_4": 3.05,
        "acc_4_5": 3.05,
        "mixcc_2_3": 2.485,
        "mixcc_3_4": 3.05,
        "mixcc_4_5": 3.05
    }

    if Y != X+1:
        print('Y does not equal X+1')

    if family != 'cc' and family != 'def2' and family != 'acc' and family != 'mixcc':
        print('Wrong basis set family stated')

    alpha = alpha_dict['{0}_{1}_{2}'.format(family, X, Y)]
    beta = beta_dict['{0}_{1}_{2}'.format(family, X, Y)]

    hf_cbs = hf_X - np.exp(-alpha*np.sqrt(X))*(hf_Y - hf_X) / \
        (np.exp(-alpha*np.sqrt(Y))-np.exp(-alpha*np.sqrt(X)))
    corr_cbs = (X**(beta)*corr_X - Y**(beta)*corr_Y)/(X**(beta)-Y**(beta))
    if convert_Hartree == True:
        if output==True:
            print('CBS({0}/{1}) HF: {2:.9f} Corr: {3:.9f} Tot: {4:.9f}'.format(X,Y, hf_cbs*Hartree + shift, corr_cbs*Hartree , (hf_cbs+corr_cbs)*Hartree + shift))
        return hf_cbs*Hartree + shift, corr_cbs*Hartree, (hf_cbs+corr_cbs)*Hartree
    else:
        if output==True:
            print('CBS({0}/{1})  HF: {2:.9f} Corr: {3:.9f} Tot: {4:.9f}'.format(X,Y, hf_cbs + shift, corr_cbs, (hf_cbs+corr_cbs) + shift))
        return hf_cbs + shift, corr_cbs, (hf_cbs+corr_cbs) + shift