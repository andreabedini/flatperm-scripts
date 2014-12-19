#!/usr/bin/env python


import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import argparse
import os.path
import sys
import numpy as np
import pylab as plt
from tables import openFile

title = 'specific heat'

def do_plot(hf):
    s = hf.title + "\n"
    att = hf.root._v_attrs
    for a in att._v_attrnamesuser:
        s = s + "{}: {}\n".format(a, att[a])

    variables = [ node for node in hf.iterNodes('/', classname = 'Group')
                  if '_analysis' in node._v_name ]

    for variable in variables:
        variable_name = variable._v_name.split('_')[0]

        ax = plt.figure().add_subplot(111)
        ax.plot(variable.c[:], label=variable_name)
        ax.set_xlabel(r'$n$')
        ax.set_ylabel(r'$c_n$')
        ax.set_title('{}: {}'.format(hf.title, title))

        ax.legend(loc = 0)
        ax.text(0.95, 0.5, s, transform = ax.transAxes, ha = 'right')
        basename = os.path.splitext(os.path.basename(hf.filename))[0]
        fn = '{}.{}.{}.pdf'.format(basename, title.replace(' ', '_'), variable_name)
        print(('saving figure in ' + fn))
        plt.savefig(fn)

if __name__ == '__main__':
    from contextlib import closing
    parser = argparse.ArgumentParser()
    for filename in sys.argv[1:]:
        with closing(openFile(filename)) as hf:
            do_plot(hf)
