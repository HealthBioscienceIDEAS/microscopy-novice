from pathlib import Path

import matplotlib.pyplot as plt
from skimage import data
import matplotlib
import numpy as np
import napari

# Based on updating histogram colours:
# https://matplotlib.org/stable/gallery/statistics/hist.html#sphx-glr-gallery-statistics-hist-py

matplotlib.use('Qt5Agg')


def plot_histogram(image, min, max, ax, title):
    ax.set_xlim(min, max)
    ax.hist(image.flatten(), bins=(max - min) + 1, range=(min, max))
    ax.set_title(title)


def clip(image):
    image[image < 0] = 0
    image[image > 255] = 255
    return image.astype("uint8")


def generate_histogram_exercise_plots(save_dir):
    # Use a size divisible by 2
    image_size = 60

    gauss1 = np.random.normal(255/2, 60, size=(image_size, image_size)).astype("uint8")
    gauss2 = np.random.normal(255/2, 5, size=(image_size, image_size)).astype("uint8")

    split1 = clip(
        np.random.normal(255*0.75, 20, size=(image_size, image_size//2)))
    split2 = clip(
        np.random.normal(255*0.25, 20, size=(image_size, image_size//2)))
    combo1 = np.zeros(shape=(image_size, image_size))
    combo1[:, 0:image_size//2] = split1
    combo1[:, image_size//2:combo1.shape[1]] = split2

    split1 = clip(
        np.random.normal(255*0.75, 20, size=(image_size//2, image_size//2)))
    split2 = clip(
        np.random.normal(255*0.25, 20, size=(image_size//2, image_size//2)))
    combo2 = np.zeros(shape=(image_size, image_size))
    combo2[0:image_size//2, 0:image_size//2] = split1
    combo2[image_size//2:combo2.shape[0], image_size//2:combo2.shape[1]] = split2
    combo2[image_size//2:combo2.shape[0], 0:image_size//2] = split2
    combo2[0:image_size//2, image_size//2:combo2.shape[1]] = split2

    fig, [[ax1, ax2], [ax3, ax4]] = plt.subplots(2, 2)
    fig.set_size_inches(9, 5)
    fig.tight_layout()
    images = [gauss1, gauss2, combo1, combo2]
    axes = [ax3, ax1, ax4, ax2]
    titles = ["c", "a", "d", "b"]
    for image, ax, title in zip(images, axes, titles):
        plot_histogram(image, 0, 255, ax, title)
    plt.savefig(Path(save_dir) / "exercise-histograms.png", dpi=300)

    fig, [[ax1, ax2], [ax3, ax4]] = plt.subplots(2, 2)
    axes = [ax2, ax3, ax1, ax4]
    titles = ["2", "3", "1", "4"]
    for image, ax, title in zip(images, axes, titles):
        ax.imshow(image, cmap='gray', vmin=0, vmax=255)
        ax.axis('off')
        ax.set_title(title)
    plt.savefig(Path(save_dir) / "exercise-hist-images.png", dpi=300, bbox_inches='tight')