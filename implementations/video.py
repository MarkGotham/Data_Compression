# coding: utf-8
# Implementations for Data Compression exercises.
# Source: https://github.com/MarkGotham/Data_Compression/tree/main


import numpy as np


def distortion_measure(
        b: np.array,
        c: np.array,
        abs_not_square: bool = True
) -> float:
    """
    Shared functionality for
    `mean_abs_diff` and `mean_sq_diff`.

    >>> frame_1 = np.array([[0, 1], [2, 3]])
    >>> frame_2 = np.array([[0, 1], [2, 4]])
    >>> frame_3 = np.array([[0, 1], [2, 5]])

    The `distortion_measure` is the same as `mean_abs_diff` when `abs_not_square = True`
    >>> mean_abs_diff(frame_1, frame_2)
    0.25

    >>> distortion_measure(frame_1, frame_2) == mean_abs_diff(frame_1, frame_2)
    True

    The `distortion_measure` is the same as `mean_sq_diff` when `abs_not_square = False`
    >>> mean_sq_diff(frame_1, frame_3)
    1.0

    >>> distortion_measure(frame_1, frame_3, abs_not_square = False) == mean_sq_diff(frame_1, frame_3)
    True

    And sometimes, the values are such that they're the same either way.

    >>> mean_abs_diff(frame_1, frame_2) == mean_sq_diff(frame_1, frame_2)
    True

    """
    assert b.shape == c.shape
    m, n = b.shape
    assert m == n
    running_value = 0

    for i in range(m):
        for j in range(n):
            diff = b[i][j] - c[i][j]
            if abs_not_square:
                running_value += np.abs(diff)
            else:
                running_value += np.square(diff)
    return running_value / np.square(m)


def mean_abs_diff(
        b: np.array,
        c: np.array
) -> float:
    """
    Calculates the
    mean absolute difference (a.k.a. mean absolute error) distortion measure:
    the average of the absolute differences between corresponding pixels in two frames
    (a block, here `b` and a candidate, here `c`).
    See doctests at `distortion_measure`.
    """
    return distortion_measure(b, c, abs_not_square=True)


def mean_sq_diff(
        b: np.array,
        c: np.array
):
    """
    Calculates the
    mean square difference distortion measure:
    as for `mean_abs_diff` but squaring each difference value.
    """
    return distortion_measure(b, c, abs_not_square=False)


def block_search(
        b: np.array,
        c: np.array,
        m_n_index: tuple[int],
        height_width: tuple[int],
        dy_dx: tuple[int],
        abs_not_square: bool = True
) -> tuple:
    """
    Perform a block search in the given region,
    specifically for:
    one reference block within the frame `b`,
    all corresponding blocks in the neighbouring frame `c`,
    within a search area defined by the values dx, and dy.
    Any argument combination that extends beyond the frame shape raises an error.

    >>> ref, comp = make_test_array_block()
    >>> ref
    array([[0, 0, 0, 0, 0],
           [0, 1, 1, 1, 0],
           [0, 1, 0, 1, 0],
           [0, 1, 1, 1, 0],
           [0, 0, 0, 0, 0]])

    >>> comp
    array([[0, 1, 1, 1, 0],
           [0, 1, 0, 1, 0],
           [0, 1, 1, 1, 0],
           [0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0]])

    >>> block_search(ref, comp, (1, 1), (3, 3), (1, 1))
    (0, 1)

    :param b: The total reference frame (within which the reference block is situated).
    :param c: The total neighbouring frame (within which we search).
    :param m_n_index: The top-left position of the reference block (m- and n-axes). Tuple.
    :param height_width: The height and width of the reference block (m- and n-axes). Tuple.
    :param dy_dx: maximum displacement parameter in the m- and n- axes. 2x constraints on size. Tuple.

    :return: An (i, j) for the coordinate of the top left corner of the best match area in `c`.
    """
    assert b.shape == c.shape  # Not strictly necessary but expected in all realistic scenarios.

    m, n = m_n_index

    if m >= b.shape[0]:
        raise ValueError(f"The m-coordinate {m} is outside the frame (shape {b.shape}).")
    if n >= b.shape[1]:
        raise ValueError(f"The n-coordinate {n} is outside the frame (shape {b.shape}).")

    dy, dx = dy_dx
    if m < dy:
        raise ValueError(f"The displacement parameter dy ({dy}) must be less than the m-coordinate.")
    if n < dx:
        raise ValueError(f"The displacement parameter dx ({dx}) must be less than the n-coordinate.")

    height, width = height_width
    if m + height + dy > b.shape[0]:
        raise ValueError(f"The maximum displacement in m- is outside the frame (shape {b.shape}).")
    if n + width + dx > b.shape[1]:
        raise ValueError(f"The maximum displacement in n- is outside the frame (shape {b.shape}).")

    best_i_j = (None, None)
    least_diff = 1000

    b_part = b[m: m + height, n: n + width]

    comparison_count = 0
    for i in range(m - dy, m + dy + 1):
        for j in range(n - dx, n + dx + 1):
            c_part = c[i: i + height, j: j + width]
            d = distortion_measure(b_part, c_part, abs_not_square)
            if d < least_diff:
                least_diff = d
                best_i_j = (i, j)
            comparison_count += 1

    assert comparison_count == ((2 * dx) + 1) * ((2 * dy) + 1)
    return best_i_j


