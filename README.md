[![Documentation Status](https://readthedocs.org/projects/axify/badge/?version=latest)](https://axify.readthedocs.io/en/latest/?badge=latest)

# axify

## Introduction

This little tool provides the means of easily creating TeX code for plotting
large 2D arrays, which are provided in as a saved numpy array. This alleviates
the drawback, that PGFplots quickly runs out of memory, when plotting large
2D heatmaps. We work around this by just plotting the numpy array to a pdf,
which is then embedded into a tikzpicture.

This approach yields the following goodies:
    1. We are able to generate large annotated heat plots at all!
    2. We save compilation time of the global TeX document, since the heatplots
       themselves are "cached".
    3. The generated *.tex files are very selfcontained and can be placed
       anywhere in your document without restrictions

## Usage

### From the Shell
In you main document you should make sure that you satisfy all dependencies by
adding
```
\usepackage{pgfplots}
\pgfplotsset{compat=1.15}
\usepgfplotslibrary{colormaps}
```
in your preamble. The rest is very easy. Invoking `python axify -h` tells you
what to do. Assume we have two files called 'test1.npy' and 'test2.npy'
containing 2D ndarrays. Then we can axify them via

`python axify.py -p test1 test2 -m jet -s heatmap -t simple`

from our favourite shell. This will make use of the 'jet' colormap and the
theme in the file 'simple.tex'. After issuing this command, we should find four
new files, namely `test1.png`, `test1.tex`, `test2.png` and `test2.tex`, where
the images contain heatmap plots of the given data and the TeX files ready to
include TeX-Code, which you can place freely in your document.

### From within Python

One can also make use of axify directly without first writing data to disk,
by using it as a module. To do so, please import via `import axify` and then
carefully study the output of `help(axify)`.
