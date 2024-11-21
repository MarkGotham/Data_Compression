# coding: utf-8
# Implementations for Data Compression exercises.
# Source: https://github.com/MarkGotham/Data_Compression/tree/main


import numpy as np
from typing import Union


# -------------------------------------------------------------------------------------------------

# Reference delta matrices. Normalisation within functions (e.g., divide by np.sqrt(2) sic not n).

delta_2 = np.array(
    [
        [1, 1],
        [1, -1]
    ]
)

delta_4 = np.array(
    [
        [1, 1, 0, 0],
        [0, 0, 1, 1],
        [1, -1, 0, 0],
        [0, 0, 1, -1]
    ]
)

delta_8 = np.array(
    [
        [1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 1],
        [1, -1, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, -1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, -1, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, -1]
    ]
)


# -------------------------------------------------------------------------------------------------

# Reference h matrices

h_2 = delta_2  # Special case of n=2, all others differ

h_2_norm = h_2 / np.sqrt(2)

h_4 = np.array(
    [
        [1, 1, 1, 1],
        [1, 1, -1, -1],
        [1, -1, 0, 0],
        [0, 0, 1, -1]
    ]
)

h_4_norm = np.array(
    [
        [1, 1, 1, 1],
        [1, 1, -1, -1],
        [np.sqrt(2), -np.sqrt(2), 0, 0],
        [0, 0, np.sqrt(2), -np.sqrt(2)]
    ]
) / 2  # aka np.sqrt(4)


h_8 = np.array(
    [
        [1] * 8,
        ([1] * 4) + ([-1] * 4),
        [1, 1, -1, -1] + ([0] * 4),
        ([0] * 4) + [1, 1, -1, -1],
        [1, -1, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, -1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, -1, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, -1]
    ]
)


h_8_norm = np.array(
    [
        [1] * 8,
        ([1] * 4) + ([-1] * 4),
        ([np.sqrt(2)] * 2) + ([-np.sqrt(2)] * 2) + ([0] * 4),
        ([0] * 4) + ([np.sqrt(2)] * 2) + ([-np.sqrt(2)] * 2),
        [2, -2, 0, 0, 0, 0, 0, 0],
        [0, 0, 2, -2, 0, 0, 0, 0],
        [0, 0, 0, 0, 2, -2, 0, 0],
        [0, 0, 0, 0, 0, 0, 2, -2]
    ]
) / np.sqrt(8)


# -------------------------------------------------------------------------------------------------

# Make h_8 matrix components

