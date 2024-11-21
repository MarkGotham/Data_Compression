# coding: utf-8
# Implementations for Data Compression exercises.
# Source: https://github.com/MarkGotham/Data_Compression/tree/main


import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Reference speeds, m/s
speed_of_sound = 343
speed_of_light = 299792458

THIS_DIR = Path(__file__).parent


def plot_wavelength(
    min_fq: int = 20,
    max_fq: int = 20000,
    vel: int = speed_of_sound,
    reference_lines: bool = False,
    write_not_show: bool = True,
    write_path: Path = THIS_DIR / "plots" / "wavelength.pdf",
) -> None:
    """
    Plot the wavelength of sound waves for a given frequency range from `min_fq` to `max_fq`.

    :param min_fq: The minimum frequency of the sound wave (in Hz, default = 20)
    :param max_fq: The maximum frequency of the sound wave (in Hz, default = 20000)
    :param vel: A velocity. Defaults to the `speed_of_sound` (343m/s)
    :param reference_lines: include gridlines for 20 and 20,000Hz, and the equivalent wavelengths.
    :param write_not_show: If True (default), write, using the `write_path`. If False, then show.
    :param write_path: Path and file name to write to.
    """
    # Frequency range from 20 to 20,000 Hz
    freq = np.geomspace(min_fq, max_fq, 100)

    # Vel in np
    vel_array = vel * np.ones_like(freq)

    # Calculate
    wavelen = vel_array / freq

    # Plot the data
    fig, ax = plt.subplots()

    # Logarithmic scale for x and y axes
    ax.set_xscale('log')
    ax.set_yscale('log')

    ax.plot(freq, wavelen, '--r', label=f"$\lambda = v / f$ for $v$ = {vel}")
    # ax.semilogy(freq, wavelen, '--r', label=f"Frequency-Wavelength for v = {vel}")

    ax.set_xlabel("Frequency ($f$) in Hz")
    ax.set_ylabel("Wavelength ($\lambda$) in metres")
    ax.set_ylim([min(wavelen)/10, max(wavelen)*10])

    ax.legend(loc='upper right')

    if reference_lines:
        ax.axhline(17.15, linestyle='--', color='k')
        ax.axhline(0.01715, linestyle='--', color='k')
        ax.axvline(20, linestyle='--', color='k')
        ax.axvline(20000, linestyle='--', color='k')
    else:
        ax.grid()

    plt.tight_layout()

    if write_not_show:
        plt.savefig(write_path)
    else:
        plt.show()


if __name__ == "__main__":
    plot_wavelength(reference_lines=False)
