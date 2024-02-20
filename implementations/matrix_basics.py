# coding: utf-8


import numpy as np


def get_m_n(a: np.array) -> tuple:
    """
    Get the m and n dimensions of a 1- or 2-D array.

    >>> a = np.array([[1.,  1.,  1.,  1.,  1.], [1.,  1.,  1.,  1.,  1.], [1.,  1.,  1.,  1.,  1.]])
    >>> get_m_n(a)
    (3, 5)

    >>> one_by_n = np.array([1, 2, 3, 4, 5, 6])
    >>> get_m_n(one_by_n)
    (6, 1)
    """

    s = a.shape
    m = s[0]
    if len(s) == 1:
        n = 1
    elif len(s) == 2:
        n = s[1]
    else:
        raise ValueError("Shape length must be 1- or 2-d")

    return m, n


def pad_2x2(a: np.array) -> np.array:
    """
    Pad an array to double the length and width (4x total)
    with zeros to the right and below.

    Note the double [[]].

    >>> pad_2x2(np.array([[1, 0]]))
    array([[1, 0, 0, 0],
           [0, 0, 0, 0]])

    >>> pad_2x2(np.array([[1], [0]]))
    array([[1, 0],
           [0, 0],
           [0, 0],
           [0, 0]])

    >>> pad_2x2(np.array([[1, 0], [0, 1]]))
    array([[1, 0, 0, 0],
           [0, 1, 0, 0],
           [0, 0, 0, 0],
           [0, 0, 0, 0]])

    :param a: Input array
    :return: expanded array
    """
    x, y = get_m_n(a)
    return np.pad(
        a,
        [(0, x), (0, y)],  # add below and right
        mode='constant',
        constant_values=0
    )


def back_to_half(a: np.array) -> np.array:
    """
    Reduce an array to half the length and width (1/4 total),
    taking the top and left most block
    (complements `pad_2x2`)

    >>> a = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
    >>> back_to_half(a)
    array([[1, 0],
           [0, 1]])

    Test the complementarity of
    `pad_2x2` and `back_to_half`
    with a roundtrip assertion.

    >>> a = np.array([[1, 0], [0, 1]])
    >>> p = pad_2x2(a)
    >>> p
    array([[1, 0, 0, 0],
           [0, 1, 0, 0],
           [0, 0, 0, 0],
           [0, 0, 0, 0]])
    >>> halved = back_to_half(p)
    >>> halved
    array([[1, 0],
           [0, 1]])

    >>> assert halved.all() == a.all()


    :param a: Input (larger) array
    :return: smaller array
    """
    x, y = get_m_n(a)
    return a[0:int(x/2), 0:int(y/2)]


def array_subtraction(
    a: np.array = np.array([[1, 2], [3, 4]]),
    n: int = 2
) -> np.array:
    """
    >>> array_subtraction()
    array([[-1,  0],
           [ 1,  2]])
    """
    return a - n


theta = np.array(
    [
        [39.88, 6.56, -2.24, 1.22, -0.37, -1.08, 0.79, 1.13],
        [-102.43, 4.56, 2.26, 1.12, 0.35, -0.63, -1.05, -0.48],
        [37.77, 1.31, 1.77, 0.25, -1.50, -2.21, -0.10, 0.23],
        [-5.67, 2.24, -1.32, -0.81, 1.41, 0.22, -0.13, 0.17],
        [-3.37, -0.74, -1.75, 0.77, -0.62, -2.65, -1.30, 0.76],
        [5.98, -0.13, -0.45, -0.77, 1.99, -0.26, 1.46, 0.00],
        [3.97, 5.52, 2.39, -0.55, -0.051, -0.84, -0.52, -0.13],
        [-3.43, 0.51, -1.07, 0.87, 0.96, 0.09, 0.33, 0.01]
    ]
)


# Compare
# https://github.com/python-pillow/Pillow/blob/6956d0b2853f5c7ec5f6ec4c60725c5a7ee73aeb/src/PIL/JpegPresets.py#L88
quantization_table = np.array(
    [
        [16, 11, 10, 16, 24, 40, 51, 61],
        [12, 12, 14, 19, 26, 58, 60, 55],
        [14, 13, 16, 24, 40, 57, 69, 56],
        [14, 17, 22, 29, 51, 87, 80, 62],
        [18, 22, 37, 56, 68, 109, 103, 77],
        [24, 35, 55, 64, 81, 104, 113, 92],
        [49, 64, 78, 87, 103, 121, 120, 101],
        [72, 92, 95, 98, 112, 100, 103, 99]
    ]
)


L = np.array(
    [
        [2, 1, 0, 0, 0, 0, 0, 0],
        [-9, 0, 0, 0, 0, 0, 0, 0],
        [3, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]
)


theta_hat = np.array(
    [
        [32, 11, 0, 0, 0, 0, 0, 0],
        [-108, 0, 0, 0, 0, 0, 0, 0],
        [42, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]
)


def quantize(
        a: np.array,
        q: np.array = quantization_table,
        reconstruct: bool = False
) -> np.array:
    """
    Quantize one square array (a) using another (q).

    >>> theta_array = theta
    >>> this_L = quantize(theta_array, quantization_table)
    >>> this_L  # compare with matrix `L` above.
    array([[ 2.,  1.,  0.,  0.,  0.,  0.,  0.,  0.],
           [-8.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
           [ 3.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
           [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
           [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
           [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
           [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
           [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.]])

    >>> quantize(this_L, quantization_table, reconstruct=True)  # Compare with `theta_hat` above
    array([[ 32.,  11.,   0.,   0.,   0.,   0.,   0.,   0.],
           [-95.,   0.,   0.,   0.,   0.,   0.,   0.,   0.],
           [ 42.,   0.,   0.,   0.,   0.,   0.,   0.,   0.],
           [  0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.],
           [  0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.],
           [  0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.],
           [  0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.],
           [  0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.]])

    :param a: input np.array.
    :param q: the quantization_table
    :param reconstruct: If False (default), perform quantisation; if True reverse the process.
    :return: the original array (a), modified.
    """

    assert a.shape == q.shape

    m, n = get_m_n(a)

    for i in range(m):
        for j in range(n):
            if reconstruct:
                x = a[i][j] * q[i][j]
            else:
                x = a[i][j] / q[i][j]
            a[i][j] = midtread(x)

    return a


def midtread(x: float) -> int:
    """
    Midtread provides the _nearest_ int.
    Compare similar but different rounding with int() and floor().
    """
    return int(x + 0.5)


# ------------------------------------------------------------------------

if __name__ == "__main__":
    import doctest
    doctest.testmod()
