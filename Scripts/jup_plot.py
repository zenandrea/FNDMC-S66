#!/usr/bin/env python
# coding: utf-8

# Script to set up the plotting environment for Jupyter notebooks
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import pandas as pd
import warnings
from scipy.optimize import OptimizeWarning

# Suppress the specific warning
warnings.filterwarnings("ignore", category=OptimizeWarning)

def texfalse_import():
    plt.rcParams.update(
        {
            "font.family": "serif",  # use serif/main font for text elements
            "font.size": 9,
            "text.usetex": False,  # use inline math for ticks
        }
    )

def textrue_import():
    import matplotlib as mpl
    mpl.use("pgf")
    plt.rcParams.update({
        "font.family": "serif",  # use serif/main font for text elements
        "font.size": 9,
        "text.usetex": True,     # use inline math for ticks
        "pgf.rcfonts": False,    # don't setup fonts from rc parameters
        "pgf.preamble":"\n".join([
            r"\usepackage{amsmath}",            # load additional packages
            r"\usepackage{amssymb}",   # unicode math setup
            r"\usepackage[mathrm=sym]{unicode-math}",  # serif font via preamble
            r"\setmathfont{FiraMath-Regular.otf}",
            r"\setmainfont[BoldFont={FiraSans-SemiBold.otf}]{FiraSans-Regular.otf}",
            r"\setmathfont[version=bold]{FiraMath-Bold.otf}",
            r"\newcommand{\minus}{\scalebox{0.5}[1.0]{$-$}}" # serif font via preamble
        ])
    })

# Dictionary of colors for the color scheme in our plots
color_dict = {
    "red": "#e6194b",
    "green": "#3cb44b",
    "yellow": "#ffe119",
    "blue": "#4363d8",
    "orange": "#f58231",
    "purple": "#911eb4",
    "cyan": "#42d4f4",
    "magenta": "#f032e6",
    "lime": "#bfef45",
    "pink": "#fabed4",
    "teal": "#469990",
    "lavendar": "#dcbeff",
    "brown": "#9A6324",
    "beige": "#fffac8",
    "maroon": "#800000",
    "mint": "#aaffc3",
    "olive": "#808000",
    "apricot": "#ffd8b1",
    "navy": "#000075",
    "grey": "#a9a9a9",
    "white": "#ffffff",
    "black": "#000000",
}

# Colors to cycle through for our plots
plt.rcParams["axes.prop_cycle"] = plt.cycler(
    color=[
        "#4363d8",
        "#e6194B",
        "#3cb44b",
        "#f58231",
        "#ffe119",
        "#911eb4",
        "#42d4f4",
        "#f032e6",
        "#bfef45",
        "#fabed4",
        "#469990",
        "#dcbeff",
        "#9A6324",
        "#fffac8",
        "#800000",
        "#aaffc3",
        "#808000",
        "#ffd8b1",
        "#000075",
        "#a9a9a9",
        "#ffffff",
        "#000000",
    ]
)

def convert_df_to_latex_input(
    df,
    start_input = '\\begin{table}\n',
    end_input = '\n\\end{table}',
    label = "tab:default",
    caption = "This is a table",
    replace_input = {},
    df_latex_skip = 0,
    adjustbox = 0,
    scalebox = False,
    multiindex_sep = "",
    filename = "./table.tex",
    index = True,
    column_format = None,
    center = False,
    rotate_column_header = False,
    output_str = False
):
    if column_format is None:
        column_format = "l" + "r" * len(df.columns)
    
    if label != "":
        label_input = r"\label{" + label + r"}"
    else:
        label_input = ""
    caption_input = r"\caption{" + label_input + caption +  "}"

    if rotate_column_header:
        df.columns = [r'\rotatebox{90}{' + col + '}' for col in df.columns]

    with pd.option_context("max_colwidth", 1000):
        df_latex_input = df.to_latex(escape=False, column_format=column_format,multicolumn_format='c', multicolumn=True,index=index)
    for key in replace_input:
        df_latex_input = df_latex_input.replace(key, replace_input[key])
    
    df_latex_input_lines = df_latex_input.splitlines()[df_latex_skip:]
    # Get index of line with midrule
    toprule_index = [i for i, line in enumerate(df_latex_input_lines) if "toprule" in line][0]
    df_latex_input_lines[toprule_index+1] = df_latex_input_lines[toprule_index+1] + ' ' + multiindex_sep
    df_latex_input = '\n'.join(df_latex_input_lines)
    end_adjustbox = False

    if output_str:
        latex_string = ""
        latex_string += start_input + "\n"
        latex_string += caption_input + "\n"
        if center == True and adjustbox == 0:
            latex_string += r"\begin{adjustbox}{center}" + "\n"
            end_adjustbox = True
        elif adjustbox > 0 and center == False:
            latex_string += r"\begin{adjustbox}{max width=" + f"{adjustbox}" + r"\textwidth}" + "\n"
            end_adjustbox = True    
        elif adjustbox > 0 and center == True:
            latex_string += r"\begin{adjustbox}{center,max width=" + f"{adjustbox}" + r"\textwidth}" + "\n"
            end_adjustbox = True
        if scalebox:
            latex_string += r"\begin{adjustbox}{scale=" + f"{scalebox}" + "}" + "\n"
            end_adjustbox = True
        latex_string += df_latex_input
        if end_adjustbox:
            latex_string += "\n\\end{adjustbox}"
        latex_string += "\n" + end_input
        return latex_string

    else:
        with open(filename, "w") as f:
            f.write(start_input + "\n")
            f.write(caption_input + "\n")
            if center == True and adjustbox == 0:
                f.write(r"\begin{adjustbox}{center}" + "\n")
                end_adjustbox = True
            elif adjustbox > 0 and center == False:
                f.write(r"\begin{adjustbox}{max width=" + f"{adjustbox}" + r"\textwidth}" + "\n")
                end_adjustbox = True    
            elif adjustbox > 0 and center == True:
                f.write(r"\begin{adjustbox}{center,max width=" + f"{adjustbox}" + r"\textwidth}" + "\n")
                end_adjustbox = True
            if scalebox:
                f.write(r"\begin{adjustbox}{scale=" + f"{scalebox}" + "}" + "\n")
                end_adjustbox = True
            f.write(df_latex_input)
            if end_adjustbox:
                f.write("\n\\end{adjustbox}")
            f.write("\n" + end_input)