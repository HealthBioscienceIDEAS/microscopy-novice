from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib
import numpy as np

matplotlib.use('Qt5Agg')


def plot_histogram(image, min, max, ax, title):
    """
    Plot image histogram on given matplotlib axes

    Parameters
    ----------
    image : numpy.ndarray
        Image to calculate histogram from
    min : int
        Histogram minimum (x axis)
    max : int
        Histogram maximum (x axis)
    ax : matplotlib axes
        Axes to plot histogram onto
    title : str
        Title to display above histogram
    """
    ax.set_xlim(min, max)
    ax.hist(image.flatten(), bins=(max - min) + 1, range=(min, max), color="#1f77b4")
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.set_title(title, fontsize=10)


def clip(values, min, max):
    """Remove any values outside of the range min to max"""
    values[values < min] = min
    values[values > max] = max
    return values


def generate_qc_histogram_exercise(save_dir):
    """
    Generate plot ('exercise-qc-histograms.png') showing 4 example acquisition histograms, labelled a-d

    Parameters
    ----------
    save_dir : str
        Path of directory to save plots into. If the directory does not exist a FileNotFoundError is raised.
    """

    fig, [[ax1, ax2], [ax3, ax4]] = plt.subplots(2, 2)
    fig.set_size_inches(9, 5)
    fig.tight_layout()
    titles = ["a", "b", "c", "d"]
    axes = [ax1, ax2, ax3, ax4]

    # Centre of normal distributions for each axis
    centres = [[70], [125], [220], [50, 150]]
    # Standard deviation of normal distributions for each axis
    st_devs = [[10], [35], [30], [10, 30]]
    min = 0
    max = 255
    n_values = 10000

    for ax, title, centre, st_dev in zip(axes, titles, centres, st_devs):
        for c, s in zip(centre, st_dev):
            values = np.random.normal(c, s, size=(n_values, 1))
            plot_histogram(clip(values, min, max), min, max, ax, title)

    plt.savefig(Path(save_dir) / "exercise-qc-histograms.png", dpi=300)