# coding: utf-8
# Implementations for Data Compression exercises.
# Source: https://github.com/MarkGotham/Data_Compression/tree/main


import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from typing import Union

THIS_DIR = Path(__file__).parent

speed_of_sound = 343

# Create an array in time
start, stop, sample = 20, 20000, 1000
fqs = np.linspace(start, stop, sample)


def wavelength_frequency(
    v: int = speed_of_sound,
    x: Union[float, int, np.linspace] = fqs
):
    """
    Maps between wavelength and frequency for a given velocity
    in either direction (wavelength to frequency or vice versa)
    and for either a single value or an array.

    For example, map the 20 and 20,000 Hz limits of human hearing
    to frequency length (in m).

    >>> wavelength_frequency(343, 20)
    17.15

    >>> wavelength_frequency(343, 20000)
    0.01715

    :param v: initalised for the speed of sound in m/s.
    :param x: an array of wavelengths or frequencies
    :return np.array:
    """
    return v / x


def tonotopic(
    x: Union[int, float],
    a: Union[int, float] = 2,
    b: Union[int, float] = 4,
    c: Union[int, float] = 10
) -> float:
    """
    Maps x in the range 0-30 to a value in the range 2000-20 with a smooth, logarithmic gradient.

    >>> tonotopic(30)
    20.0

    >>> tonotopic(20)
    200.0

    >>> tonotopic(10)
    2000.0

    >>> tonotopic(0)
    20000.0

    """
    return a * 10**(b - (x/c))


def plot_tonotopic(
    basilar_length: Union[int, float] = 30,
    increment: int = 1,
    reference_lines: bool = True,
    write_not_show: bool = True,
    write_path: Path = THIS_DIR / "plots" / "tonotopic.pdf",
) -> None:
    """
    Plots the
    length along the basilar membrane against the approximate
    frequency associated with that position, for a fixed length of the basilar membrane.

    :param basilar_length: Fixed length of the basilar membrane (in mm, default 30)
    :param increment: For making the array. Default 1.
    :param reference_lines: include gridlines for 20 and 20,000 Hz.
    :param write_not_show: If True (default), write, using the `write_path`. If False, then show.
    :param write_path: Path and file name to write to.
    """

    xs = range(0, basilar_length + 1, increment)
    ys = [tonotopic(x) for x in xs]
    plt.plot(xs, ys)

    plt.xscale('linear')
    plt.yscale('log')

    plt.xlabel('Position along basilar membrane (mm)')
    plt.ylabel('Frequency (Hz)')

    # plt.title('Tonotopic Function')

    if reference_lines:
        plt.axvline(0, linestyle='--', color='k')
        plt.axvline(30, linestyle='--', color='k')
        plt.axhline(20, linestyle='--', color='r')
        plt.axhline(20000, linestyle='--', color='r')
    else:
        plt.grid()

    if write_not_show:
        plt.savefig(write_path)
    else:
        plt.show()


if __name__ == "__main__":
    import doctest
    doctest.testmod()
