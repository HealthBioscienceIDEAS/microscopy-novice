from pathlib import Path

import matplotlib.pyplot as plt
from skimage import data
import matplotlib

# Based on updating histogram colours:
# https://matplotlib.org/stable/gallery/statistics/hist.html#sphx-glr-gallery-statistics-hist-py

matplotlib.use('Qt5Agg')


def plot_histogram(image, min, max, title, cmap, ax):

    ax.set_xlim(min, max)

    # hide x ticks
    ax.tick_params(bottom=False)
    ax.xaxis.set_ticklabels([])
    ax.set_title(title)

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


def generate_colormap_plot(save_dir):
    """Generate plot with 4 histograms and corresponding colorbars"""

    fig, [[ax1, ax2], [ax3, ax4]] = plt.subplots(2, 2)
    fig.set_size_inches(9, 5)
    image = data.coins()
    min = 0
    max = 255
    axes = [ax1, ax2, ax3, ax4]
    cmaps = [plt.cm.gray, plt.cm.Greens, plt.cm.viridis, plt.cm.inferno]
    titles = ["gray", "green", "viridis", "inferno"]

    for ax, cmap, title in zip(axes, cmaps, titles):
        plot_histogram(image, min, max, title, cmap, ax)

    plt.savefig(Path(save_dir) / "colorbar-comparison.png", dpi=300)

