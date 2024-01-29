from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib
import numpy as np

matplotlib.use('Qt5Agg')


def plot_2d_gauss(ax, sigma, n=150):

    x = np.arange(-n, n+1, 1)
    y = np.arange(-n, n+1, 1)
    x, y = np.meshgrid(x, y)

    z = np.exp(-(x*x + y*y)/(2*sigma*sigma))
    z = z / z.max()

    ax.plot_surface(x, y, z, rstride=1, cstride=1, linewidth=0, antialiased=False, cmap=plt.cm.viridis)
    ax.axis(False)


def generate_gauss_plots(save_dir):
    """generate one plot with a 2D gaussian function and another with three 2D gaussian functions with increasing
    sigma values"""

    fig, ax = plt.subplots(1, 1, subplot_kw={"projection": "3d", "elev": 30})
    fig.set_size_inches(3, 3)
    plot_2d_gauss(ax, 10, n=50)
    plt.savefig(Path(save_dir) / "gaussian-kernel.png", dpi=300, bbox_inches='tight')

    fig, all_axes = plt.subplots(1, 3, subplot_kw={"projection": "3d", "elev": 30})
    fig.subplots_adjust(wspace=0, hspace=0)
    fig.set_size_inches(8, 3)

    sigmas = [15, 30, 70]

    for ax, sigma in zip(all_axes, sigmas):
        plot_2d_gauss(ax, sigma)

    fig.suptitle(r'$\text{increasing sigma}\longrightarrow$')

    plt.savefig(Path(save_dir) / "gaussian-kernel-comparison.png", dpi=300, bbox_inches='tight')