def make_h_8_components(
        component: str = "a",
        w: Union[float, int] = 1,
        from_deltas: bool = False
) -> np.array:
    """
    Demostrates making the components for the `h_8`,
    either
        weighted (e.g., `w = 1 / 2` or `1 / np.sqrt(2)`)
        or not (`w = 1`, default, results in binary 1s and 0s)
    and
    either
        `from_deltas` (build from deltas)
        or not (fill in `w` values).

    >>> a = make_h_8_components("a")
    >>> a
    array([[ 1,  1,  0,  0,  0,  0,  0,  0],
           [ 1, -1,  0,  0,  0,  0,  0,  0],
           [ 0,  0,  1,  0,  0,  0,  0,  0],
           [ 0,  0,  0,  1,  0,  0,  0,  0],
           [ 0,  0,  0,  0,  1,  0,  0,  0],
           [ 0,  0,  0,  0,  0,  1,  0,  0],
           [ 0,  0,  0,  0,  0,  0,  1,  0],
           [ 0,  0,  0,  0,  0,  0,  0,  1]])

    >>> b = make_h_8_components("b")
    >>> b
    array([[ 1,  1,  0,  0,  0,  0,  0,  0],
           [ 0,  0,  1,  1,  0,  0,  0,  0],
           [ 1, -1,  0,  0,  0,  0,  0,  0],
           [ 0,  0,  1, -1,  0,  0,  0,  0],
           [ 0,  0,  0,  0,  1,  0,  0,  0],
           [ 0,  0,  0,  0,  0,  1,  0,  0],
           [ 0,  0,  0,  0,  0,  0,  1,  0],
           [ 0,  0,  0,  0,  0,  0,  0,  1]])

    >>> c = make_h_8_components("c")
    >>> c
    array([[ 1,  1,  0,  0,  0,  0,  0,  0],
           [ 0,  0,  1,  1,  0,  0,  0,  0],
           [ 0,  0,  0,  0,  1,  1,  0,  0],
           [ 0,  0,  0,  0,  0,  0,  1,  1],
           [ 1, -1,  0,  0,  0,  0,  0,  0],
           [ 0,  0,  1, -1,  0,  0,  0,  0],
           [ 0,  0,  0,  0,  1, -1,  0,  0],
           [ 0,  0,  0,  0,  0,  0,  1, -1]])

    Confirm the same results from deltas.

    >>> np.allclose(a, make_h_8_components("a", from_deltas=True))
    True

    >>> np.allclose(b, make_h_8_components("b", from_deltas=True))
    True

    >>> np.allclose(c, make_h_8_components("c", from_deltas=True))
    True

    And now weighted.

    >>> a = make_h_8_components("a", w = 1 / np.sqrt(2)).round(3)
    >>> a
    array([[ 0.707,  0.707,  0.   ,  0.   ,  0.   ,  0.   ,  0.   ,  0.   ],
           [ 0.707, -0.707,  0.   ,  0.   ,  0.   ,  0.   ,  0.   ,  0.   ],
           [ 0.   ,  0.   ,  1.   ,  0.   ,  0.   ,  0.   ,  0.   ,  0.   ],
           [ 0.   ,  0.   ,  0.   ,  1.   ,  0.   ,  0.   ,  0.   ,  0.   ],
           [ 0.   ,  0.   ,  0.   ,  0.   ,  1.   ,  0.   ,  0.   ,  0.   ],
           [ 0.   ,  0.   ,  0.   ,  0.   ,  0.   ,  1.   ,  0.   ,  0.   ],
           [ 0.   ,  0.   ,  0.   ,  0.   ,  0.   ,  0.   ,  1.   ,  0.   ],
           [ 0.   ,  0.   ,  0.   ,  0.   ,  0.   ,  0.   ,  0.   ,  1.   ]])

    >>> b = make_h_8_components("b", w = 1 / np.sqrt(2)).round(3)
    >>> b
    array([[ 0.707,  0.707,  0.   ,  0.   ,  0.   ,  0.   ,  0.   ,  0.   ],
           [ 0.   ,  0.   ,  0.707,  0.707,  0.   ,  0.   ,  0.   ,  0.   ],
           [ 0.707, -0.707,  0.   ,  0.   ,  0.   ,  0.   ,  0.   ,  0.   ],
           [ 0.   ,  0.   ,  0.707, -0.707,  0.   ,  0.   ,  0.   ,  0.   ],
           [ 0.   ,  0.   ,  0.   ,  0.   ,  1.   ,  0.   ,  0.   ,  0.   ],
           [ 0.   ,  0.   ,  0.   ,  0.   ,  0.   ,  1.   ,  0.   ,  0.   ],
           [ 0.   ,  0.   ,  0.   ,  0.   ,  0.   ,  0.   ,  1.   ,  0.   ],
           [ 0.   ,  0.   ,  0.   ,  0.   ,  0.   ,  0.   ,  0.   ,  1.   ]])

    >>> c = make_h_8_components("c", w = 1 / np.sqrt(2)).round(3)
    >>> c
    array([[ 0.707,  0.707,  0.   ,  0.   ,  0.   ,  0.   ,  0.   ,  0.   ],
           [ 0.   ,  0.   ,  0.707,  0.707,  0.   ,  0.   ,  0.   ,  0.   ],
           [ 0.   ,  0.   ,  0.   ,  0.   ,  0.707,  0.707,  0.   ,  0.   ],
           [ 0.   ,  0.   ,  0.   ,  0.   ,  0.   ,  0.   ,  0.707,  0.707],
           [ 0.707, -0.707,  0.   ,  0.   ,  0.   ,  0.   ,  0.   ,  0.   ],
           [ 0.   ,  0.   ,  0.707, -0.707,  0.   ,  0.   ,  0.   ,  0.   ],
           [ 0.   ,  0.   ,  0.   ,  0.   ,  0.707, -0.707,  0.   ,  0.   ],
           [ 0.   ,  0.   ,  0.   ,  0.   ,  0.   ,  0.   ,  0.707, -0.707]])

    Or weighted another way

    >>> a = make_h_8_components("a", w = 1 / 2)
    >>> a
    array([[ 0.5,  0.5,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0.5, -0.5,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  1. ,  0. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  1. ,  0. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  1. ,  0. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  1. ,  0. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  1. ,  0. ],
           [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  1. ]])

    """

    if component == "a":
        if from_deltas:
            delta_2 = np.array(
                [
                    [1, 1],
                    [1, -1]
                ]
            ) * w  # weighting / normalisation
            upper = np.pad(delta_2, [(0, 0), (0, 6)], mode='constant', constant_values=0)  # 2 right of delta
            lower = np.pad(make_i_matrix(6), [(0, 0), (2, 0)], mode='constant', constant_values=0)  # 6 left of i
            return np.concatenate((upper, lower), axis=0)
        else:
            return np.array(
                [
                    [w, w, 0, 0, 0, 0, 0, 0],
                    [w, -w, 0, 0, 0, 0, 0, 0],
                    [0, 0, 1, 0, 0, 0, 0, 0],
                    [0, 0, 0, 1, 0, 0, 0, 0],
                    [0, 0, 0, 0, 1, 0, 0, 0],
                    [0, 0, 0, 0, 0, 1, 0, 0],
                    [0, 0, 0, 0, 0, 0, 1, 0],
                    [0, 0, 0, 0, 0, 0, 0, 1]
                ]
            )
    elif component == "b":
        if from_deltas:
            delta_4 = np.array(
                [
                    [1, 1, 0, 0],
                    [0, 0, 1, 1],
                    [1, -1, 0, 0],
                    [0, 0, 1, -1]
                ]
            ) * w  # weighting / normalisation
            upper = np.pad(delta_4, [(0, 0), (0, 4)], mode='constant', constant_values=0)  # 2 right of delta
            lower = np.pad(make_i_matrix(4), [(0, 0), (4, 0)], mode='constant', constant_values=0)  # 6 left of i
            return np.concatenate((upper, lower), axis=0)
        return np.array(
            [
                [w, w, 0, 0, 0, 0, 0, 0],
                [0, 0, w, w, 0, 0, 0, 0],
                [w, -w, 0, 0, 0, 0, 0, 0],
                [0, 0, w, -w, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 1]
            ]
        )
    elif component == "c":
        # Note no if from_deltas option
        return np.array(
            [
                [w, w, 0, 0, 0, 0, 0, 0],
                [0, 0, w, w, 0, 0, 0, 0],
                [0, 0, 0, 0, w, w, 0, 0],
                [0, 0, 0, 0, 0, 0, w, w],
                [w, -w, 0, 0, 0, 0, 0, 0],
                [0, 0, w, -w, 0, 0, 0, 0],
                [0, 0, 0, 0, w, -w, 0, 0],
                [0, 0, 0, 0, 0, 0, w, -w]
            ]
        )
    else:
        raise ValueError("Component must be one of a, b, c")


