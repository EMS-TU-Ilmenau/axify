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

## Usage

It is very easy. Invoking `python axify -h` tells you what to do.
