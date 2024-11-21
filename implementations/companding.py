# coding: utf-8
# Implementations for Data Compression exercises.
# Source: https://github.com/MarkGotham/Data_Compression/tree/main


import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
THIS_DIR = Path(__file__).parent


# ------------------------------------------------------------------------

def signum(x: float):
    """
    The sign or signum function
    (Currently implemented within mu_law).
    """
    if x > 0:
        return 1
    elif x < 0:
        return -1
    elif x == 0:
        return 0
    else:
        raise ValueError("Unexpected value that's not 0, positive, or negative.")


def mu_law_encode(
        x: int,
        mu: int = 255,
        in_upper: int = 8191,
        in_lower: int = -8192,
        out_upper: int = 255,
        out_lower: int = -256,
) -> int:
    """
    The mu-law is a subtler and more standardised form of companding.

    >>> mu_law_encode(5000)
    232

    :param x: A signed integer value for the sample, between `in_upper` and `in_lower`.
    :param mu: An integer, 255 by default.
    :param in_upper: Upper value of the input (e.g., 8191 for 14-bit data).
    :param in_lower: Lower value of the input.
    :param out_upper: Upper value of the output (e.g., 255 for 8-bit data).
    :param out_lower: Lower value of the output.
    """

    if x == 0:  # cf signum
        return 0
    elif x < 0:
        if x < in_lower:
            raise ValueError(f"x (currently {x} must be greater than {in_lower}")
        else:
            norm = x / in_lower  # norm to the interval [−1, +1]
    elif x > 0:
        if x > in_upper:
            raise ValueError(f"x (currently {x} must be less than {in_upper}")
        else:
            norm = x / in_upper  # norm to the interval [−1, +1]

    log_exp = np.log(1 + (mu * np.abs(norm))) / np.log(1 + mu)

    if x > 0:
        return int(log_exp * out_upper)
    else:  # x < 0
        return int(log_exp * out_lower)


def plot_mu(
        x_label: str = "Before",
        y_label: str = "After",
        write_path: Path = THIS_DIR / "plots" / "compand.pdf",
        write_not_show: bool = False
) -> None:
    """
    Plot mu-law compand curve.
    """
    fig, ax = plt.subplots()
    freqs = np.linspace(-8192, 8191)
    ax.plot(freqs, [mu_law_encode(f) for f in freqs])

    plt.tight_layout()
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

    if write_not_show:
        plt.savefig(write_path)
    else:
        plt.show()


# ------------------------------------------------------------------------

if __name__ == "__main__":
    import doctest
    doctest.testmod()
