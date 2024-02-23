# coding: utf-8


import numpy as np


# -------------------------------------------------------------------------------------------------

h_2 = np.array([[1, 1], [1, -1]]) / np.sqrt(2)


def make_i_matrix(n: int = 2):
    """
    Make an i matrix of size n x n.

    >>> make_i_matrix(2)
    array([[1., 0.],
           [0., 1.]])

    >>> make_i_matrix(4)
    array([[1., 0., 0., 0.],
           [0., 1., 0., 0.],
           [0., 0., 1., 0.],
           [0., 0., 0., 1.]])
    """
    a = np.zeros((n, n))
    for x in range(len(a)):
        a[x][x] = 1
    return a


def make_h4() -> np.array:
    """
    Make h_4 from h_2.

    >>> hn_4 = make_h4()
    >>> hn_4
    array([[ 0.5       ,  0.5       ,  0.5       ,  0.5       ],
           [ 0.5       ,  0.5       , -0.5       , -0.5       ],
           [ 0.70710678, -0.70710678,  0.        , -0.        ],
           [ 0.        , -0.        ,  0.70710678, -0.70710678]])

    Check on one position that should be sqrt(1/2).

    >>> np.isclose(hn_4[2][0] ** 2, 0.5)
    True

    """

    h_part = np.kron(h_2, (1, 1))

    i_2 = make_i_matrix(2)
    i_part = np.kron(i_2, (1, -1))

    return np.concatenate((h_part, i_part), axis=0) / np.sqrt(2)


def make_double_h(h_n: np.array) -> np.array:
    """
    Make h_2n from h_n.

    >>> hn_4 = make_double_h(h_2)
    >>> hn_4
    array([[ 0.5       ,  0.5       ,  0.5       ,  0.5       ],
           [ 0.5       ,  0.5       , -0.5       , -0.5       ],
           [ 0.70710678, -0.70710678,  0.        , -0.        ],
           [ 0.        , -0.        ,  0.70710678, -0.70710678]])

    Check result matches above

    >>> np.allclose(hn_4, make_h4())
    True

    """

    h_part = np.kron(h_n, (1, 1))

    m, n = h_n.shape
    if m != n:
        raise ValueError("Only call on a square shape")

    i_n = make_i_matrix(n)
    i_part = np.kron(i_n, (1, -1))

    return np.concatenate((h_part, i_part), axis=0) / np.sqrt(n)


# -------------------------------------------------------------------------------------------------

# RCT, ICT

def prep(
        rgb: tuple,
        dc_shift: int = 255
) -> tuple:
    """
    Return the three colour components
    of a pixel (after DC shifting from, e.g., rgb)

    :param rgb:
    :param dc_shift: the amount of shift for a space 0–2^k-1. Defaults to 255 for the 256 space.
    """
    i_0, i_1, i_2 = [(x - dc_shift) for x in rgb]
    return i_0, i_1, i_2


def rct(rgb: tuple) -> tuple:
    """
    Implements the RCT (reversible component transform).

    Note, uses int() to truncate
    as opposed to floor() which rounds down.

    :param rgb: an RGB tuple.
    :return:
    """
    i_0, i_1, i_2 = prep(rgb)

    y_0 = int((i_0 + 2 * i_1 + i_2) / 4)
    y_1 = i_2 - i_1
    y_2 = i_0 - i_1
    return y_0, y_1, y_2


def ict(rgb: tuple) -> tuple:
    """
    Implements the ICT (irreversible component transform)
    :param rgb: an RGB tuple.
    :return:
    """
    i_0, i_1, i_2 = prep(rgb)
    y_0 = (0.299 * i_0) + (0.587 * i_1) + (0.144 * i_2)
    y_1 = (-0.16875 * i_0) - (0.33126 * i_1) + (0.5 * i_2)
    y_2 = (0.5 * i_0) - (0.41869 * i_1) - (0.08131 * i_2)
    return y_0, y_1, y_2


# -------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    import doctest
    doctest.testmod()
