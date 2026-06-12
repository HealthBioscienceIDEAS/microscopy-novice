from pathlib import Path

import matplotlib.pyplot as plt
from skimage import data
import matplotlib
import numpy as np

matplotlib.use('Qt5Agg')


def plot_histogram(image, ax, min, max, contrast_min, contrast_max, cmap, hide_x_ticks=True):
    """
    Plot image histogram on given matplotlib axes

    Based on updating histogram colours:
    https://matplotlib.org/stable/gallery/statistics/hist.html#sphx-glr-gallery-statistics-hist-py
    + https://stackoverflow.com/questions/14777066/matplotlib-discrete-colorbar

    Parameters
    ----------
    image : numpy.ndarray
        Image to calculate histogram from
    ax : matplotlib axes
        Axes to plot histogram onto
    min : int
        X axis minimum
    max : int
        X axis maximum
    contrast_min : int
        Contrast minimum (i.e. pixel value colormap begins at)
    contrast_max : int
        Contrast maximum (i.e. pixel value colormap ends at)
    cmap : matplotlib colormap
        Colormap to colour histogram with
    hide_x_ticks : bool
        Whether to hide ticks on the x axis
    """
    ax.set_xlim(min, max)

    if hide_x_ticks:
        ax.tick_params(bottom=False)
        ax.xaxis.set_ticklabels([])

    n_bins = (max - min) + 1
    n, bin_edges, patches = ax.hist(image.flatten(),
                                    bins=n_bins,
                                    range=(min, max))

    # Want to colour based on centre value of each bin
    bin_centres = (bin_edges[:-1] + bin_edges[1:]) / 2

    # find fraction of max
    fracs = (bin_centres - contrast_min) / (contrast_max - contrast_min)

    # Now, we'll loop through our objects and set the color of each accordingly
    for frac, patch in zip(fracs, patches):
        color = cmap(frac)
        patch.set_facecolor(color)

    edges_colormap = np.linspace(contrast_min, contrast_max, num=n_bins + 1)
    # extract all colors from the cmap
    cmaplist = [cmap(i) for i in range(cmap.N)]

    # Add extra bin + colour for the min
    if contrast_min != min:
        edges_colormap = np.insert(edges_colormap, 0, min)
        cmaplist.insert(0, cmaplist[0])
        ax.axvline(x=contrast_min)

    # Add extra bin + colour for the max
    if contrast_max != max:
        edges_colormap = np.append(edges_colormap, max)
        cmaplist.append(cmaplist[-1])
        ax.axvline(x=contrast_max)

    new_cmap = matplotlib.colors.LinearSegmentedColormap.from_list(
        'Custom cmap', cmaplist, len(cmaplist))
    norm = matplotlib.colors.BoundaryNorm(edges_colormap, len(cmaplist))

    cb = plt.colorbar(matplotlib.cm.ScalarMappable(norm=norm, cmap=new_cmap),
                      orientation='horizontal', ax=ax, spacing='proportional',
                      ticks=[0, 50, 100, 150, 200, 250], boundaries=edges_colormap,
                      pad=0.05)

    cb.ax.xaxis.set_ticks([], minor=True)


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


def generate_contrast_plot(save_dir):
    """
    Generate multiple plots of the 'coins' sample image with different contrast settings
    (named 'contrast-comparison-{contrast_min}-{contrast_max}.png). Each shows a coloured histogram, colorbar and
    corresponding image.

    Parameters
    ----------
    save_dir : str
        Path of directory to save plots into. If the directory does not exist a FileNotFoundError is raised.
    """

    image = data.coins()
    cmap = plt.cm.gray
    min = 0
    max = 255
    contrast_mins = [0, 150, 150]
    contrast_maxes = [255, 255, 200]

    for contrast_min, contrast_max in zip(contrast_mins, contrast_maxes):
        fig, axes = plt.subplots(1, 2)
        fig.subplots_adjust(wspace=0.05)
        fig.set_size_inches(8, 3)
        plot_histogram(image, axes[0], min, max, contrast_min, contrast_max, cmap)
        plot_image(image, contrast_min, contrast_max, cmap, axes[1])
        plt.savefig(Path(save_dir) / f"contrast-comparison-{contrast_min}-{contrast_max}.png",
                    dpi=300, bbox_inches='tight')