def make_test_array_block():
    """Make a test array pair for a simple block search demo."""
    shared = [
        [0, 1, 1, 1, 0],
        [0, 1, 0, 1, 0],
        [0, 1, 1, 1, 0]
    ]
    empty_row = [[0] * 5]
    return np.array(empty_row + shared + empty_row), np.array(shared + empty_row + empty_row)


def make_test_array_log():
    """Make a test array to match (in the simplest way) the log search example."""
    test_array = np.zeros((17, 17))
    test_array[4, 8] = 0.25
    test_array[4, 12] = 0.5
    test_array[4, 14] = 0.75
    test_array[4, 15] = 1
    return test_array


def logarithmic_search_2d_demo() -> tuple:
    """
    A demonstration of the two-dimensional logarithmic search
    for two 17x17 arrays, starting at the central note (9, 9).
    We start at the central node, and step size 8,
    reducing the search area in each step until we get down to one node.
    Return the best match coordinate as an (m, n) tuple.

    >>> logarithmic_search_2d_demo()
    (4, 15)

    """
    test_array = make_test_array_log()
    reference_array = np.ones((17, 17))
    assert test_array.shape == reference_array.shape
    m, n = test_array.shape

    s = int(
        2 ** (
            np.floor(
                np.log2(
                    m / 2
                )
            ) - 1
        )
    )

    a = int(m / 2)
    b = int(n / 2)
    ref_coord = (a, b)
    min_diff = np.abs(
        test_array[a, b] - reference_array[a, b]
    )

    while s > 1:  # For s > 1, search 4 locations
        new_coord = None
        a, b = ref_coord

        for this_coord in (
                # Four in diamond shape around central point:
                (a + s, b),
                (a - s, b),
                (a, b + s),
                (a, b - s)
        ):
            diff = np.abs(
                test_array[
                    this_coord[0], this_coord[1]
                ] - reference_array[
                    this_coord[0], this_coord[1]
                ]
            )
            if diff < min_diff:
                min_diff = diff
                new_coord = (this_coord[0], this_coord[1])

        if new_coord:
            ref_coord = new_coord
        else:
            s = int(s/2)  # shrink area

    # s = 1, search 8 locations
    for this_coord in (
            # Four diamond as before:
            (a + 1, b),
            (a - 1, b),
            (a, b + 1),
            (a, b - 1),
            # Four corners only this time:
            (a + 1, b + 1),
            (a - 1, b - 1),
            (a - 1, b + 1),
            (a + 1, b - 1)
    ):
        diff = np.abs(
            test_array[
                this_coord[0], this_coord[1]
            ] - reference_array[
                this_coord[0], this_coord[1]
            ]
        )
        if diff < min_diff:
            min_diff = diff
            ref_coord = (this_coord[0], this_coord[1])  # Note: no more s updates.

    return ref_coord


if __name__ == "__main__":
    import doctest
    doctest.testmod()