# -------------------------------------------------------------------------------------------------

def is_orthogonal(
        a: np.array,
        require_i: bool = True
) -> bool:
    """
    Check if an input matrix is orthogonal.
    If True, dot product (`.dot`, `.matmul`, `@`) of the array against a transpose of itself
    gives the i-matrix (see `make_i_matrix`).
    If not `require_i`, then allow any values on the diagonal, and check only for 0 values elsewhere.

    >>> is_orthogonal(h_2)
    False

    >>> is_orthogonal(h_4)
    False

    But if not `require_i`:

    >>> is_orthogonal(h_2, require_i=False)
    True

    >>> is_orthogonal(h_4, require_i=False)
    True

    The normalised matrices are, either way

    >>> is_orthogonal(h_4_norm)
    True

    >>> is_orthogonal(h_8_norm)
    True

    And one other False case.

    >>> is_orthogonal(np.array([range(9)]).reshape(3, 3))
    False

    Note different fraom calling on an invalid shape (non-square) which raises a ValueError.
    """
    m, n = a.shape
    if m != n:
        raise ValueError("Only call on a square shape")
    t = np.transpose(a)
    product = np.matmul(a, t)

    if require_i:
        i = make_i_matrix(m)
        return np.allclose(i, product)
    else:
        for i in range(m):
            for j in range(m):
                if i != j:  # alternatively, if require_i and i==j, assert [i][j] == 0
                    if product[i][j] != 0:
                        return False
        return True


