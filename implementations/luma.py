# coding: utf-8
# Implementations for Data Compression exercises.
# Source: https://github.com/MarkGotham/Data_Compression/tree/main


import numpy as np

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
) -> float:
    """
    Calculate the blue chrominance component from B and luminance values.
    >>> rgb = (100, 150, 200)
    >>> l = brightness(rgb)
    >>> l
    142.98

    >>> c_b(rgb[2], l)
    26.451578000000005
    """
    return (b - luma) / 2 * (1 - k_b)


def c_r(
        r: int,
        luma: float,
        k_r: float = rgb_weights_1[0]
):
    """
    Calculate the red chrominance component from R and luminance values.
    >>> rgb = (100, 150, 200)
    >>> l = brightness(rgb)
    >>> c_r(200, l)
    22.448774000000004
    """
    return (r - luma) / 2 * (1 - k_r)


test_array = np.array([  # first 16x16 of `ski.data.astronaut()`
    [[154, 147, 151],
     [109, 103, 124],
     [63, 58, 102],
     [54, 51, 98],
     [76, 76, 106],
     [100, 100, 104],
     [124, 121, 122],
     [139, 135, 133],
     [148, 141, 138],
     [141, 134, 130],
     [123, 115, 111],
     [100, 90, 94],
     [62, 56, 73],
     [21, 15, 40],
     [8, 2, 25],
     [3, 1, 10]],

    [[177, 171, 171],
     [144, 141, 143],
     [113, 114, 124],
     [106, 107, 120],
     [128, 128, 131],
     [148, 144, 138],
     [163, 158, 155],
     [170, 165, 159],
     [173, 167, 159],
     [159, 150, 146],
     [133, 124, 120],
     [96, 86, 92],
     [48, 42, 62],
     [17, 6, 43],
     [9, 3, 27],
     [3, 1, 8]],

    [[201, 194, 193],
     [182, 178, 175],
     [168, 165, 164],
     [159, 157, 157],
     [167, 165, 161],
     [186, 180, 175],
     [190, 185, 179],
     [192, 186, 174],
     [183, 176, 165],
     [163, 154, 149],
     [125, 115, 118],
     [79, 69, 85],
     [29, 21, 56],
     [14, 3, 37],
     [9, 3, 27],
     [4, 2, 13]],

    [[220, 213, 210],
     [214, 206, 206],
     [202, 198, 196],
     [197, 191, 193],
     [200, 194, 196],
     [202, 198, 189],
     [205, 202, 192],
     [198, 194, 185],
     [181, 174, 167],
     [149, 142, 138],
     [108, 101, 108],
     [55, 45, 74],
     [21, 10, 50],
     [18, 5, 43],
     [11, 4, 31],
     [5, 2, 15]],

    [[232, 223, 223],
     [226, 220, 215],
     [221, 215, 210],
     [215, 210, 206],
     [221, 211, 213],
     [212, 206, 200],
     [212, 206, 201],
     [194, 187, 181],
     [168, 161, 155],
     [131, 123, 124],
     [85, 76, 91],
     [35, 25, 68],
     [20, 7, 47],
     [18, 6, 44],
     [13, 3, 34],
     [7, 2, 22]],

    [[236, 229, 226],
     [235, 228, 224],
     [229, 224, 219],
     [226, 218, 218],
     [224, 216, 216],
     [216, 210, 207],
     [202, 198, 187],
     [181, 175, 165],
     [151, 143, 140],
     [108, 101, 107],
     [53, 49, 78],
     [28, 13, 61],
     [25, 13, 58],
     [18, 5, 44],
     [13, 4, 34],
     [8, 3, 24]],

    [[235, 229, 225],
     [237, 230, 228],
     [233, 226, 224],
     [228, 224, 220],
     [221, 215, 209],
     [212, 205, 200],
     [191, 184, 176],
     [168, 159, 156],
     [129, 121, 122],
     [81, 73, 92],
     [39, 30, 78],
     [29, 19, 65],
     [26, 11, 57],
     [16, 4, 39],
     [11, 4, 31],
     [9, 3, 28]],

    [[232, 226, 220],
     [235, 226, 226],
     [231, 223, 222],
     [225, 219, 212],
     [216, 212, 205],
     [207, 200, 197],
     [188, 182, 177],
     [154, 149, 144],
     [107, 102, 111],
     [55, 49, 90],
     [36, 26, 77],
     [36, 22, 77],
     [31, 16, 67],
     [17, 4, 41],
     [12, 4, 32],
     [7, 2, 21]],

    [[229, 223, 218],
     [231, 223, 218],
     [229, 220, 218],
     [222, 216, 211],
     [215, 211, 202],
     [204, 200, 191],
     [184, 179, 172],
     [150, 145, 140],
     [102, 95, 105],
     [49, 41, 86],
     [39, 29, 83],
     [34, 21, 73],
     [28, 14, 63],
     [20, 8, 46],
     [13, 4, 33],
     [8, 2, 24]],

    [[227, 221, 218],
     [228, 222, 217],
     [224, 218, 212],
     [219, 213, 206],
     [214, 210, 200],
     [204, 201, 192],
     [184, 178, 168],
     [156, 151, 147],
     [114, 110, 115],
     [69, 63, 93],
     [39, 31, 82],
     [36, 22, 76],
     [28, 14, 63],
     [22, 11, 50],
     [15, 4, 39],
     [10, 3, 28]],

    [[228, 222, 217],
     [227, 221, 216],
     [225, 219, 211],
     [221, 217, 210],
     [214, 211, 203],
     [209, 203, 196],
     [193, 188, 179],
     [175, 165, 164],
     [143, 138, 136],
     [105, 98, 110],
     [59, 57, 86],
     [35, 27, 75],
     [29, 16, 64],
     [21, 8, 49],
     [15, 5, 37],
     [9, 2, 25]],

    [[226, 219, 212],
     [229, 222, 220],
     [227, 220, 217],
     [227, 219, 214],
     [217, 212, 206],
     [214, 209, 198],
     [204, 197, 188],
     [187, 181, 173],
     [164, 159, 151],
     [135, 131, 123],
     [96, 90, 103],
     [54, 45, 78],
     [26, 16, 57],
     [21, 8, 47],
     [18, 7, 42],
     [11, 4, 30]],

    [[228, 222, 215],
     [227, 222, 214],
     [230, 224, 219],
     [227, 219, 220],
     [220, 214, 208],
     [219, 212, 208],
     [210, 206, 197],
     [200, 196, 183],
     [183, 176, 164],
     [158, 151, 140],
     [130, 121, 122],
     [83, 77, 89],
     [40, 34, 71],
     [26, 15, 59],
     [18, 5, 44],
     [10, 4, 30]],

    [[233, 226, 223],
     [229, 223, 221],
     [228, 220, 217],
     [224, 216, 214],
     [218, 212, 211],
     [214, 207, 203],
     [210, 203, 200],
     [204, 199, 190],
     [194, 188, 177],
     [174, 169, 157],
     [149, 145, 134],
     [118, 110, 109],
     [74, 67, 79],
     [34, 24, 60],
     [16, 5, 40],
     [11, 4, 30]],

    [[231, 223, 220],
     [225, 218, 215],
     [220, 214, 215],
     [214, 206, 208],
     [206, 198, 196],
     [197, 189, 185],
     [200, 192, 189],
     [198, 192, 183],
     [193, 188, 172],
     [187, 176, 168],
     [168, 158, 150],
     [140, 133, 125],
     [108, 101, 100],
     [62, 55, 77],
     [24, 14, 50],
     [13, 4, 35]],

    [[227, 218, 217],
     [214, 208, 201],
     [207, 200, 201],
     [190, 183, 186],
     [178, 170, 173],
     [173, 162, 172],
     [176, 167, 167],
     [175, 167, 165],
     [176, 169, 160],
     [178, 169, 161],
     [165, 158, 152],
     [146, 137, 124],
     [126, 116, 110],
     [88, 83, 89],
     [44, 36, 59],
     [17, 7, 39]]
])


