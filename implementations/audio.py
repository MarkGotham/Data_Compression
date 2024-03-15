# coding: utf-8

import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path
THIS_DIR = Path(__file__).parent
PATH_TO_BARK = THIS_DIR / "data" / "bark.csv"


# ------------------------------------------------------------------------

# Bark data

bark_data = pd.read_csv(
        PATH_TO_BARK,
        header=0,
        # names=y_labels
    )


def plot_bark(
    df: pd.DataFrame = bark_data,
    x_label: str = "Bark",
    y_label: str = "Frequency, Hz",
    write_not_show: bool = False,
    write_path: Path = THIS_DIR / "plots" / "bark_data.pdf",
) -> None:
    """
    Plot "Bark" data:
    an approximation of critical bandwidth after Zwicker 1961
    from a CSV file hosted locally in the form
    "Bark", "Lower", "Mid", "Upper", "Bandwidth".
    :return: None (plot)
    """

    fig, ax = plt.subplots()

    ax.errorbar(
        df["Bark"],
        df["Mid"],
        yerr=[
            df["Mid"] - df["Lower"],
            df["Upper"] - df["Mid"]
        ],
        fmt='o'
        ,
        label="Data"
    )

    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

    if write_not_show:
        plt.savefig(write_path)
    else:
        plt.show()


# ------------------------------------------------------------------------

# Bark models

def schroeder(f):
    """See note and credit at plot_bark_models"""
    return 7 * math.asinh(f/650)


def terhardt(f):
    """See note and credit at plot_bark_models"""
    return 13.3 * math.atan(0.75 * f/1000)


def zwicker(f):
    """See note and credit at plot_bark_models"""
    return 13 * math.atan(0.76 * f/1000) + 3.5 * math.atan(f/7500)


def traunmuller(f):
    """See note and credit at plot_bark_models"""
    return 26.81/(1+1960./f) - 0.53


def plot_bark_models(
        min_fq: int = 20,
        max_fq: int = 20000,
        write_not_show: bool = False,
        write_path: Path = THIS_DIR / "plots" / "bark_models.pdf",
) -> None:
    """
    Plot 4x models of the
    frequency-Bark relationship
    after (and with thanks to) Alexander Lerch:
    https://github.com/alexanderlerch/pyACA/blob/master/pyACA/ToolFreq2Bark.py
    """
    fig, ax = plt.subplots()
    freqs = np.linspace(min_fq, max_fq, 100)

    bark_dict = {
        "Schroeder": [schroeder(f) for f in freqs],
        "Terhardt": [terhardt(f) for f in freqs],
        "Traunmuller": [traunmuller(f) for f in freqs],
        "Zwicker": [zwicker(f) for f in freqs],
    }

    for k in bark_dict.keys():
        ax.plot(
            bark_dict[k],
            freqs,
            label=k)

    ax.legend(loc='upper left')
    plt.tight_layout()

    if write_not_show:
        plt.savefig(write_path)
    else:
        plt.show()


# ------------------------------------------------------------------------

def hearing_threshold(
        f,
        components_to_use=None
) -> float:
    """
    Return the model of absolute hearing threshold according to
    Fletcher H., “Auditory Patterns”, Rev. Mod. Phys., January 1940, pp. 47-65.
    This is made in three parts to encourage exploration of the components.
    """
    if components_to_use is None:
        components_to_use = [0, 1, 2]
    components = [0, 0, 0]
    if 0 in components_to_use:
        components[0] = 3.64 * ((f / 1000) ** -0.8)
    if 1 in components_to_use:
        components[1] = -6.5 * (np.e ** (-0.6 * (f / 1000 - 3.3) ** 2))
    if 2 in components_to_use:
        components[2] = (10 ** -3) * ((f / 1000) ** 4)
    return sum(components)


def approx_mask(
    freq: np.array,
    mu: int = 1000,
    sigma: int = 200,
    a: int = 50
) -> float:
    """
    Create an approximate masking effect with a
    Gaussian distribution around the a, mu, and sigma values given.
    """
    return a * np.exp(-(freq - mu)**2 / (2 * sigma**2))


