from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import scipy.stats as stats

matplotlib.use('Qt5Agg')


def plot_1d_gauss(ax, sigma):
    """
    Plot 1D gaussian function on given matplotlib axes

    Parameters
    ----------
    ax : matplotlib axes
        Axes to plot onto
    sigma : float
        Sigma of gaussian function
    """

    # assume mean of zero
    mu = 0
    # plot three standard deviations (sigma) away from the mean
    x = np.linspace(mu - 3 * sigma, mu + 3 * sigma, 100)
    ax.plot(x, stats.norm.pdf(x, mu, sigma), label=sigma)


def plot_2d_gauss(ax, sigma, xy_min=None, xy_max=None, z_max=None):
    """
    Plot 2D gaussian function on given matplotlib axes

    Parameters
    ----------
    ax : matplotlib axes
        Axes to plot onto
    sigma : float
        Sigma of gaussian function
    xy_min: float
        Minimum of x and y axes
    xy_max : float
        Maximum of x and y axes
    z_max : float
        Maximum of z axis
    """

    # assume mean of zero
    mu = 0
    n = 100

    # plot three standard deviations (sigma) away from the mean in x and y
    x = np.linspace(mu - 3 * sigma, mu + 3 * sigma, n)
    y = np.linspace(mu - 3 * sigma, mu + 3 * sigma, n)
    x, y = np.meshgrid(x, y)

    z = np.exp(-(x * x + y * y) / (2 * sigma * sigma))
    z = z / (2 * np.pi * sigma * sigma)

    ax.plot_surface(x, y, z, rstride=1, cstride=1, linewidth=0, antialiased=False, cmap=plt.cm.viridis)

    if xy_min is not None and xy_max is not None:
        ax.set_xlim(xy_min, xy_max)
        ax.set_ylim(xy_min, xy_max)

    if z_max is not None:
        ax.set_zlim(0, z_max)

    # Remove tick labels on all axes
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    ax.set_zticklabels([])


def generate_gauss_plots(save_dir):
    """
    Generate two plots - a 1D gaussian with three sigma values (gaussian-1d-comparison.png), and a
    2D gaussian with three sigma values (gaussian-2d-comparison.png)

    Parameters
    ----------
    save_dir : str
        Path of directory to save plots into. If the directory does not exist a FileNotFoundError is raised.
    """

    # Plot 1D gaussian with three sigma values
    fig, ax = plt.subplots()
    fig.set_size_inches(6, 3)

    sigmas = [2, 4, 6]
    for sigma in sigmas:
        plot_1d_gauss(ax, sigma)

    ax.legend(title="sigma")
    plt.savefig(Path(save_dir) / "gaussian-1d-comparison.png", dpi=300, bbox_inches='tight')

    # Plot 2D gaussian with three sigma values
    sigmas = [2, 2.5, 3]
    fig, all_axes = plt.subplots(1, 3, subplot_kw={"projection": "3d", "elev": 30})
    fig.set_size_inches(8, 3)

    # Limit the x and y axis at 3 times the largest standard deviation (sigma) away from the mean
    xy_max = 3 * sigmas[-1]
    xy_min = -xy_max

    for ax, sigma in zip(all_axes, sigmas):
        plot_2d_gauss(ax, sigma, xy_min, xy_max, z_max=0.03)

    fig.suptitle(r'$\text{increasing sigma}\longrightarrow$')
    plt.savefig(Path(save_dir) / "gaussian-2d-comparison.png", dpi=300, bbox_inches='tight')