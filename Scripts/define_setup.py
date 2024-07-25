
equil_time_au = 10.

#pickunits = 'au'
pickunits = 'kcal/mol'

units = { 'au':1, 'eV':2, 'kcal/mol':3,
        'au/atom':4, 'eV/atom':5, 'kcal/mol/atom':6 }

conv2au = {
        'au':1.0,
        'eV':27.21138505,
        'kcal/mol':627.503,
        'kJ/mol':2625.5,
        'cm^-1':219474.63,
        'K': 315777.,
        'J': 43.60E-19,
        'Hz':6.57966E+15,
        }

#os.getcwd()
dir_analysis = '/Users/zen/Dropbox/WORK/2021_S66/ANALYSIS/'
#dir_analysis = '/home/zen/Dropbox/WORK/2021_S66/ANALYSIS/'

#datadir = dir_analysis +'/../DATA_CAM/'
#reblockexe = '/Users/zen/APPS/CASINO/bin_qmc/reblock'
#reblockexe = '/Users/zen/CASINO/bin_qmc/utils/macos-gnu-parallel.Andreas-MacBook-Pro-2021/reblock'

atoms_info = {
    'H' : { 'Nel':1, 'Nelv':1 },
    'C' : { 'Nel':6, 'Nelv':4 },
    'N' : { 'Nel':7, 'Nelv':5 },
    'O' : { 'Nel':8, 'Nelv':6 }
}

mol_names = ( 
    'AcNH2',
    'AcOH',
    'Benzene',
    'Cyclopentane',
    'Ethene',
    'Ethyne',
    'MeNH2',
    'MeOH',
    'Neopentane',
    'Pentane',
    'Peptide',
    'Pyridine',
    'Uracil',
    'Water'
)

