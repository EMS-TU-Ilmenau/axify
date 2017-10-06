# This file is part of axify.

# axify is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# axify is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with axify.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
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
    help='Colormap for the plot; must be present in matplotlib and pgfplots. \
    Currently supported themes: hot, jet, tui',
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

# definition of the simplest theme possible
simple = r"""\begin{tikzpicture}
\begin{axis}[
    enlargelimits = false,
    axis on top = true,
    axis equal image,
    point meta min = %f,
    point meta max = %f,
    colorbar horizontal,
    %s,
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
# dictionary of present themes
themes = {
    'simple': simple
}

# generate a tuple containing the object that is the matplotlib colorbar
# and the string the generates the same bar in TeX code


def genCustomColormap(tplCols, name):

    # create the matplotlib colorbar
    theMap = LinearSegmentedColormap.from_list(
        name,
        [*tplCols],
        N=50
    )

    # get the number of colors
    numCols = len(tplCols)
    tplCols255 = ()

    # generate the code for each color node
    for ii, tt in enumerate(tplCols):
        col = ','.join(tuple(str(cc) for cc in tt))
        tplCols255 = tplCols255 + ('rgb(%fpt)=(%s)' %
                                   (ii / (numCols - 1), col),)

    # fuse everything together to a simple line of code
    theTex = r"""colormap={mymap}{%s}""" % ('; '.join(tplCols255))
    return (theMap, theTex)

# generate a tuple that contains the matplotlib name and the TeX code to
# be included in the document


def genPresentColormap(name):
    return (name, r"""colormap/%s""" % (name))


# tuple containing all the color maps. custom ones and predefined ones
maps = {
    'hot': genPresentColormap('hot'),
    'jet': genPresentColormap('jet'),
    'tui': genCustomColormap(((0.75, 0.12, 0.06), (1, 1, 1), (0, 0.21, 0.39)),
                             'tui')
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
            imsave(
                fname=imgPath + '.png',
                arr=data,
                cmap=maps[colorMap][0]
            )

            size = (data.shape[1], data.shape[0])
            metaMin = np.min(data)
            metaMax = np.max(data)

            # call the composition function
            compose(theme, metaMin, metaMax, size, maps[colorMap][1], imgPath)
        else:
            raise(StandardError)
