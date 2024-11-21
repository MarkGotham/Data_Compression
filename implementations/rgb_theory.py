# coding: utf-8
# Implementations for Data Compression exercises.
# Source: https://github.com/MarkGotham/Data_Compression/tree/main


import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

THIS_DIR = Path(__file__).parent

# Means and SD in nanometres
λ_S = 420
λ_M = 530
λ_L = 560
σ = 20


def gaussian_cone_sensitivity(wavelength, peak_wavelength, sigma):
    """
    Gaussian model of cone cell sensitivity.
    """
    return np.exp(-((wavelength - peak_wavelength) ** 2) / (2 * sigma ** 2))


def s_resp(wavelength):
    """S-cones (blue)"""
    return gaussian_cone_sensitivity(wavelength, λ_S, σ)


def m_resp(wavelength):
    """M-cones (green)"""
    return gaussian_cone_sensitivity(wavelength, λ_M, σ)


def l_resp(wavelength):
    """L-cones (red)"""
    return gaussian_cone_sensitivity(wavelength, λ_L, σ)


def cone_resp(wavelength):
    return s_resp(wavelength), m_resp(wavelength), l_resp(wavelength)


def plot_resp(
    start: int = 400,
    stop: int = 700,
    num: int = 100,
    reference_lines: bool = False,
    write_not_show: bool = True,
    write_path: Path = THIS_DIR / "plots" / "rgb_theory.pdf",
):
    """
    Approximate Gaussian modelling for RGB values, using
    `s_resp`, `m_resp`, and `l_resp`.

    :param start: Wavelength value to start at, in nm.
    :param stop: Wavelength value to stop at, in nm.
    :param num: Increment / step for making the np.linspace.
    :param reference_lines: include gridlines for each mu value (x3).
    :param write_not_show: If True (default), write, using the `write_path`. If False, then show.
    :param write_path: Path and file name to write to.
    """

    wavelengths = np.linspace(start, stop, num)
    R_S, R_M, R_L = cone_resp(wavelengths)
    plt.plot(wavelengths, R_S, label='S-cone', color='b')
    plt.plot(wavelengths, R_M, label='M-cone', color='g')
    plt.plot(wavelengths, R_L, label='L-cone', color='r')
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Normalized resp')

    if reference_lines:
        plt.axvline(λ_S, linestyle='--', color='k')
        plt.axvline(λ_M, linestyle='--', color='k')
        plt.axvline(λ_L, linestyle='--', color='k')
    else:
        plt.grid()

    plt.legend()

    if write_not_show:
        plt.savefig(write_path)
    else:
        plt.show()


if __name__ == "__main__":
    plot_resp(reference_lines=True)
