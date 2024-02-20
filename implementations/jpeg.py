# coding: utf-8


import numpy as np
import scipy.fft as fft


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
                (np.pi * k * ((2 * n) + 1)) / (2 * N)
            ) for n in range(N)
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
    if double_transpose:  # An alternative
        return fft.dct(
            fft.dct(
                a.transpose(),
                norm="ortho"
            ).transpose(),
            norm="ortho"
        )  # default is over the last axis (i.e., axis=-1, i.e., not 0)
    else:
        return fft.dct(
            fft.dct(
                a,
                axis=0,
                norm="ortho"
            ),
            norm="ortho"
        )  # default is over the last axis (i.e., axis=-1, i.e., not 0)


def test_roundtrip(
        a: np.array
) -> np.array:
    """
    Implements a roundtrip test on a 2-d array and returns the value and position of the largest divergence.
    I.e.,
    - Take an array (a),
    - run DCT,
    - quant (to nearest integer in this case),
    - run IDCT,
    - compare change on each item (abs diff in this case).

    Using the `continuous_tone_pattern` matrix from Salomon's example.

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

    >>> fft.idctn(cont_dct, norm="ortho").round(2)
    array([[ 0.12, 10.02, 20.1 , 30.  , 30.  , 20.1 , 10.02,  0.12],
           [10.02, 19.92, 30.  , 39.9 , 39.9 , 30.  , 19.92, 10.02],
           [20.1 , 30.  , 40.08, 49.98, 49.98, 40.08, 30.  , 20.1 ],
           [30.  , 39.9 , 49.98, 59.88, 59.88, 49.98, 39.9 , 30.  ],
           [30.  , 39.9 , 49.98, 59.88, 59.88, 49.98, 39.9 , 30.  ],
           [20.1 , 30.  , 40.08, 49.98, 49.98, 40.08, 30.  , 20.1 ],
           [10.02, 19.92, 30.  , 39.9 , 39.9 , 30.  , 19.92, 10.02],
           [ 0.12, 10.02, 20.1 , 30.  , 30.  , 20.1 , 10.02,  0.12]])

    >>> test_roundtrip(continuous_tone_pattern)
    (0.12, (0, 0))

    So the largest diff is the 0 vs 0.012 in position 0, 0 (top left).

    """
    dct_round = fft.dctn(a, norm="ortho").round(0)
    idct_v = fft.idctn(dct_round, norm="ortho")
    m, n = a.shape
    assert m > 1
    assert n > 1
    max_diff = 0
    diff_ref = None
    for i in range(m):
        for j in range(n):
            this_diff = abs(a[i][j] - idct_v[i][j])
            if this_diff > max_diff:
                max_diff = this_diff
                diff_ref = (i, j)

    return round(max_diff, 2), diff_ref


# ------------------------------------------------------------------------

if __name__ == "__main__":
    import doctest
    doctest.testmod()
