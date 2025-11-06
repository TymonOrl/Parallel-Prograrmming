import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector
import sys
import os
sys.path.insert(0, os.path.abspath("Parallel-Prograrmming/mandelbrot_set/build")) 

import mandelbrotCalc

class MandelbrotVisualisation:
    def __init__(self,
                 width=800, height=600,
                 a_min=-2.0, a_max=2.0,
                 b_min=-1.5, b_max=1.5,
                 max_iteration=10, inf_cap=16):
        self.width = width
        self.height = height
        self.initial_bounds = [a_min, a_max, b_min, b_max] 
        self.bounds = [a_min, a_max, b_min, b_max]
        self.max_it = max_iteration
        self.inf_cap = inf_cap
        self.fig, self.ax = plt.subplots()
        self.img = None

        # Drag-to-zoom rectangle
        self.selector = RectangleSelector(
            self.ax, self.on_select,
            useblit=True, button=[1],
            interactive=False, minspanx=5, minspany=5, spancoords='pixels'
        )

        # Mouse + keyboard
        self.cid_scroll = self.fig.canvas.mpl_connect('scroll_event', self.on_scroll)
        self.cid_key    = self.fig.canvas.mpl_connect('key_press_event', self.on_key)

        self.redraw()

    def _title(self):
        a_min, a_max, b_min, b_max = self.bounds
        return f"Section  x=[{a_min:.3f},{a_max:.3f}]  y=[{b_min:.3f},{b_max:.3f}]"

    def compute(self):
        # computes iterations for each pixel
        a_min, a_max, b_min, b_max = self.bounds
        # C++ compiled code
        img = mandelbrotCalc.mandelbrotCalc(width = self.width, height = self.height,
                          a_min = a_min, a_max = a_max,
                          b_min = b_min, b_max = b_max,
                          max_iteration = self.max_it, inf_cap = self.inf_cap)
        return img

    def redraw(self):
        img = self.compute()
        a_min, a_max, b_min, b_max = self.bounds
        if self.img is None:
            self.img = self.ax.imshow(
                img, origin='lower', cmap='bone', #bone
                vmin=-30, vmax=self.max_it,
                extent=[a_min, a_max, b_min, b_max],
                interpolation='nearest',
                aspect='auto', 
            )
        else:
            self.img.set_data(img)
            self.img.set_extent([a_min, a_max, b_min, b_max])

        self.ax.set_title(self._title())
        self.ax.set_xlabel("Drag or Scroll to zoom  | h: reset, backspace: zoom out")
        self.ax.figure.canvas.draw_idle()

    # --- interactions ---
    def on_select(self, e0, e1):
        if e0.xdata is None or e1.xdata is None:
            return
        x0, y0, x1, y1 = e0.xdata, e0.ydata, e1.xdata, e1.ydata
        self.bounds = [min(x0, x1), max(x0, x1), min(y0, y1), max(y0, y1)]
        self.redraw()

    def on_scroll(self, event):
        if event.xdata is None or event.ydata is None:
            return
        factor = 0.8 if event.button == 'up' else 1/0.8
        a_min, a_max, b_min, b_max = self.bounds
        cx, cy = event.xdata, event.ydata
        dx = (a_max - a_min) * factor * 0.5
        dy = (b_max - b_min) * factor * 0.5
        self.bounds = [cx - dx, cx + dx, cy - dy, cy + dy]
        self.redraw()

    def on_key(self, event):
        a_min, a_max, b_min, b_max = self.bounds
        if event.key == 'h':  # reset to default view
            self.bounds = self.initial_bounds.copy()
            self.redraw()
        elif event.key == 'backspace':  # zoom out x2
            cx = 0.5*(a_min+a_max); cy = 0.5*(b_min+b_max)
            dx = (a_max - a_min);   dy = (b_max - b_min)
            self.bounds = [cx - dx, cx + dx, cy - dy, cy + dy]
            self.redraw()


if __name__ == "__main__":
    viewer = MandelbrotVisualisation(
                 width=1980, height=1080,
                 a_min=-2, a_max=2,
                 b_min=-1.5, b_max=1.5,
                 max_iteration=255, inf_cap=1000)
    plt.show()
