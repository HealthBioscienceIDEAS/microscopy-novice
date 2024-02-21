from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib
import numpy as np

matplotlib.use('Qt5Agg')


def plot_histogram(image, min, max, ax, title, alpha=1):
    ax.set_xlim(min, max)
    ax.hist(image.flatten(), bins=(max - min) + 1, range=(min, max), alpha=alpha)
    ax.set_title(title, fontsize=10)


def generate_snr_comparison_plots(save_dir):
    """Generate two diagrams for signal to noise ratio. One represents a low signal to noise scenario, the other a
    high signal to noise scenario. For each there are three histograms - left, no noise. Middle, with noise (separate
    histograms). Right, with noise (combined histogram)"""

    centres = [[20, 30], [80, 120]]
    names = ["low", "high"]

    for centre, name in zip(centres, names):
        fig, all_axes = plt.subplots(1, 3)
        fig.set_size_inches(10, 2)

        min = 0
        max = 255
        st_dev = 10
        n_values = 1000

        lows = np.random.normal(centre[0], 0, size=n_values)
        highs = np.random.normal(centre[1], 0, size=n_values)
        lows_with_noise = np.random.normal(centre[0], st_dev, size=(n_values, 1))
        highs_with_noise = np.random.normal(centre[1], st_dev, size=(n_values, 1))

        plot_histogram(np.concatenate((lows, highs)), min, max, all_axes[0], "no noise")
        plot_histogram(lows_with_noise, min, max, all_axes[1], "with noise (separate histograms)", alpha=0.5)
        plot_histogram(highs_with_noise, min, max, all_axes[1], "with noise (separate histograms)", alpha=0.5)
        plot_histogram(np.concatenate((lows_with_noise, highs_with_noise)), min, max, all_axes[2],
                       "with noise (combined histogram)")

        plt.savefig(Path(save_dir) / f"snr-comparison-{name}.png", dpi=300, bbox_inches='tight')