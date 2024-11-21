# coding: utf-8
# Implementations for Data Compression exercises.
# Source: https://github.com/MarkGotham/Data_Compression/tree/main


import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path

THIS_DIR = Path(__file__).parent

from typing import Union


def simple_sin(
        a: Union[int, float],
        hz: Union[int, float],
        t: Union[int, float, np.array]
):
    """
    >>> s = simple_sin(1, 100, 0.0325)
    >>> np.isclose(s, 1)
    True

    :param a: amplitude
    :param hz: frequency
    :param t: time (point or array)
    """
    return a * np.sin(2 * np.pi * hz * t)


def fundamental_w_partials(
        fundamental: int = 100,
        multiples=None,
) -> np.array:
    """
    Support function for creating a composite signal with
    a fundamental frequency
    and several overtones with
    each frequency as an integer multiple of the fundamental and
    each max amplitude by inverse proportion.

    >>> fundamental_w_partials(100, [1, 2, 4])
    {100: 1.0, 200: 0.5, 400: 0.25}

    :param fundamental: the fundamental frequency in Hertz
    :param multiples: a list of integer multiples to create overtones.
    :return: dict with each overtone (the multiples given) and 1 / overtone as a max amplitude.
    """

    overtone_magnitude_dict = {fundamental: 1}

    if multiples is None:
        multiples = [1, 2, 3, 4, 5, 6, 7]

    for m in multiples:
        overtone_magnitude_dict[m * fundamental] = 1 / m

    return overtone_magnitude_dict


def composite_signal(
        t: Union[int, float, np.array],
        overtone_magnitude_dict: dict = fundamental_w_partials()
) -> float:
    """
    Create a composite signal from a time array,
    and a set of frequency-magnitude pairs for simple sine waves.

    :param t: time point or array
    :param overtone_magnitude_dict: frequency-magnitude pairs. See `fundamental_w_partials` for an example.
    """
    out_val = 0
    for hz in overtone_magnitude_dict:
        out_val += simple_sin(overtone_magnitude_dict[hz], hz, t)
    return out_val


def plot_signal(
        time_array: np.array,
        plot_proportion: float = 0.1,
        overtone_magnitude_dict: Union[dict, None] = None,
        plot_components: bool = True,
        write_not_show: bool = True,
        write_path: Union[Path, str] = THIS_DIR / "plots" / "composite.pdf"
) -> None:
    """
    Plot a `time_array` against both a composite signal and the components that make it up.

    :param time_array: a numpy array of time increments
    :param plot_proportion: how much of the sample to plot. Float, default 0.1 (i.e., 10%).
    :param overtone_magnitude_dict: see `fundamental_w_partials` above
    :param plot_components: if True, Create a second subplot with the signal and components shown separately.
    :param write_not_show: Chose between saving and showing.
    :param write_path: If writing/saving, chose a file location and name.
    :return: None (plot)
    """

    plt.figure(figsize=(10, 6))
    axis_label_size, legend_label_size = 14, 13
    plt.subplot(2, 1, 1)  # position above/below

    if 0 < plot_proportion <= 1:
        plot_range = int(len(time_array) * plot_proportion)
    else:
        raise ValueError("The `plot_proportion` must be greater than 0 and less than or equal to 1.")

    # Prep and plot composite
    if not overtone_magnitude_dict:
        overtone_magnitude_dict = fundamental_w_partials()
    y = composite_signal(time_array, overtone_magnitude_dict=overtone_magnitude_dict)
    plt.plot(time_array[:plot_range], y[:plot_range], label='signal')

    plt.ylabel('Amplitude', fontsize=axis_label_size)
    plt.axis('tight')
    plt.grid()
    plt.xlim(time_array[0], time_array[plot_range])
    plt.legend(loc='upper right', shadow=False, fontsize=legend_label_size)

    if plot_components:
        plt.subplot(2, 1, 2)  # position above/below
        plt.plot(time_array, y, label='signal')  # as before, signal
        count = 1
        for hz in overtone_magnitude_dict:  # now the reference/components
            y = simple_sin(overtone_magnitude_dict[hz], hz, time_array)
            plt.plot(time_array[:plot_range], y[:plot_range], "--", label=f'component {count}')
            count += 1
        plt.ylabel('Amplitude', fontsize=axis_label_size)
        plt.axis('tight')
        plt.grid()
        plt.xlim(time_array[0], time_array[plot_range])

    plt.xlabel('Time (seconds)', fontsize=axis_label_size)
    plt.legend(loc='upper right', shadow=False, fontsize=legend_label_size)
    plt.tight_layout()

    if write_not_show:
        plt.savefig(write_path)
    else:
        plt.show()


# Running values to experiment with
sr = 22050  # sample rate
# sr /= 2   # Try halving the sample rate here
T = 1.0     # total time in seconds
hz = 440
time_array = np.linspace(0, T, int(T * sr))  # from 0 to T with T*sr increments


def run():
    """
    Put all these functions together for a set of example values.
    """
    fp = fundamental_w_partials(fundamental=100, multiples=[1, 2, 3, 4, 5, 6, 7])
    plot_signal(time_array, 0.05, fp, True)


def quick_fft(
        composite: Union[np.array, None] = None,
        plot_proportion: float = 0.05,
        write_not_show: bool = True,
        write_path: Union[Path, str] = THIS_DIR / "plots" / "dft.pdf"
) -> None:
    """
    Calculate and plot the Fourier transform.

    :param composite: The signal. If none, then it creates a demo from hard coded values.
    :param plot_proportion: a float, greater than 0 and leq 1. E.g.,
    if 1 then return full results (at least after the abs),
    if 0.5 then return half removing the symmetry.
    If outside the range 0-1, then raise ValueError.
    :param write_not_show: Chose between saving and showing.
    :param write_path: If writing/saving, chose a file location and name.
    :return: None (plot)
    """
    if not composite:
        fp = fundamental_w_partials(fundamental=100, multiples=[1, 2, 3, 4, 5, 6, 7])
        composite = composite_signal(time_array, overtone_magnitude_dict=fp)

    X = np.fft.fft(composite)
    X_mag = np.absolute(X)
    f = np.linspace(0, sr, len(X_mag))

    plt.figure(figsize=(10, 6))

    if 0 < plot_proportion <= 1:
        plt.plot(f[:int(len(f) * plot_proportion)], X_mag[:int(len(X_mag) * plot_proportion)])
    else:
        raise ValueError("The `plot_proportion` must be Greater than nought and less than or equal to 1.")

    axis_label_size = 14
    plt.ylabel('FFT Amplitude $|X(freq)|$', fontsize=axis_label_size)
    plt.xlabel('Frequency, $Hz$', fontsize=axis_label_size)

    plt.grid()

    if write_not_show:
        plt.savefig(write_path)
    else:
        plt.show()


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    # run()
    # quick_fft()
