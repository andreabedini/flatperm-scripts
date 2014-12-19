from . import flatperm2
import pylab as plt
import numpy as np
from matplotlib.widgets import Slider, Button, RadioButtons

def plot(Z):
    ax = plt.subplot(111)
    plt.subplots_adjust(bottom=0.25)
    ax.contour(flatperm2.pd(Z, 1, 1).T)
    
    ax1 = plt.axes([0.125, 0.15, 0.775, 0.03])
    ax2 = plt.axes([0.125, 0.05, 0.775, 0.03])

    s1 = Slider(ax1, r'$\omega_1$', 0.1, 30.0, valinit=1)
    s2 = Slider(ax2, r'$\omega_2$', 0.1, 10.0, valinit=1)
    
    plt.show()

    def update(val):
        w1 = s1.val
        w2 = s2.val
        print((w1, w2))
        ax.clear()
        ax.contour(flatperm2.pd(Z, w1, w2).T)
        # l.set_ydata(amp*sin(2*pi*freq*t))
        plt.draw()

    s1.on_changed(update)
    s2.on_changed(update)

    return

    resetax = axes([0.8, 0.025, 0.1, 0.04])
    button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')
    def reset(event):
        sfreq.reset()
        samp.reset()
    button.on_clicked(reset)

    rax = axes([0.025, 0.5, 0.15, 0.15], axisbg=axcolor)
    radio = RadioButtons(rax, ('red', 'blue', 'green'), active=0)
    def colorfunc(label):
        l.set_color(label)
        draw()
    radio.on_clicked(colorfunc)

    show()

