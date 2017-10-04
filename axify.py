import argparse
import numpy as np
import matplotlib.pyplot as plt
import os
from pylab import *

parser = argparse.ArgumentParser(
    description=r"""Script to convert a large numpy array to a pdf
and also generate a tikzpicture, which plots the pdf with axises
to be included in a TeX document."""
    )

parser.add_argument(
    '-p',
    action="store",
    help='path to the *.npy file(s) without the file extension',
    nargs='+',
    type=str
    )

parser.add_argument(
    '-m',
    action="store",
    help='colormap for the plot; must be present in matplotlib and pgfplots',
    default="jet",
    type=str
    )

parser.add_argument(
    '-t',
    action="store",
    help='tikz template to use; possible choices: simple,...',
    default="simple",
    type=str
    )

args = parser.parse_args()

simple = r"""\begin{tikzpicture}
\begin{axis}[
    enlargelimits = false,
    axis on top = true,
    axis equal image,
    point meta min = %f,
    point meta max = %f,
    colorbar horizontal,
    colormap/%s
    ]
    \addplot graphics [
        xmin = 0,
        xmax = %d,
        ymin = 0,
        ymax = %d
    ] {%s};
\end{axis}
\end{tikzpicture}
"""

themes = {
    'simple': simple
}

def compose(
    theme,          # the theme to use in TeX code
    metaMin,        # minimum value in data
    metaMax,        # maximum value in data
    size,           # tuple of dimensions; attention it is swapped!
    colorMap,       # the colormap of the plot and colorbar
    path            # path to work on
    ):
    
    # open the file
    f = open(path + '.tex', 'w')
    
    # write the tikz-snippet
    f.write(themes[theme] % (
            metaMin,
            metaMax,
            colorMap,
            *size,
            path
        ))
    
    # clean everything up
    f.close()

if __name__ == "__main__":
    
    # parse arguments
    lstPaths = args.p
    colorMap = args.m
    theme = args.t
    
    for imgPath in lstPaths:
        if os.path.isfile(imgPath + '.npy'):
            
            # load the numpy array
            data = np.load(imgPath + '.npy')
            
            # plot image without boundaries and save it to pdf
            ax = subplot(111)
            img = ax.imshow(data, interpolation='nearest')
            img.set_cmap(colorMap)
            imsave(
                fname = imgPath + '.pdf', 
                arr = data,
                cmap = colorMap
            )
            
            size = (data.shape[1], data.shape[0])
            metaMin = np.min(data)
            metaMax = np.max(data)
            
            # call the composition function
            compose(theme, metaMin, metaMax, size, colorMap, imgPath)
        else:
            raise(StandardError)
