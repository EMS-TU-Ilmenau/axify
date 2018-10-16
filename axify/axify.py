#!/usr/bin/env python3

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


import colorfy
import argparse
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.colors as clr
import matplotlib.cm as cmx
import os


class Theme:
    r"""
    Theme Abstraction Class

    This class represents a theme, that can be constructed by providing
    a file, which contains the template of the theme. It also allows
    to feed data into the theme and then return the finished output.

    Most of the plotting routines need a theme to work with.

    Examples
    --------
    >>> import axify as ax
    >>> thme = ax.Theme('simple.tex')
    """
    @property
    def string(self):
        return self._string

    @property
    def path(self):
        return self._path

    def __init__(self, path):
        self._path = path
        try:
            open(self._path)
        except (FileNotFoundError):
            print('Could not find theme file ' + path)
        else:
            with open(self._path) as f:
                self._string = f.read()

    def reload(self):
        with open(self._path) as f:
            self._string = f.read()


class ColorMap:
    r"""
    Colormap Class

    This class provides various methods to load, import and print colorbars
    which then are used in the plots created by axify.

    Examples
    --------
    >>> import axify as ax
    >>> cmap = ax.ColorMap('hot')
    """

    @property
    def obj(self):
        return self._obj

    def __init__(self, name, **kwargs):
        # remember if we found a map in the colorfy workspace
        nameFound = 0

        # check if we should import a colorfy workspace
        if 'colorfy' in kwargs:

            # try to load it
            ws = colorfy.Workspace(kwargs['colorfy'])

            # now look if we can find the colorbar in the workspace
            for ccbb in ws.colorMaps:
                if ccbb._name == name:
                    nameFound = 1

                    # extract the colorbar information from the workspace
                    self._name = ccbb.name
                    self._cols = [col._tplDef for col in ccbb.colors]
                    self._pos = [pos for pos in ccbb.positions]

                    # prepare the data to be registered as a matplotlib
                    # colormap
                    cdct = {}
                    cdct['red'] = []
                    cdct['green'] = []
                    cdct['blue'] = []
                    for cc, pp in zip(self._cols, self._pos):
                        cdct['red'].append([pp, cc[0], cc[0]])
                        cdct['green'].append([pp, cc[1], cc[1]])
                        cdct['blue'].append([pp, cc[2], cc[2]])

                    plt.register_cmap(name=self._name, data=cdct)
                    self._obj = plt.get_cmap(self._name)

                    # create a sampling of the resulting colormap
                    self._smpl = self._sample()

        # if we did not find it in the workspace, it must be a
        # matplotlib colorbar
        if nameFound == 0:
            if name in plt.colormaps():
                self._name = name
                self._obj = plt.get_cmap(self._name)
                self._cols = []
                self._pos = []
                self._smpl = self._sample()
            else:
                raise(NotImplementedError)

    def _sample(self):
        num = 100
        colMapNorm = clr.Normalize(vmin=0, vmax=1)
        scalarMap = cmx.ScalarMappable(norm=colMapNorm, cmap=self._obj)

        res = np.empty((3, num))

        for ii in range(num):
            res[:, ii] = scalarMap.to_rgba(float(ii) / (num - 1))[:3]

        return res

    def toPGF(self):
        handleString = r"""
        rgb(%(pos)s pt)=(%(col)s),"""
        res = "colormap={" + self._name + "}{"

        ii = 0
        N = self._smpl.shape[1]
        for ii in range(N):
            dct = {
                'pos': float(ii)/(N - 1),
                'col': ','.join([
                    str(self._smpl[0, ii]),
                    str(self._smpl[1, ii]),
                    str(self._smpl[2, ii])
                ])
            }
            res += handleString % (dct)

        return res + "}"


