# coding: utf-8
# Implementations for Data Compression exercises.
# Source: https://github.com/MarkGotham/Data_Compression/tree/main


import numpy as np
import scipy.fft as fft

try:
    import matrix_basics
except:
    from . import matrix_basics

# Code: New implementations
# Example values from Salomon and Motta Handbook of Data Compression, 5th Edition.


signal_1d = (12, 10, 8, 10, 12, 10, 8, 11)

continuous_tone_pattern = np.array(
    [
        [0, 10, 20, 30, 30, 20, 10, 0],
        [10, 20, 30, 40, 40, 30, 20, 10],
        [20, 30, 40, 50, 50, 40, 30, 20],
        [30, 40, 50, 60, 60, 50, 40, 30],
        [30, 40, 50, 60, 60, 50, 40, 30],
        [20, 30, 40, 50, 50, 40, 30, 20],
        [10, 20, 30, 40, 40, 30, 20, 10],
        [0, 10, 20, 30, 30, 20, 10, 0]
    ]
)


dct_matrix = np.array(
    [
        [0.354, 0.354, 0.354, 0.354, 0.354, 0.354, 0.354, 0.354],
        [0.49, 0.416, 0.278, 0.098, -0.098, -0.278, -0.416, -0.49],
        [0.462, 0.191, -0.191, -0.462, -0.462, -0.191, 0.191, 0.462],
        [0.416, -0.098, -0.49, -0.278, 0.278, 0.49, 0.098, -0.416],
        [0.354, -0.354, -0.354, 0.354, 0.354, -0.354, -0.354, 0.354],
        [0.278, -0.49, 0.098, 0.416, -0.416, -0.098, 0.49, -0.278],
        [0.191, -0.462, 0.462, -0.191, -0.191, 0.462, -0.462, 0.191],
        [0.098, -0.278, 0.416, -0.49, 0.49, -0.416, 0.278, -0.098]
    ]
)


def create_DCT_matrix(
        n: int = 8
) -> np.array:
    """
    Create a DCT transform matrix (cosine functions of various periodicities).
    Create from scratch, and compare with scipy.
    (Compare and contrast also with the DCT directly on a signal at `dct`, below).
    Test properties.

    The DCT matrix is bascially the result of a DCT on an i-matrix of the given size.
    First with scipy:

    >>> i = np.eye(8)
    >>> c_scipy = fft.dct(i, type=2, norm='ortho').round(3).transpose()
    >>> np.allclose(c_scipy, dct_matrix)
    True

    Now from scratch (here):

    >>> C = create_DCT_matrix()
    >>> np.allclose(C.round(3), dct_matrix)
    True

    As such, the inverse relation C_T = C_-1
    >>> product = (np.transpose(C) @ C).round(4)
    >>> product
    array([[ 1., -0.,  0.,  0., -0.,  0.,  0., -0.],
           [-0.,  1.,  0.,  0.,  0., -0., -0.,  0.],
           [ 0.,  0.,  1., -0., -0., -0., -0.,  0.],
           [ 0.,  0., -0.,  1.,  0.,  0.,  0.,  0.],
           [-0.,  0., -0.,  0.,  1., -0., -0., -0.],
           [ 0., -0., -0.,  0., -0.,  1.,  0.,  0.],
           [ 0., -0., -0.,  0., -0.,  0.,  1.,  0.],
           [-0.,  0.,  0.,  0., -0.,  0.,  0.,  1.]])

    """
    c = np.zeros((n, n))

    i = 0
    for j in range(n):
        c[i][j] = np.sqrt(1 / n)

    for i in range(1, n):  # k
        for j in range(n):  # n
            c[i][j] = np.cos(
                (np.pi * i * ((2 * j) + 1)) / (2 * n)  # This line (i, j, n)
            ) * np.sqrt(2 / n)

    return c


def dct(
        a: np.array,
        scaling: bool = True
) -> np.array:
    """
    Implements the DCT.
    This demonstration uses example values from Salomon and Motta Handbook of Data Compression, 5th Edition
    as above

    First, using scipy (not this local implementation):

    >>> dct_v = fft.dct(signal_1d, norm="ortho")  # From Handbook.
    >>> dct_v
    array([28.63782464,  0.5712017 ,  0.46193977,  1.757     ,  3.18198052,
           -1.7295601 ,  0.19134172, -0.3087094 ])

    >>> quantized_1dp = dct_v.round(1)  # Equivalent to `round(x, 1) for x in` ...
    >>> quantized_1dp  # Note DS has different value: -1.7 -> -1.8. Note comment on limited precision (rounding).
    array([28.6,  0.6,  0.5,  1.8,  3.2, -1.7,  0.2, -0.3])

    >>> quasi_dct_values = [28.6,  0.6,  0.5,  1.8,  3.2, -1.8,  0.2, -0.3]
    >>> idct_1 = fft.idct(quasi_dct_values, norm="ortho")  # (DS values)
    >>> idct_1  # 12.0254, 10.0233, 7.96054, 9.93097, 12.0164, 9.99321, 7.94354, 10.9989  # (DS values)
    array([12.02551752, 10.02344091,  7.9606358 ,  9.93106862, 12.01645057,
            9.99331063,  7.94363714, 10.99895457])

    >>> quantized_ints = np.array([round(x, 0) for x in dct_v])
    >>> quantized_ints
    array([29.,  1.,  0.,  2.,  3., -2.,  0., -0.])

    >>> idct_2 = fft.idct(quantized_ints, norm="ortho")  # From Handbook.
    >>> idct_2
    array([12.08000052, 10.39381792,  8.29429767, 10.02421381, 12.60320318,
           10.09047864,  7.99095839, 10.54741648])

    Second set, with the same values but using this (local, from scratch) implementation.

    >>> dct_ours = dct(signal_1d, scaling=True)
    >>> dct_ours
    array([28.63782464,  0.5712017 ,  0.46193977,  1.757     ,  3.18198052,
           -1.7295601 ,  0.19134172, -0.3087094 ])

    >>> np.isclose(dct_ours.all(), dct_v.all())
    True

    :param a: A np.array.
    :param scaling: Optional (bool, default = True) use of a scaling factor.

    """
    N = len(a)
    y = [None] * N  # init

    for k in range(N):
        y[k] = 2 * sum(
            [a[n] * np.cos(
                (np.pi * k * ((2 * n) + 1)) / (2 * N)  # This line (k, n, N)
            ) for n in range(N)  # 0 to N-1
             ]
        )

    if scaling:
        y = [(x / np.sqrt(2 * N)) for x in y]  # For most.
        y[0] /= np.sqrt(2)  # Different scale for the DC (0th term)

    return np.array(y)


