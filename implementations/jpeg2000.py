# coding: utf-8


import numpy as np
from typing import Union


# -------------------------------------------------------------------------------------------------

# RCT, ICT

def dc_shift(
        rgb: Union[list, tuple],
        shift: int = 255
) -> list:
    """
    Return the three colour components
    of a pixel (after DC shifting from, e.g., rgb)

    :param rgb: the three colour component tuple (e.g., RGB).
    :param shift: the amount of shift for a space 0–2^k-1. Defaults to 255 for the 256 space.
    """
    return [(x - shift) for x in rgb]


def rct(rgb: Union[list, tuple]) -> tuple:
    """
    Implements the RCT (reversible component transform).

    Note, uses int() to truncate
    as opposed to floor() which rounds down.

    :param rgb: an RGB tuple.
    :return:
    """
    i_0, i_1, i_2 = dc_shift(rgb)

    y_0 = int((i_0 + 2 * i_1 + i_2) / 4)
    y_1 = i_2 - i_1
    y_2 = i_0 - i_1
    return y_0, y_1, y_2


def ict(rgb: Union[list, tuple]) -> tuple:
    """
    Implements the ICT (irreversible component transform)
    :param rgb: an RGB tuple.
    :return:
    """
    i_0, i_1, i_2 = dc_shift(rgb)
    y_0 = (0.299 * i_0) + (0.587 * i_1) + (0.144 * i_2)
    y_1 = (-0.16875 * i_0) - (0.33126 * i_1) + (0.5 * i_2)
    y_2 = (0.5 * i_0) - (0.41869 * i_1) - (0.08131 * i_2)
    return y_0, y_1, y_2


# ------------------------------------------------------------------------

# Wavelet filter coefficients used by JPEG 2000 for CDF 9/7.

constants_dict = {
    "alpha": -1.586134342,
    "beta": -0.052980118,
    "gamma": 0.882911075,
    "delta": 0.443506852,
    "K": 1.230174105
}


# ------------------------------------------------------------------------

def cdf_9_7(
        a: np.array,
        m_n: Union[tuple, None] = None,
        alpha: float = constants_dict["alpha"],
        beta: float = constants_dict["beta"],
        gamma: float = constants_dict["gamma"],
        delta: float = constants_dict["delta"],
        K: float = constants_dict["K"]
) -> np.array:
    """
    Cohen-Daubechies-Feauveau (CDF) 9/7 wavelet transform.

    :param a: a 2D, n-by-n numpy array. Transform performed on all columns.
    :param m_n: A tuple with the m and n dimensions. Optional (otherwise use .shape).
    :param alpha: a coefficient.
    :param beta: a coefficient.
    :param gamma: a coefficient.
    :param delta: a coefficient.
    :param K: a scaling coefficient.

    :returns: the input matrix, modified. Highpass results on the left, lowpass on the right.

    >>> a = np.array(range(64)).reshape(8, 8)
    >>> a
    array([[ 0,  1,  2,  3,  4,  5,  6,  7],
           [ 8,  9, 10, 11, 12, 13, 14, 15],
           [16, 17, 18, 19, 20, 21, 22, 23],
           [24, 25, 26, 27, 28, 29, 30, 31],
           [32, 33, 34, 35, 36, 37, 38, 39],
           [40, 41, 42, 43, 44, 45, 46, 47],
           [48, 49, 50, 51, 52, 53, 54, 55],
           [56, 57, 58, 59, 60, 61, 62, 63]])

    >>> cdf_9_7(a)
    array([[ 0, 15, 30, 47,  0,  0,  0,  2],
           [ 2, 16, 30, 47,  0,  0, -1,  2],
           [ 3, 17, 32, 49,  0,  0,  0,  3],
           [ 4, 18, 33, 50,  0,  0, -1,  3],
           [ 4, 19, 34, 51,  0,  0,  0,  3],
           [ 5, 20, 35, 52,  0,  0,  0,  2],
           [ 7, 21, 37, 54,  0,  0,  0,  3],
           [ 8, 22, 37, 54,  0,  0, -1,  3]])
    """

    if m_n:
        m, n = m_n
    else:
        m, n = a.shape

    for col in range(n):

        # Step 1
        for row in range(1, m - 1, 2):
            a[row][col] += alpha * (a[row - 1][col] + a[row + 1][col])
        a[m - 1][col] += 2 * alpha * a[m - 2][col]

        # Step 2
        for row in range(2, m, 2):
            a[row][col] += beta * (a[row - 1][col] + a[row + 1][col])
        a[0][col] += 2 * beta * a[1][col]

        # Step 3
        for row in range(1, m - 1, 2):
            a[row][col] += gamma * (a[row - 1][col] + a[row + 1][col])
        a[m - 1][col] += 2 * gamma * a[m - 2][col]

        # Step 4
        for row in range(2, m, 2):
            a[row][col] += delta * (a[row - 1][col] + a[row + 1][col])
        a[0][col] += 2 * delta * a[1][col]

    # Steps 5-6
    temp_bank = [[0] * n for i in range(m)]
    for row in range(m):
        for col in range(n):
            # Scaling:
            if row % 2 == 0:  # even rows
                temp_bank[col][int(row / 2)] = a[row][col] / K
            else:  # odd ones
                temp_bank[col][int((row / 2) + (m / 2))] = a[row][col] * K / 2

    for row in range(n):
        for col in range(m):
            a[row][col] = temp_bank[row][col]

    return a


def i_cdf_9_7(
        a: np.array,
        m_n: Union[tuple, None] = None,
        alpha: float = - constants_dict["alpha"],
        beta: float = - constants_dict["beta"],
        gamma: float = - constants_dict["gamma"],
        delta: float = - constants_dict["delta"],
        K: float = - constants_dict["K"]
) -> np.array:
    """
    Inverse CDF 9/7 function.
    See notes at `cdf_9_7()` and note the inverse coefficient values (e.g., `- alpha`).
    """

    if m_n:
        m, n = m_n
    else:
        m, n = a.shape

    w_2 = int(n / 2)

    temp_bank = [[0] * n for i in range(m)]
    for col in range(w_2):
        for row in range(m):
            temp_bank[col * 2][row] = a[row][col] * K  # cf line 100
            temp_bank[col * 2 + 1][row] = a[row][col + w_2] * 2 / K  # cf line 102

    for row in range(n):
        for col in range(m):
            a[row][col] = temp_bank[row][col]

    for col in range(n):

        for row in range(2, m, 2):
            a[row][col] += delta * (a[row - 1][col] + a[row + 1][col])
        a[0][col] += 2 * delta * a[1][col]

        for row in range(1, m - 1, 2):
            a[row][col] += gamma * (a[row - 1][col] + a[row + 1][col])
        a[m - 1][col] += 2 * gamma * a[m - 2][col]

        for row in range(2, m, 2):
            a[row][col] += beta * (a[row - 1][col] + a[row + 1][col])
        a[0][col] += 2 * beta * a[1][col]

        for row in range(1, m - 1, 2):
            a[row][col] += alpha * (a[row - 1][col] + a[row + 1][col])
        a[m - 1][col] += 2 * alpha * a[m - 2][col]

    return a


# ------------------------------------------------------------------------

if __name__ == "__main__":
    import doctest
    doctest.testmod()
