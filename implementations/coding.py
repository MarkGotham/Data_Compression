# coding: utf-8
# Implementations for Data Compression exercises.
# Source: https://github.com/MarkGotham/Data_Compression/tree/main


from collections import Counter
from heapq import heappush, heappop, heapify
import numpy as np


def huffman_encode(
        symb_freq_dict: dict,
        as_dict: bool = True
):
    """
    For a given dict (mapping symbols-to-weights)
    return a mapping from symbol to Huffman encoded binary.

    >>> this_dict = Counter("stutterer")
    >>> this_dict
    Counter({'t': 3, 'e': 2, 'r': 2, 's': 1, 'u': 1})

    >>> huffman_encode(this_dict)
    {'e': '00', 'r': '01', 's': '100', 'u': '101', 't': '11'}

    >>> huffman_encode(this_dict, as_dict=False)
    [['e', '00'], ['r', '01'], ['t', '11'], ['s', '100'], ['u', '101']]

    Note that the shorter binary values are assigned to the more-used characters (t, e, r).

    Now for the special case of a `pangram` which uses every letter of the alphabet at least once.
    Here's one using the 26 English lower case letters plus one for the space ` ` (27 total).
    >>> pangram = "the quick brown fox jumps over the lazy dog"
    >>> this_dict = Counter(pangram)
    >>> encoded = huffman_encode(this_dict)
    >>> len(encoded)
    27

    And finally, a "perfect pangram" using every letter of given alphabet EXACTLY once
    (here, Finish without the `loan letters` only used for foreign words).
    >>> p_pangram = "Törkylempijävongahdus"
    >>> this_dict = Counter(p_pangram)
    >>> encoded = huffman_encode(this_dict)
    >>> len(encoded) == len(p_pangram)
    True

    """
    heap = [[wt, [sym, ""]] for sym, wt in symb_freq_dict.items()]
    heapify(heap)  # Transform list into a heap, in-place, in linear time.
    while len(heap) > 1:
        lo = heappop(heap)  # Pop the smallest item from the heap
        hi = heappop(heap)  # .. twice
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    if as_dict:
        out_dict = {}
        for x in heap[0][1:]:
            out_dict[x[0]] = x[1]
        return out_dict
    else:
        return sorted(heappop(heap)[1:], key=lambda p: (len(p[-1]), p))


def entropy(prob_list: list):
    """
    The entropy of a discrete random variable X.

    >>> prob_list_1 = [1/6] * 3 + [1/8] * 4
    >>> entropy(prob_list_1)
    2.792481250360578

    >>> prob_list_2 = [1/12] * 6 + [1/4] * 2
    >>> entropy(prob_list_2) == entropy(prob_list_1)
    True

    :param prob_list: A list of probabilities p(x) that sum to 1.
    """
    assert np.isclose(sum(prob_list), 1)
    return -sum([px * np.log2(px) for px in prob_list])


if __name__ == "__main__":
    import doctest
    doctest.testmod()
