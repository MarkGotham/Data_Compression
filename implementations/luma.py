# -*- coding: utf-8 -*-

rgb_weights_1 = (0.2126, 0.7152, 0.0722)
rgb_weights_2 = (0.299, 0.587, 0.114)


# Demo integer rounding
rgb_weights_ints_1 = [round(10 * x) for x in rgb_weights_1]
assert rgb_weights_ints_1 == [2, 7, 1]

rgb_weights_ints_2 = [round(10 * x) for x in rgb_weights_2]
assert rgb_weights_ints_2 == [3, 6, 1]


def brightness(
    rgb: tuple,
    rgb_weights: tuple = rgb_weights_1
) -> float:
    """
    Calculate luminance from rgb.

    >>> brightness((200, 100, 200))
    128.48

    The above uses default weightings, but others can be used:

    >>> brightness((200, 100, 200), rgb_weights_2)
    141.3

    :param rgb: a tuple with three values for r, g, and b
    :param rgb_weights: a tuple with three values for the r, g, and b weightings
    :return: float for the combined, weighted luminance.
    """
    r, g, b = rgb
    r_weight, g_weight, b_weight = rgb_weights

    return (r * r_weight) + (g * g_weight) + (b * b_weight)


def c_b(
    b: int,
    luma: float,
    k_b: float = rgb_weights_1[2]
):
    return (b - luma) / 2*(1 - k_b)


def c_r(
    r: int,
    luma: float,
    k_r: float = rgb_weights_1[0]
):
    return (r - luma) / 2*(1 - k_r)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
