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


r"""
axify – a tool to put axes around plots

As wonderful as TikZ and PGFplots might be, they are not very good at
handling large amounts of data when it comes to plotting. High resolution
heatmaps or large scale scatter plots tend to be a problem, because soon
PGFplots runs out of memory plotting them natively. And even if it still
can handle the large plots, compilation might still take a long time if
several plots are present in the document.

Dependencies:
  * colorfy

Usage:
  If you want to use axify from within python, the simplest way to use it
  is to do the following:

  >>> import axify as ax
  >>> import numpy as np

  >>> # create some random data
  >>> data = np.random.randn(1024, 1024)

  >>> # load an axify theme
  >>> thme = ax.Theme('simple.tex')

  >>> # construct a colormap
  >>> cmap = ax.Colormap('hot')

  >>> # write the png and the tex file
  >>> ax.toHeatmap(data, 'data', thme, cmap)

  which generates the files data.png and data.tex from this given Numpy array
  and can be included into a TeX-document very easily. Here the file
  'simple.tex' could look like this:

  \begin{tikzpicture}
  \begin{axis}[
    enlargelimits = false,
    axis on top = true,
    axis equal image,
    point meta min = %(dataMin)f,
    point meta max = %(dataMax)f,
    colorbar horizontal,
    %(colormap)s,
    ]
    \addplot graphics [
      xmin = %(xMin)f,
      xmax = %(xMax)f,
      ymin = %(yMin)f,
      ymax = %(yMax)f
    ] {%(imagePath)s};
    \end{axis}
  \end{tikzpicture}

  Theme files may contain the following variables which are known by axify:

    * dataMin – minimum value of given data
    * dataMax – maximum value of given data
    * xMin – minimum x value
    * xMax – maximum x value
    * xLabel
    * yMin – minimum y value
    * yMax – maximum y value
    * yLabel
    * imagePath – path to the rendered png
    * colormap – defining text of the colormap

  Moreover, there is colorfy support, which allows to import colormaps that
  follow a certain scheme. So let's assume, we have a file colors.json
  containting the following definitions:

  {
      "colors" : {
          "col1" : {
              "space": "rgb",
              "def": [1, 0.5, 0.75]
              }
          ,
          "col2" : {
              "space": "rgb",
              "def": [0.5, 1, 0.5]
          }
      },
      "colorbars": {
          "triple": {
              "def": ["col1", "col2", "col1"],
              "pos": [0, 0.2, 1]
          }
      }
  }

  The we could use the following code, to make use of the colorbar 'triple':

  >>> import axify as ax
  >>> import numpy as np

  >>> # create some random data
  >>> data = np.random.randn(1024, 1024)

  >>> # load an axify theme
  >>> thme = ax.Theme('simple.tex')

  >>> # construct a colormap
  >>> cmap = ax.Colormap('triple', colorfy='colors')

  >>> # write the png and the tex file
  >>> ax.toHeatmap(data, 'data', thme, cmap)

  Again, this results in two files data.png and data.tex, but now data.tex
  makes use of the colorbar defined in 'colors.json'.
"""


from .axify import Theme
from .axify import ColorMap
from .axify import toHeatmap
from .axify import toScatter
