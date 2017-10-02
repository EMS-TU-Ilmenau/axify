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
    help='path to the *.npy file without the file extension',
    type=str
    )

parser.add_argument(
    '-m',
    action="store",
    help='colormap for the plot; must be present in matplotlib and pgfplots',
    default="jet",
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

def main(metaMin, metaMax, size, colorMap, path):
    f = open(path + '.tex', 'w')
    
    f.write(simple % (
            metaMin,
            metaMax,
            colorMap,
            *size,
            path
        ))
    
    f.close()

if __name__ == "__main__":
    # parse arguments
    imgPath = args.p
    colorMap = args.m
    
    
    if os.path.isfile(imgPath + '.npy'):
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
        
        # call the main function
        main(metaMin, metaMax, size, colorMap, imgPath)
    else:
        raise(StandardError)