def _compose(
    theme,          # the theme to use in TeX code
    dctPlotInfo,    # dictionary containing the extracted image data
):

    try:
        # open the file
        f = open(dctPlotInfo['imagePath'] + '.tex', 'w')
    except IOError:
        print("Could not write to file " + dctPlotInfo['imagePath'])
    else:
        # write the tikz-snippet
        f.write(theme.string % (dctPlotInfo))

        # clean everything up
        f.close()


def toHeatmap(
    arrData,
    imgPath,
    theme,
    colorMap,
    xLim=[],
    yLim=[],
    zLim=[],
    xLabel='x',
    yLabel='y',
    themeArgs={},
):
    """
    Create a heatmap plot from 2D data.

    Parameters
    ----------
    arrData : numpy.ndarray
        the actual data to plot. must be 2D.
    imgPath : string
        path to save image and text file to, no file-ending
    theme : Theme
        teX theme to be used
    colorMap : Colormap
        colormap to be used
    xLim=[] : list
        range if the x axis
    yLim=[] : list
        range of the y axis
    zLim=[] : list
        range of the data values
    xLabel='x' : string
        label on the x axis
    yLabel='y' : string
        label on the y axis

    Examples
    --------
    >>> import axify as ax
    >>> import numpy as np
    >>> # create some random data
    >>> data = np.random.randn(1024, 1024)
    >>> # load an axify theme
    >>> thme = ax.Theme('simple.tex')
    >>> # construct a colormap
    >>> cmap = ax.ColorMap('hot')
    >>> # write the png and the tex file
    >>> ax.toHeatmap(data, 'data', thme, cmap)
    """

    if xLim == []:
        xLim = [0, arrData.shape[1]]

    if yLim == []:
        yLim = [0, arrData.shape[0]]

    if zLim == []:
        zLim = [np.min(arrData), np.max(arrData)]

    dctPlotInfo = {
        'dataMin': zLim[0],
        'dataMax': zLim[1],
        'xMin': xLim[0],
        'xMax': xLim[1],
        'xLabel': xLabel,
        'yMin': yLim[0],
        'yMax': yLim[1],
        'yLabel': yLabel,
        'imagePath': imgPath,
        'colormap': colorMap.toPGF()
    }

    dctPlotInfo.update(themeArgs)

    mat = arrData - zLim[0]
    mat /= (zLim[1] - zLim[0])

    try:
        # plot image without boundaries and save it to png
        plt.imsave(
            fname=imgPath + '.png',
            arr=255*mat,
            cmap=colorMap.obj,
            vmin = 0,
            vmax = 255
        )
        print(zLim)
    except IOError:
        print("Could not write to file " + imgPath)
    else:
        # call the composition function
        _compose(theme, dctPlotInfo)


