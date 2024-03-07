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
    ax.hist(image.flatten(), bins=(max - min) + 1, range=(min, max))
    ax.set_title(title)


def clip(image):
    """Set all pixel values below zero to zero, and all values above 255 to 255"""
    image[image < 0] = 0
    image[image > 255] = 255
    return image.astype("uint8")


def generate_sample_images(image_size):
    """
    Generate four square sample images

    Parameters
    ----------
    image_size : int
        Each generated image will be 'image_size' pixels wide and 'image_size' pixels high
        The given 'image_size' should be divisible by 2

    Returns
    -------
    list of numpy.ndarray
        List containing four sample images
    """

    # Generate image using gaussian values with large standard deviation
    gauss1 = np.random.normal(255 / 2, 60, size=(image_size, image_size)).astype("uint8")
    # Generate image using gaussian values with small standard deviation
    gauss2 = np.random.normal(255 / 2, 5, size=(image_size, image_size)).astype("uint8")

    # Generate image split into two halves. Both use gaussian values with the same standard
    # deviation but different mean values. Left half - higher mean. Right half - lower mean.
    split1 = clip(
        np.random.normal(255 * 0.75, 20, size=(image_size, image_size // 2)))
    split2 = clip(
        np.random.normal(255 * 0.25, 20, size=(image_size, image_size // 2)))
    combo1 = np.zeros(shape=(image_size, image_size))
    combo1[:, 0:image_size // 2] = split1
    combo1[:, image_size // 2:combo1.shape[1]] = split2

    # Generate image split into quarters. All quarters use gaussian values with the same
    # standard deviation but different mean values. Top left quarter - higher mean.
    # All other quarters - lower mean.
    split1 = clip(
        np.random.normal(255 * 0.75, 20, size=(image_size // 2, image_size // 2)))
    split2 = clip(
        np.random.normal(255 * 0.25, 20, size=(image_size // 2, image_size // 2)))
    combo2 = np.zeros(shape=(image_size, image_size))
    combo2[0:image_size // 2, 0:image_size // 2] = split1
    combo2[image_size // 2:combo2.shape[0], image_size // 2:combo2.shape[1]] = split2
    combo2[image_size // 2:combo2.shape[0], 0:image_size // 2] = split2
    combo2[0:image_size // 2, image_size // 2:combo2.shape[1]] = split2

    return gauss1, gauss2, combo1, combo2


def generate_histogram_exercise_plots(save_dir):
    """
    Generate two plots: one with 4 simple sample images, labelled 1-4 (exercise-hist-images.png),
    and another with corresponding histograms, labelled a-d (exercise-histograms.png). The order of
    histograms and images are randomised, so students can guess which image corresponds to which
    histogram.

    Parameters
    ----------
    save_dir : str
        Path of directory to save plots into. If the directory does not exist a FileNotFoundError is raised.
    """

    # Use a size divisible by 2
    image_size = 60
    sample_images = generate_sample_images(image_size)

    # Plot histograms for each sample image
    fig, [[ax1, ax2], [ax3, ax4]] = plt.subplots(2, 2)
    fig.set_size_inches(9, 5)
    fig.tight_layout()
    # randomise order of axes, so they don't directly correspond to the order of the image axes
    axes = [ax3, ax1, ax4, ax2]
    titles = ["c", "a", "d", "b"]
    for image, ax, title in zip(sample_images, axes, titles):
        plot_histogram(image, 0, 255, ax, title)
    plt.savefig(Path(save_dir) / "exercise-histograms.png", dpi=300)

    # Plot all sample images
    fig, [[ax1, ax2], [ax3, ax4]] = plt.subplots(2, 2)
    # randomise order of axes, so they don't directly correspond to the order of histogram axes
    axes = [ax2, ax3, ax1, ax4]
    titles = ["2", "3", "1", "4"]
    for image, ax, title in zip(sample_images, axes, titles):
        ax.imshow(image, cmap='gray', vmin=0, vmax=255)
        ax.axis('off')
        ax.set_title(title)
    plt.savefig(Path(save_dir) / "exercise-hist-images.png", dpi=300, bbox_inches='tight')