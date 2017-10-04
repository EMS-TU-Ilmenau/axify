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
In you main document you should make sure that you satisfy all dependencies by 
adding
```
\usepackage{pgfplots}
\pgfplotsset{compat=1.15}
\usepgfplotslibrary{colormaps}
```
in your preamble. The rest is very easy. Invoking `python axify -h` tells you 
what to do. The provided example can be procssed by calling 

`python axify -p test tist -m jet -t simple && pdflatex main`

from your favourite shell.
