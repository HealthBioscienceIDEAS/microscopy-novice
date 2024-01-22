from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import skimage.data as data

matplotlib.use('Qt5Agg')


def plot_image(image, min, max, cmap, ax, title):
    ax.imshow(image, cmap=cmap, vmin=min, vmax=max)
    ax.axis('off')
    ax.set_title(title, fontsize=10)


def generate_image_with_noise(save_dir):
    """Generate plot with two images. Left - a standard image of nuclei. Right - the same image with added noise"""

    cells = data.cells3d()
    nucleus = cells[30, 1, :, :]

    nucleus_noisy = nucleus + np.random.normal(scale=5000.0, size=nucleus.shape)

    fig, all_axes = plt.subplots(1, 2)
    fig.set_size_inches(5, 2)

    min = 0
    max = 65535
    plot_image(nucleus, min, max, plt.cm.gray, all_axes[0], "nuclei image")
    plot_image(nucleus_noisy, min, max, plt.cm.gray, all_axes[1], "nuclei image with added noise")

    plt.savefig(Path(save_dir) / f"image-with-noise.png", dpi=300, bbox_inches='tight')