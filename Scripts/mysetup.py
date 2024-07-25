# setup

taumax = 0.1 # 0.3 # 0.091


systems = [ 'm', 'w', 'mw', 'm---w' ]

syst_names = dict(zip(systems,['methane','water','complex','far']))


methods = [ 'LA', 'TM', 'DLA', 'DLTM' ]

methods_opt = ['LA0', 'TM0']


Ediffs_label = {
'Eb'   : 'Binding Energy [meV]',
'Ebsc' : 'Binding Energy S.C. [meV]',
'SCE'  : 'Size Consistency Error [meV]'
}

Ediffs_ref = {
'Eb'   : -27.0,
'Ebsc' : -27.0,
'SCE'  : 0.0
}

Ediffs = list( Ediffs_label.keys() )

#######################################

colors = {
    'TurboRVB' : 'red',
    'CASINO'   : 'green',   # see above 
    'QMCPACK'  : 'blue',
    'CHAMP_Holland' : 'blueviolet', # set here the final name for Claudia Filippi's version
    'CHAMP_Cornell_Paris' : 'magenta',    # set here the final name for Cyrus Umrigar's version
    'QMC=Chem' : 'cyan',
    'QMeCha'   : 'orange',
    'PyQMC'    : 'black',
    'Amolqc'   : 'brown',
    'QWalk'    : 'olive',
    'CMQMC'    : 'darkgray',
}

codes = list( colors.keys() )

colors_opt = {
    'TurboRVB_sandro'  : 'tomato',
    'QMCPACK_complex'  : 'skyblue',
    'CASINO_limdmc4'   : 'gold',
    'CASINO_limdmc5'   : 'green', 
    'CASINO_limdmc5_j+'    : 'red', #'mediumseagreen',
    'CASINO_limdmc5_cbycJbufF' : 'blue', #'darkgreen',
    'CASINO_limdmc5t'   : 'magenta', #'yellow',
    'CASINO_limdmc6t'   : 'lime',
    'CASINO_pw1000'    : 'lime',
    'CASINO_pw1000_andes' : 'mediumseagreen',
}

codes_opt = list( colors_opt.keys() )

colors_all = { **colors, **colors_opt }

codes_all = codes + codes_opt

codes_sel = [ 'CASINO', 'QMCPACK', 'TurboRVB' ]

codes_sel2 = [ c for c in codes_all if c.startswith('CASINO') or c.startswith('QMCPACK') or c.startswith('TurboRVB') ]

codes_casino = [ c for c in codes_all if c.startswith('CASINO_') ]

