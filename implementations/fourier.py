# coding: utf-8

import numpy as np


def square_dft_matrix(n: int) -> np.array:
    """
    Creates a DFT matrix of size len(x) x len(x).

    Check this (from scratch) against built in `np.eye`.

    >>> n = 8
    >>> np_square = np.fft.fft(np.eye(n)) / np.sqrt(n)
    >>> np.isclose(square_dft_matrix(n).all(), np_square.all())
    True

    :param n: the size (length and width) of the square matrix. Int.
    return: a DFT matix of size len(x) x len(x).
    """
    X = np.zeros((n, n), dtype=np.complex128)
    for i in range(n):
        for j in range(n):
            X[i, j] = np.exp(-2j * np.pi * i * j / n)
    return X / np.sqrt(n)


def dft_at_once(a: np.array) -> np.array:
    """
    Implement Fourier transform from a signal
    using `square_dft_matrix()` to make the square matrix separately.
    """
    a = a.astype(np.complex128)
    n = len(a)
    dft_mat = square_dft_matrix(n)
    return np.dot(dft_mat, a)


def dft_dot_product_steps(x: np.array) -> np.array:
    """
    Implement Fourier transform from a signal
    by creating a square DFT matrix and doing dot product together.
    """
    x = x.astype(np.complex128)
    n = len(x)
    n_by_1 = []
    for i in range(n):
        nums = []
        for j in range(n):
            sq = np.exp(-2j * np.pi * i * j / n)  # value from what would be the square dft matrix
            nums.append(x[i] * sq)
        n_by_1.append(sum(nums))

    return np.array(n_by_1).astype(np.complex128)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
