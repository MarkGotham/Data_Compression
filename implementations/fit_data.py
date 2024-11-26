# coding: utf-8
# Implementations for Data Compression exercises.
# Source: https://github.com/MarkGotham/Data_Compression/tree/main


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path
from scipy.optimize import curve_fit
from typing import Union

THIS_DIR = Path(__file__).parent


def gaussian(x, amp, mean, sigma):
    return amp * np.exp(-((x - mean) / sigma) ** 2)


def fit_gaussian_to_data(x_data, y_data):
    popt, pcov = curve_fit(
        gaussian,
        x_data,
        y_data,
        p0=[max(y_data), np.mean(x_data), np.std(x_data)]
    )
    return popt


def plot_fit(
        file_path: Union[str, Path] = THIS_DIR / "data" / "rgb.csv",
        x_label: Union[str, None] = "Wavelength $\lambda$",
        y_label: Union[str, None] = "Sensitivity",
        plot: bool = True,
        write_path: Union[Path, str] = THIS_DIR / "plots" / "r_data_with_fit.pdf"
) -> None:
    """
    Demonstrate curve fitting for the case of R cone cells:
    Take R from the RGB data and attempt to fit it with a Gaussian curve
    using the mean and SD from the data as an initial guess.
    """

    df = pd.read_csv(
        file_path,
        header=None,
        names=["x", "R", "G", "B"]
    )

    x_data = df["x"]
    r_data = df["R"]

    popt = fit_gaussian_to_data(x_data, r_data)

    plt.plot(x_data, r_data, linestyle="dotted", label="data", color="r")
    plt.plot(x_data, gaussian(x_data, *popt), linestyle="solid", label="fit", color="r")
    plt.legend()
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.savefig(write_path)


# ------------------------------------------------------------------------

if __name__ == "__main__":
    plot_fit()