def make_i_matrix(
        n: int = 2
):
    """
    Make an i matrix of size n x n (always square).

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


def make_h4(norm: bool = True) -> np.array:
    """
    Make h_4 from h_2.

    >>> hn_4 = make_h4()
    >>> hn_4
    array([[ 0.5       ,  0.5       ,  0.5       ,  0.5       ],
           [ 0.5       ,  0.5       , -0.5       , -0.5       ],
           [ 0.70710678, -0.70710678,  0.        , -0.        ],
           [ 0.        , -0.        ,  0.70710678, -0.70710678]])

    >>> np.allclose(hn_4, h_4_norm)
    True

    Check on one position that should be sqrt(1/2).

    >>> np.isclose(hn_4[2][0] ** 2, 0.5)
    True

    >>> hn_4 = make_h4(norm=False)
    >>> hn_4
    array([[ 1.,  1.,  1.,  1.],
           [ 1.,  1., -1., -1.],
           [ 1., -1.,  0., -0.],
           [ 0., -0.,  1., -1.]])

    >>> np.allclose(hn_4, h_4)
    True

    """
    if norm:
        h_part = np.kron(h_2_norm, (1, 1))
    else:
        h_part = np.kron(h_2, (1, 1))

    i_2 = make_i_matrix(2)
    i_part = np.kron(i_2, (1, -1))

    if norm:
        return np.concatenate((h_part, i_part), axis=0) / np.sqrt(2)
    else:
        return np.concatenate((h_part, i_part), axis=0)


def make_double_h(
        h_n: np.array,
        norm: bool = True
) -> np.array:
    """
    Make h_2n from h_n.

    E.g., hn_4_norm from h_2_norm:

    >>> hn_4_norm = make_double_h(h_2_norm)
    >>> hn_4_norm
    array([[ 0.5       ,  0.5       ,  0.5       ,  0.5       ],
           [ 0.5       ,  0.5       , -0.5       , -0.5       ],
           [ 0.70710678, -0.70710678,  0.        , -0.        ],
           [ 0.        , -0.        ,  0.70710678, -0.70710678]])

    Check result matches above

    >>> np.allclose(hn_4_norm, make_h4())
    True

    And now without normalisation (note both the `h_2` and `norm=False` arguments).
    >>> hn_4 = make_double_h(h_2, norm=False)
    >>> hn_4
    array([[ 1.,  1.,  1.,  1.],
           [ 1.,  1., -1., -1.],
           [ 1., -1.,  0., -0.],
           [ 0., -0.,  1., -1.]])

    Again, check results match above

    >>> np.allclose(hn_4, make_h4(norm=False))
    True

    Now for h_8 from h_4

    >>> hn_8_norm = make_double_h(hn_4_norm).round(3)
    >>> hn_8_norm
    array([[ 0.354,  0.354,  0.354,  0.354,  0.354,  0.354,  0.354,  0.354],
           [ 0.354,  0.354,  0.354,  0.354, -0.354, -0.354, -0.354, -0.354],
           [ 0.5  ,  0.5  , -0.5  , -0.5  ,  0.   ,  0.   , -0.   , -0.   ],
           [ 0.   ,  0.   , -0.   , -0.   ,  0.5  ,  0.5  , -0.5  , -0.5  ],
           [ 0.707, -0.707,  0.   , -0.   ,  0.   , -0.   ,  0.   , -0.   ],
           [ 0.   , -0.   ,  0.707, -0.707,  0.   , -0.   ,  0.   , -0.   ],
           [ 0.   , -0.   ,  0.   , -0.   ,  0.707, -0.707,  0.   , -0.   ],
           [ 0.   , -0.   ,  0.   , -0.   ,  0.   , -0.   ,  0.707, -0.707]])

    >>> np.allclose(hn_8_norm, h_8_norm.round(3))
    True

    And while we're at it let's confirm `h_8_norm` to be orthogonal.

    Take a look:

    >>> comp = (h_8_norm @ h_8_norm.transpose()).round(3)
    >>> comp
    array([[ 1.,  0.,  0.,  0., -0., -0., -0., -0.],
           [ 0.,  1.,  0.,  0., -0., -0.,  0.,  0.],
           [ 0.,  0.,  1.,  0.,  0.,  0.,  0.,  0.],
           [ 0.,  0.,  0.,  1.,  0.,  0.,  0.,  0.],
           [-0., -0.,  0.,  0.,  1.,  0.,  0.,  0.],
           [-0., -0.,  0.,  0.,  0.,  1.,  0.,  0.],
           [-0.,  0.,  0.,  0.,  0.,  0.,  1.,  0.],
           [-0.,  0.,  0.,  0.,  0.,  0.,  0.,  1.]])

    And confirm:

    >>> is_orthogonal(h_8_norm @ h_8_norm.transpose(), require_i=True)
    True

    And finally, not normalised:

    >>> hn_8 = make_double_h(h_4, norm=False)
    >>> hn_8
    array([[ 1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.],
           [ 1.,  1.,  1.,  1., -1., -1., -1., -1.],
           [ 1.,  1., -1., -1.,  0.,  0.,  0.,  0.],
           [ 0.,  0.,  0.,  0.,  1.,  1., -1., -1.],
           [ 1., -1.,  0., -0.,  0., -0.,  0., -0.],
           [ 0., -0.,  1., -1.,  0., -0.,  0., -0.],
           [ 0., -0.,  0., -0.,  1., -1.,  0., -0.],
           [ 0., -0.,  0., -0.,  0., -0.,  1., -1.]])

    >>> np.allclose(hn_8, h_8)
    True

    """
    h_part = np.kron(h_n, (1, 1))

    m, n = h_n.shape
    if m != n:
        raise ValueError("Only call on a square shape")

    i_n = make_i_matrix(n)
    i_part = np.kron(i_n, (1, -1))

    if norm:
        return np.concatenate((h_part, i_part), axis=0) / np.sqrt(2)
    else:
        return np.concatenate((h_part, i_part), axis=0)


# -------------------------------------------------------------------------------------------------

def values_from_salomon():
    """
    A test function on some values from Salomon.
    Returns True if no assertion fails.

    >>> values_from_salomon()
    True
    """
    initial_values = np.array([255, 244, 192, 159, 127, 95, 63, 32])

    a1 = make_h_8_components("c", w=1/2)
    a1_product = a1 @ initial_values
    a1_expected = np.array([249.5, 175.5, 111, 47.5, 5.5, 16.5, 16, 15.5])
    assert np.allclose(a1_product, a1_expected)

    a2 = make_h_8_components("b", w=1/2)
    a2_product = a2 @ np.array([239.5, 175.5, 111, 47.5, 15.5, 16.5, 16, 15.5]),
    # NB: != `a1_expected`: 2x slips/typos in Salomon-Motta: 249->239 and 5.5->15.5.
    # Here, we use Salomon-Motta actual return values to continue with the next steps.
    a2_expected = np.array([207.5, 79.25, 32.0, 31.75, 15.5, 16.5, 16.0, 15.5])
    assert np.allclose(a2_product, a2_expected)

    a3 = make_h_8_components("a", w=1/2)
    a3_product = a3 @ a2_expected  # does = a2_expected in this case.
    a3_expected = np.array([143.375, 64.125, 32., 31.75, 15.5, 16.5, 16., 15.5])
    assert np.allclose(a3_product, a3_expected)
    return True


# -------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    import doctest
    doctest.testmod()
