# Define name and color convenctions



def map_DMC( name ):
    if ( name == 'DMC' ):
        rename = 'DMC/LA/ZSGMA'
    elif ( name == 'DMCdla' ):
        rename = 'DMC/DLA/ZSGMA'
    elif ( name == 'DMCdla5' ):
        rename = 'DMC/DLA/ZSGMA*'
    elif ( name == 'DMCtm5' ):
        rename = 'DMC/TM/ZSGMA*'
    else:
        rename = 'DMC(unknown)'
    return rename

def dmc_color( dmc_type, dmc_Jas='Jopt' ):
    if dmc_type=='DMCdla5':
        if dmc_Jas=='Jopt':
            color = 'green'
        elif dmc_Jas=='JoptLA':
            color = 'coral'
        elif dmc_Jas=='Jdimer':
            color = 'red'
        else:
            color = 'violet'
    elif dmc_type=='DMCtm5':
        if dmc_Jas=='JoptLA':
            color = 'blue'
        elif dmc_Jas=='Jopt':
            color = 'cyan'
        elif dmc_Jas=='Jdimer':
            color = 'gray'
        else:
            color = 'violet'
    elif dmc_type=='DMCdla':
        if dmc_Jas=='Jopt':
            color = 'gold'
        elif dmc_Jas=='Jdimer':
            color = 'yellow'
        else:
            color = 'violet'
    elif dmc_type=='DMC':
        if dmc_Jas=='Jopt':
            color = 'magenta'
        elif dmc_Jas=='Jdimer':
            color = 'orange'
        else:
            color = 'violet'        
    return color

def dft_color( name ):
    if name == 'LDA':
        c = 'yellow'
    elif name == 'PBE':
        c = 'orange'
    elif name == 'B3LYP':
        c = 'red'
    elif name == 'HF':
        c = 'silver'
    elif name == 'CCSD(T) small':
        c = 'gray'
    elif name == 'CCSD(T)':
        c = 'black'
    elif name == '0.10':
        c = 'cyan'
    elif name == '0.03':
        c = 'blue'
    elif name == '0.01':
        c = 'green'
    elif name == '0.003':
        c = 'darkgreen'
    else:
        c = 'lightgreen'
    return c

