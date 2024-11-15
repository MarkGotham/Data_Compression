# -*- coding: utf-8 -*-
from typing import Union
import matplotlib.pyplot as plt
import pandas as pd

from pathlib import Path
THIS_DIR = Path(__file__).parent


def plot_rgb_csv(
    file_path: Union[str, Path] = THIS_DIR / "data" / "rgb.csv",
    x_label: Union[str, None] = "Wavelength $\lambda$",
    y_labels: Union[list, None] = None,
    write_not_show: bool = True,
    write_path: Union[Path, str] = THIS_DIR / "plots" / "rgb_data.pdf"
) -> None:
    """
    Plots cone spectral sensitivities data after Stockman & Sharpe (2000)
    from a CSV file hosted locally.

    :param file_path: Path to the CSV file (Path or str). Default provided.
    :param x_label: Label for the x-axis (str, optional). Default provided is "Wavelength $\lambda$".
    :param y_labels: List of labels for the y-axes (List[str], optional). Default given as ["R", "G", "B"].
    :param write_not_show: If True (default), write, using the `write_path`. If False, then show.
    :param write_path: Path and file name to write to.
    """

    # Load data from CSV file
    if y_labels is None:
        y_labels = ["R", "G", "B"]

    df = pd.read_csv(
        file_path,
        header=None,
        names=["x"] + y_labels
    )

    fig, ax = plt.subplots()
    for i in range(3):

        tag = y_labels[i]
        ax.plot(
            df["x"],
            df[tag],
            label=tag + " data",
            color=tag.lower()
        )

    # Set axis labels
    ax.set_xlabel(x_label)
    ax.set_ylabel("Cone spectral sensitivities")

    # Legend
    legend = ax.legend(loc="upper right")
    legend.get_frame().set_alpha(0.5)

    if write_not_show:
        plt.savefig(write_path)
    else:
        plt.show()


if __name__ == "__main__":
    plot_rgb_csv()
