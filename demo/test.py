import axify as ax
import numpy as np

# create some random data
data = np.empty((1024,3))
data[:,:2] = np.random.uniform(-1, 1, (1024,2))
data[:,2] = np.random.randn(1024)

# load an axify theme
thme = ax.Theme('simple.tex')

# construct a colormap
cmap = ax.ColorMap('hot')

# write the png and the tex file
ax.toHeatmap(data, 'data', thme, cmap)