def toScatter(
    arrData,
    imgPath,
    theme,
    colorMap,
    xLim=[],
    yLim=[],
    zLim=[],
    xLabel='x',
    yLabel='y',
    themeArgs={}
):
    r"""
    Create a scatter plot from a Nx3 ndarray, where the first two
    columns are used as plotting coordinates where the values of the third
    column are plotted to.

    Parameters
    ----------
    arrData : numpy.ndarray
        the actual data to plot. must be of dimension N x 3.
    imgPath : string
        path to save image and text file to, no file-ending
    theme : Theme
        teX theme to be used
    colorMap : ColorMap
        colormap to be used
    xLim=[] : list
        range if the x axis
    yLim=[] : list
        range of the y axis
    zLim=[] : list
        range of the data values
    xLabel='x' : string
        label on the x axis
    yLabel='y' : string
        label on the y axis

    Returns
    -------

    Examples
    --------
    >>> import axify as ax
    >>> import numpy as np
    >>> # create some random data
    >>> data = np.empty((1024,3))
    >>> data[:,:2] = np.random.uniform(-1, 1, (1024,2))
    >>> data[:,2] = np.random.randn(1024)
    >>> # load an axify theme
    >>> thme = ax.Theme('simple.tex')
    >>> # construct a colormap
    >>> cmap = ax.ColorMap('hot')
    >>> # write the png and the tex file
    >>> ax.toHeatmap(data, 'data', thme, cmap)
    """

    if xLim == []:
        xLim = [np.min(arrData[:, 0]), np.max(arrData[:, 0])]

    if yLim == []:
        yLim = [np.min(arrData[:, 1]), np.max(arrData[:, 1])]

    if zLim == []:
        zLim = [np.min(arrData), np.max(arrData)]

    dctPlotInfo = {
        'dataMin': np.min(arrData[:, 2]),
        'dataMax': np.max(arrData[:, 2]),
        'xMin': xLim[0],
        'xMax': xLim[1],
        'xLabel': xLabel,
        'yMin': yLim[0],
        'yMax': yLim[1],
        'yLabel': yLabel,
        'imagePath': imgPath,
        'colormap': colorMap.toPGF()
    }

    # plot image without boundaries and save it to png
    plt.scatter(
        x=arrData[:, 0],
        y=arrData[:, 1],
        s=arrData[:, 2],
        c=arrData[:, 2],
        cmap=colorMap.obj,
        linewidths=5
    )

    dctPlotInfo.update(themeArgs)

    fig = plt.gcf()
    fig.patch.set_alpha(0)
    a = fig.gca()
    a.set_frame_on(False)
    a.set_xticks([])
    a.set_yticks([])
    plt.axis('off')

    try:
        fig.savefig(
            imgPath + '.png',
            transparent=True,
            bbox_inches='tight',
            pad_inches=0
        )
    except IOError:
        print("Could not write to file " + imgPath + '.png')
    else:
        # call the composition function
        _compose(theme, dctPlotInfo)


if __name__ == "__main__":

    plotFunctions = {
        'heatmap': toHeatmap,
        'scatter': toScatter
    }

    # define and parse arguments
    parser = argparse.ArgumentParser(
        description=r"""Script to convert a large numpy array to a png
    and also generate a tikzpicture, which plots the png with axes
    to be included in a TeX document."""
    )

    parser.add_argument(
        '-s',
        action='store',
        help='Plotting style to use. Currently supported ones: \n' +
        'heatmap, scatter',
        type=str,
        default='heatmap'
    )

    parser.add_argument(
        '-p',
        action="store",
        help='Path to the *.npy file(s) without the file extension',
        nargs='+',
        type=str
    )

    parser.add_argument(
        '-m',
        action="store",
        help='Colormap for the plot; supports all maps of matplotlib',
        default="jet",
        type=str
    )

    parser.add_argument(
        '-t',
        action="store",
        help='TeX template to use',
        default="",
        type=str
    )

    parser.add_argument(
        '-c',
        action='store',
        help='Path to a JSON file containing a colorfy workspace',
        default='',
        type=str
    )

    args = parser.parse_args()

    # paths to the numpy files
    lstPaths = args.p

    # name of the desired colormap
    colorMapName = args.m

    # desired theme-skeleton file
    theme = Theme(args.t + '.tex')

    # check if the functionality is implemented
    try:
        function = plotFunctions[args.s]
    except KeyError:
        print('Requested ' + args.s + ' functionality not implemented.')
        raise(NotImplementedError)
    else:
        # set a maybe desired colorfy workspace
        colorfyWS = args.c

        if colorfyWS == "":
            colorMap = ColorMap(colorMapName)
        else:
            try:
                colorMap = ColorMap(colorMapName, colorfy=colorfyWS)
            except (FileNotFoundError):
                print(
                    'Unable to load colorfy workspace from ' +
                    args.c +
                    '.json'
                )

        # go through all images
        for imgPath in lstPaths:
            try:
                open(imgPath + '.npy')
                # load the numpy array and call the entry point
                # function for it
            except (FileNotFoundError):
                print('File ' + imgPath + '.npy not found.')
            else:
                function(
                    np.load(imgPath + '.npy'),
                    imgPath,
                    theme,
                    colorMap=colorMap,
                )
