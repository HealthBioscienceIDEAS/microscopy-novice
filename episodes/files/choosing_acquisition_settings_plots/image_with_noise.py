from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import skimage.data as data

matplotlib.use('Qt5Agg')


def plot_image(image, min, max, cmap, ax, title):
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
    ax :  matplotlib axes
        Axes to plot the image onto
    title : str
        Title to display above image
    """
    ax.imshow(image, cmap=cmap, vmin=min, vmax=max)
    ax.axis('off')
    ax.set_title(title, fontsize=10)


def generate_image_with_noise(save_dir):
    """
    Generate plot ('image-with-noise.png') with two images. Left - a standard image of nuclei.
    Right - the same image with added noise.

    Parameters
    ----------
    save_dir : str
        Path of directory to save plots into. If the directory does not exist a FileNotFoundError is raised.
    """

    cells = data.cells3d()
    nucleus = cells[30, 1, :, :]

    nucleus_noisy = nucleus + np.random.normal(scale=5000.0, size=nucleus.shape)

    fig, all_axes = plt.subplots(1, 2)
    fig.subplots_adjust(wspace=0)
    fig.set_size_inches(5, 2)

    min = 0
    max = 29713
    plot_image(nucleus, min, max, plt.cm.gray, all_axes[0], "nuclei image")
    plot_image(nucleus_noisy, min, max, plt.cm.gray, all_axes[1], "nuclei image with added noise")

    plt.savefig(Path(save_dir) / f"image-with-noise.png", dpi=300, bbox_inches='tight')