# coding: utf-8
# Implementations for Data Compression exercises.
# Source: https://github.com/MarkGotham/Data_Compression/tree/main


"""
An implementation of the zigzag read/write method.

Note the alternative a lookup ;):
https://github.com/python-pillow/Pillow/blob/6956d0b2853f5c7ec5f6ec4c60725c5a7ee73aeb/src/PIL/JpegImagePlugin.py#L611)
"""


import numpy as np
from typing import Union

import logging


# Shared values

right = (0, 1)
down_left = (1, -1)
down = (1, 0)
up_right = (-1, 1)


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


def transform(
        a: np.array,
        shape: Union[tuple, None] = None,
        moves_order: list = [right, down_left, down, up_right],
        log_moves: bool = True,

) -> np.array:
    """
    Implements the Zigzag scan of a matrix as used in jpeg.
    Use this same `transform` function to convert
    from flat (1 x n) to shape (m x n, specifying the destination shape with the `shape` argument)
    and vice versa (mxn source to flat 1xn).

    Here's a demo with one starting array, and 2 different re-shapings with round trip checks.

    >>> a = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])

    Re-shape 1:

    >>> r34 = a.reshape(3, 4)
    >>> r34
    array([[ 1,  2,  3,  4],
           [ 5,  6,  7,  8],
           [ 9, 10, 11, 12]])

    Transform from shape to flat 1:

    >>> zr34 = transform(r34, moves_order=[right, down_left, down, up_right])
    >>> zr34
    array([ 1,  2,  5,  9,  6,  3,  4,  7, 10, 11,  8, 12])

    Run again to revert to initial shape 1.

    >>> and_back = transform(zr34, shape = (3, 4), moves_order=[right, down_left, down, up_right])
    >>> and_back
    array([[1, 2, 3, 4],
           [5, 6, 7, 8],
           [9, 10, 11, 12]], dtype=object)

    Re-shape 1:

    >>> r43 = a.reshape((4, 3))
    >>> r43
    array([[ 1,  2,  3],
           [ 4,  5,  6],
           [ 7,  8,  9],
           [10, 11, 12]])

    Transform from shape to flat 2:

    >>> zr43 = transform(r43, moves_order=[right, down_left, down, up_right])
    >>> zr43
    array([ 1,  2,  4,  7,  5,  3,  6,  8, 10, 11,  9, 12])

    Run again to revert to initial shape 2.

    >>> and_back_again = transform(zr43, shape = (4, 3), moves_order=[right, down_left, down, up_right])
    >>> and_back_again
    array([[1, 2, 3],
           [4, 5, 6],
           [7, 8, 9],
           [10, 11, 12]], dtype=object)

    :param a: a numpy array, size m * n, not necessarily a square.
     If either of the dimensions is 1 then it's transformed to a new shape of dimensions given by `shape`.
     Otherwise, (m != 1m n!= 1) then it's transformed to a flat list, 1 x m*n.
    :param shape: the 2-d dimensions of the array, for use when the input is 1 x n.
    :param moves_order: The sequence of steps. Adapted within, so list (not tuple) & re-set for each call.
    :param log_moves: Keep a log of each movement (bool).
    :return: a numpy array either in 1D (length m * n) or of shape m * n as defined above.
    """
    if log_moves:
        logging.basicConfig(filename="zigzag.log", level=logging.INFO)
        logging.info(f"*** Starting log. Starting at top-left position. First move will be {moves_order[0]}.")

    # Init
    m, n = get_m_n(a)  # shape
    i, j = 0, 0  # position
    current_move_index = 0
    convert_shape_to_flat = True  # convert from shape to flat, or from flat to shape

    logging.info(f"m, n shape of input = {m, n}")

    if n == 1:
        m, n = n, m
        a = a.transpose()
        logging.info(f"Transposing, so m, n shape of input now {m, n}")

    # Direction
    if m == 1:
        convert_shape_to_flat = False
        list_form = a  # given
        shape_form = np.array([None] * m * n).reshape(shape)  # init ...
        shape_form[0][0] = list_form[0]  # ... and first value move
        m, n = shape
    elif m > 1:
        # convert_shape_to_flat = True
        list_form = [a[0][0]]  # init, first value moved.
        shape_form = a  # given
    else:
        raise ValueError("Shape of input array must be m x n or 1 x n. I.e., m > 0.")

    num_moved = 1  # a counter, note that we are already at 1.

    while num_moved < (m * n):

        # Move position in the m x n
        logging.info(f"moving by {moves_order[current_move_index]}")
        i += moves_order[current_move_index][0]
        j += moves_order[current_move_index][1]

        # Recording value from source to destination
        if convert_shape_to_flat:
            list_form.append(shape_form[i][j])
            logging.info(f"Adding {shape_form[i][j]} to the list")
            logging.info(f"List now: {list_form}")
        else:  # flat to shape
            shape_form[i][j] = list_form[num_moved]
            logging.info(f"Inserting {list_form[num_moved]} into the array a position {i, j}")
            logging.info(f"Array now: {shape_form}")

        # Update move index (if necessary, shared)
        if moves_order[current_move_index] in [right, down]:
            current_move_index += 1
        elif moves_order[current_move_index] == down_left:
            if j == 0:
                logging.info(f"Last move was {moves_order[current_move_index]}. Now at left-most column.")
                if i == m - 1:
                    logging.info(f"... and at bottom-most row.")
                current_move_index += 1
            elif i == m - 1:  # sic elif. Both case handled above.
                logging.info(f"Last move was {moves_order[current_move_index]}. Now at bottom-most row.")
                current_move_index += 1
        elif moves_order[current_move_index] == up_right:
            if i == 0:
                logging.info(f"Last move was {moves_order[current_move_index]}. Now at top-most row.")
                current_move_index += 1
            elif j == n - 1:
                logging.info(f"Last move was {moves_order[current_move_index]}. Now at right-most column.")
                current_move_index += 1
        else:
            raise ValueError("Unknown issue with the `moves_order[current_move_index]`")
        current_move_index = current_move_index % len(moves_order)

        # Update move order (if necessary, shared)
        if i == m - 1:
            logging.info("At bottom-most row: changing next scheduled d -> r")
            for x in range(len(moves_order)):
                if moves_order[x] == down:
                    moves_order[x] = right
                    logging.info(f"Scheduled down-move found at index {x}. Changing")
        if j == n - 1:
            # moves_order[0] = down  # not reliable
            logging.info(f"At right-most column: changing next scheduled r -> d")
            for x in range(len(moves_order)):
                if moves_order[x] == right:
                    moves_order[x] = down
                    logging.info(f"Scheduled right-move found at index {x}. Changing")

        logging.info(f"Current full moves order schedule = {moves_order}")
        logging.info(f"Current position = {i, j}")
        num_moved += 1

    if convert_shape_to_flat:
        return np.array(list_form)
    else:
        return np.array(shape_form)


# -------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    import doctest
    doctest.testmod()