def mb_to_luma_cb_cr(
        macro_block: list[list],
        luma_only: bool = False
):
    """
    For any 16x16 RGB array,
    Return luminance values (16x16)
    and two 8×8 blocks of chrominance samples (sampling every other value).

    >>> three_returns = mb_to_luma_cb_cr(test_array)
    >>> len(three_returns[0])  # luminance
    16

    >>> len(three_returns[1])  # c_b
    8

    >>> len(three_returns[2])  # c_r
    8

    If `luma_only`, the only return the luma array.
    >>> one_return = mb_to_luma_cb_cr(test_array, luma_only=True)
    >>> len(one_return)  # luminance
    16
    """
    luma_block = []
    for i in macro_block:
        luma_block.append([brightness(x) for x in i])

    if luma_only:
        return luma_block

    c_b_block = cbr_8_from_16(luma_block, macro_block, b_not_r=True)
    c_r_block = cbr_8_from_16(luma_block, macro_block, b_not_r=False)
    return luma_block, c_b_block, c_r_block


def cbr_8_from_16(
        luma_block: np.array,
        macro_block: np.array,
        b_not_r: bool = True
) -> np.array:
    """
    Shared function for creating 8x8 c_b or c_r arrays from a
    16x16 source and luma.
    """
    if b_not_r:
        index = 2  # B
    else:
        index = 0  # R

    new_block = [[0] * 8] * 8
    for i in range(8):  # for 8x8
        for j in range(8):
            luma_val = luma_block[i * 2][j * 2]
            br = macro_block[i * 2][j * 2][index]
            if b_not_r:
                new_block[i][j] = c_b(br, luma_val)  # NB not [i * 2][j * 2]
            else:
                new_block[i][j] = c_r(br, luma_val)

    return new_block


if __name__ == "__main__":
    import doctest

    doctest.testmod()
