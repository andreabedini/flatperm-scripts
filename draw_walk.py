import numpy as np

from matplotlib.path import Path
from matplotlib.patches import PathPatch
from matplotlib import pyplot as plt

def midpoint(a, b):
    return tuple([(x_y[0] + x_y[1]) / 2. for x_y in zip(a, b)])

def read_walks(filename):
    data = np.loadtxt(filename)
    for n, m, *points in data:
        yield n, m, np.array(points).reshape(-1,2)

def walk_to_patch(points):
    verts = []
    codes = []

    verts.append( points[0] ); codes.append( Path.MOVETO )

    for x,y,z in zip(points[0:], points[1:], points[2:]):
        codes.append( Path.CURVE4 ); verts.append( y )
        codes.append( Path.CURVE4 ); verts.append( y )
        codes.append( Path.CURVE4 ); verts.append( midpoint(y,z) )
    
    codes.append( Path.LINETO ); verts.append( z )
    
    path = Path(verts, codes)
    return PathPatch(path, fill=None, lw=1)

def draw_walk(points, ax = None):

    verts = []
    codes = []

    verts.append( points[0] ); codes.append( Path.MOVETO )

    for x,y,z in zip(points[0:], points[1:], points[2:]):
        codes.append( Path.CURVE4 ); verts.append( y )
        codes.append( Path.CURVE4 ); verts.append( y )
        codes.append( Path.CURVE4 ); verts.append( midpoint(y,z) )
    
    codes.append( Path.LINETO ); verts.append( z )
    
    path = Path(verts, codes)

    xmax, ymax = np.max(verts, axis=0)
    xmin, ymin = np.min(verts, axis=0)

    if not ax:
        fig = plt.figure()
        ax = fig.add_subplot(111, xticks=[], yticks=[], frame_on=False, aspect=1)

    patch = PathPatch(path, fill=None, lw=1)
    ax.add_patch(patch)
    ax.set_xlim(xmin - 1, xmax + 1)
    ax.set_ylim(ymin - 1, ymax + 1)