def dct_2d(
        a: np.array,
        double_transpose: bool = False
) -> np.array:
    """
    Perform a multi- (specifically 2-) dimensional DCT-II of an n x n matrix,
    e.g., for an image.
    This is equivalent to `fft.dctn(a)` (as demonstrated in the following),
    simply showing the rows-then-axes method in 2 different ways.

    Contnuing with the `continuous_tone_pattern` matrix from Salomon's example.

    First, with `dctn` off the shelf (note, recent scipy version needed):

    >>> cont_dct = fft.dctn(continuous_tone_pattern, norm="ortho").round(0)
    >>> cont_dct
    array([[240.,   0., -89.,   0.,   0.,   0.,  -6.,   0.],
           [  0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.],
           [-89.,   0.,   0.,   0.,   0.,   0.,   0.,   0.],
           [  0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.],
           [  0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.],
           [  0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.],
           [ -6.,   0.,   0.,   0.,   0.,   0.,   0.,   0.],
           [  0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.]])

    Now with local versions x 2:

    >>> no_double_transpose = dct_2d(continuous_tone_pattern, double_transpose=False).round(0)
    >>> no_double_transpose
    array([[240.,   0., -89.,   0.,   0.,   0.,  -6.,   0.],
           [  0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.],
           [-89.,   0.,   0.,   0.,   0.,   0.,   0.,   0.],
           [  0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.],
           [  0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.],
           [  0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.],
           [ -6.,   0.,   0.,   0.,   0.,   0.,   0.,   0.],
           [  0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.]])

    >>> with_double_transpose = dct_2d(continuous_tone_pattern, double_transpose=True).round(0)
    >>> with_double_transpose
    array([[240.,   0., -89.,   0.,   0.,   0.,  -6.,   0.],
           [  0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.],
           [-89.,   0.,   0.,   0.,   0.,   0.,   0.,   0.],
           [  0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.],
           [  0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.],
           [  0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.],
           [ -6.,   0.,   0.,   0.,   0.,   0.,   0.,   0.],
           [  0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.]])

    >>> assert np.allclose(no_double_transpose, with_double_transpose)
    >>> assert np.allclose(cont_dct, with_double_transpose)
    >>> assert np.allclose(cont_dct, no_double_transpose)

    :param a: Input array
    :param double_transpose: An equivalent method that doubly transposes `a` to get at the two axes.
    :return: array, DCT'd in 2 d.
    """
    if double_transpose:  # By transposing the array back and forth. An alternative (not default).
        return fft.dct(
            fft.dct(
                a.transpose(),
                norm="ortho"
            ).transpose(),
            norm="ortho"
        )
    else:  # By specifying the axis. Default is the last axis (i.e., axis=-1), so setting axis=0 gets the other one.
        return fft.dct(
            fft.dct(
                a,
                axis=0,
                norm="ortho"
            ),
            norm="ortho"
        )


def test_roundtrip(
        a: np.array,
        quant: bool = True
) -> np.array:
    """
    Implements a roundtrip test on a 2-d array and returns the value and position of the largest divergence.
    I.e.,
    - Take an array (a),
    - DCT-N,
    - optionally quantize and then reverse quantize (with `quantize(reconstruct=True)`),
    - IDCT-N,
    - compare change on each item to return the size and position of the greatest (abs) diff.

    This function returns the value of `max_diff_val_and_location`
    except where that largest difference is 0, in which case the function returns `None`.

    Using the `continuous_tone_pattern` matrix from Salomon's example,
    >>> test_roundtrip(continuous_tone_pattern, quant=True)
    (5.83, (0, 0))

    the version with no `quantize` step return an array with no difference:
    >>> test_roundtrip(continuous_tone_pattern, quant=False) is None
    True

    """
    dct_round = fft.dctn(a, norm="ortho")
    if quant:
        dct_quant = matrix_basics.quantize(dct_round)
        dct_unquant = matrix_basics.quantize(dct_quant, reconstruct=True)
        idct_v = fft.idctn(dct_unquant, norm="ortho")
    else:
        idct_v = fft.idctn(dct_round, norm="ortho")
    d = matrix_basics.max_diff_val_and_location(a, idct_v)
    if d[0] == 0:
        return None
    else:
        return d


# ------------------------------------------------------------------------

if __name__ == "__main__":
    import doctest
    doctest.testmod()