def plot_hearing_threshold(
        freqs: np.array = np.linspace(20, 20000, 100),
        reference_lines: bool = True,
        mask: bool = True,
        write_not_show: bool = False,
        write_path: Path = THIS_DIR / "plots" / "hearing_threshold.pdf",
):
    """
    Plot the hearing threshold defined in `fletcher`.
    Optionally (bool) add a masking value (see `approx_mask`)modelled very approximately by a
    Gaussian with mu given by `mask_mu` and sigma by `mask_db`.

    :param reference_lines: Optionally (bool) add grid list at f = 20 and 20,000
    :param mask: Optionally (bool) add a mask as defined above.
    :param:Gaussian with mu given by `mask_mu` and sigma by `mask_db`.
    """
    fig, ax = plt.subplots()
    fletch = [hearing_threshold(f, components_to_use=[0, 1, 2]) for f in freqs]
    ax.plot(
        freqs,
        fletch,
        label="Original threshold"
    )
    ax.set_xscale('log')
    ax.set_xlabel("Frequency ($f$) in Hz")
    ax.set_ylabel("Decibel ($dB$)")
    if reference_lines:
        ax.axvline(20, linestyle='--', color='k')
        ax.axvline(20000, linestyle='--', color='k')
    else:
        ax.grid()

    if mask:
        mask_vals = approx_mask(freqs)
        ax.plot(
            freqs,
            mask_vals,
            label="Mask"
        )

        ax.plot(
            freqs,
            mask_vals + fletch,
            label="Combined"
        )

        ax.legend(loc='upper right')

    plt.tight_layout()

    if write_not_show:
        plt.savefig(write_path)
    else:
        plt.show()


def audible(f, db):
    """
    Simple bool estimate for whether a frequency-decibel pair will be audible.

    >>> audible(500, 50)
    True

    >>> audible(500, 5)
    False

    """
    ht_db = hearing_threshold(f)
    return db > ht_db


# ------------------------------------------------------------------------

def compand(s: int) -> int:
    """
    Map 16-bit nonlinearly to 15-bit numbers.
    Take a number in the range 0-65536 (i.e., 2 ** 16)
    and map it to one in the range 0-32767 (2 ** 15 − 1).
    Small numbers are less affected than large ones.

    >>> s = 65536  # NB would map to 16 bits 1111 1111 1111 1111
    >>> compand(s)
    32767

    >>> s = 50
    >>> compand(s)
    17

    """
    return round(32767 * ((2 ** (s / 65536)) - 1))


sampling_rates = [  # Hz.
    22050,  # e.g. MPEG
    44100,  # e.g. CD
    48000,  # e.g. DVD
]


bit_rates = [  # kbit/s
    8, 16, 24, 32,
]


def bits_per_frame(
        bit_rate: int = bit_rates[0],
        samples_per_frame: int = 1000,  # TODO
        sampling_rate: int = sampling_rates[0],
) -> float:
    return bit_rate * samples_per_frame / sampling_rate


def spectral_flatness(a: np.array):
    """
    [NB: bonus function, not in the textbook lecture notes]

    Measure a signal's `flatness'.
    Random data (e.g., white noise) is maximally flat (has minimum redundancy).
    The less noisy the signal, the less flat, the more redundancy, the more to compress.

    >>> signal = np.array(range(100))
    >>> psd(signal).round(5)
    0.03003

    >>> noise = np.random(100)
    >>> psd(a).round(5)
    0.03003

    """
    # Power Spectral Density (PSD)
    sxx = np.abs(np.fft.fft(a))**2

    # geometric mean:
    sxx_geom = np.exp(np.mean(np.log(sxx)))

    # arithmetic mean:
    sxx_arith = np.mean(sxx)

    # Compute the spectral flatness measure (SFM)
    return sxx_geom / sxx_arith


# ------------------------------------------------------------------------

if __name__ == "__main__":
    import doctest
    doctest.testmod()
