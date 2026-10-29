from pathlib import Path

import matplotlib.pyplot as plt
from skimage import data
import matplotlib

matplotlib.use('Qt5Agg')


def plot_histogram(image, min, max, title, cmap, ax):
    """
    Plot image histogram on given matplotlib axes

    Based on updating histogram colours:
    https://matplotlib.org/stable/gallery/statistics/hist.html#sphx-glr-gallery-statistics-hist-py

    Parameters
    ----------
    image : numpy.ndarray
        Image to calculate histogram from
    min : int
        Histogram minimum (x axis)
    max : int
        Histogram maximum (x axis)
    title : str
        Title to display on the histogram's y axis
    cmap : matplotlib colormap
        Colormap to colour histogram with
    ax : matplotlib axes
        Axes to plot histogram onto
    """
    ax.set_xlim(min, max)
    ax.set_ylabel(title, x=-0.3, y=0.3)

    # hide x ticks
    ax.tick_params(bottom=False)
    ax.xaxis.set_ticklabels([])

    n, bin_edges, patches = ax.hist(image.flatten(), bins=(max - min) + 1, range=(min, max))

    # Want to colour based on centre value of each bin
    bin_centres = (bin_edges[:-1] + bin_edges[1:]) / 2

    # find fraction of max
    fracs = bin_centres / max

    # Now, we'll loop through our objects and set the color of each accordingly
    for frac, patch in zip(fracs, patches):
        color = cmap(frac)
        patch.set_facecolor(color)

    norm = matplotlib.colors.Normalize(min, max)
    plt.colorbar(matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap),
                 orientation='horizontal', ax=ax, pad=0.05)


def plot_image(image, min, max, cmap, ax):
    """
    Plot an image on the given matplotlib axis

    Parameters
    ----------
    image : numpy.ndarray
        Image to plot
    min : int
        Contrast minimum
    max : int
        Contrast maximum
    cmap : matplotlib colormap
        Colormap to use on image
    ax : matplotlib axes
        Axes to plot the image onto
    """
    ax.imshow(image, cmap=cmap, vmin=min, vmax=max)
    ax.axis('off')


def generate_colormap_plot(save_dir):
    """
    Generate a plot (colorbar-comparison.png) showing the 'coins' sample image using four different colormaps.
    Each row displays a coloured histogram and corresponding image for each colormap.

    Parameters
    ----------
    save_dir : str
        Path of directory to save plots into. If the directory does not exist a FileNotFoundError is raised.
    """

    fig, all_axes = plt.subplots(4, 2)
    fig.subplots_adjust(hspace=0.3, wspace=0)
    fig.set_size_inches(6, 9)
    image = data.coins()
    min = 0
    max = 255
    cmaps = [plt.cm.gray, plt.cm.Greens, plt.cm.viridis, plt.cm.inferno]
    titles = ["gray", "green", "viridis", "inferno"]

    for axis_pair, cmap, title in zip(all_axes, cmaps, titles):
        image_axis = axis_pair[1]
        hist_axis = axis_pair[0]

        plot_histogram(image, min, max, title, cmap, hist_axis)
        plot_image(image, min, max, cmap, image_axis)

    plt.savefig(Path(save_dir) / "colorbar-comparison.png", dpi=200, bbox_inches='tight')

