## Background

The JPEG compression routine includes the following steps:
1. split images of any size into 8x8 size block
2. subtract 128 from each value,
3. implement and apply the DCT (see 'DCT' below) 
4. 'quantize' using the 'uniform midtread quantization' (see 'Quantization' below)
5. Encode the DC coefficient (position (0, 0)) and the AC coefficients using Huffman coding. 


### DCT

The discrete cosine transform (DCT) is a variant of the discrete Fourier transform (DFT) that only takes the cosines.
So, we're still in the business of expressing a complex signal in terms of periodic components,
here a sum of cosine functions.


### Quantization

In this context, 'Quantization' involves taking each value in an 8x8 matrix and:
- dividing by the corresponding value in the reference matrix, such as the one given as **Q** below.
- rounding to the nearest integer using 'midtread' mapping (`int(x + 0.5)`, see `matrix_basics.midtread`).

$$
{\bf Q} = \begin{pmatrix}
16 & 11 & 10 & 16 & 24 & 40 & 51 & 61\\
12 & 12 & 14 & 19 & 26 & 58 & 60 & 55\\
14 & 13 & 16 & 24 & 40 & 57 & 69 & 56\\
14 & 17 & 22 & 29 & 51 & 87 & 80 & 62\\
18 & 22 & 37 & 56 & 68 & 109 & 103 & 77\\
24 & 35 & 55 & 64 & 81 & 104 & 113 & 92\\
49 & 64 & 78 & 87 & 103 & 121 & 120 & 101\\
72 & 92 & 95 & 98 & 112 & 100 & 103 & 99
\end{pmatrix}
$$

The reconstruction involves the same process in reverse, now multiplying rather than dividing.


## Task

- Type: Implement
- Task: Implement the quantization and reconstruction processes described in steps 3–4 above (and 1-2 if you like).
- Reference implementation:
  - Sample values are given `jpeg.continuous_tone_pattern`, or use your own
  - for DCT: local implementation at `jpeg.dct` and/or remote in [scipy](https://docs.scipy.org/doc/scipy/reference/generated/scipy.fftpack.dct.html)
    - Bonus: create from scratch.
  - for quantization and reconstruction: `matrix_basics.quantize()` including arguments for:
    - `reconstruct` (bool)
    - the quantization table to use (with **Q** above as default: `matrix_basics.quantization_table`)
  - for DCT, create (bonus) or use `jpeg.dct_matrix` and/or [scipy](https://docs.scipy.org/doc/scipy/reference/generated/scipy.fftpack.dct.html)


## Also on this repository

The [`fourier_rountrip` notebook](https://github.com/MarkGotham/Data_Compression/blob/main/fourier_roundtrip.ipynb)
runs a similar roundtrip, with the following differences:
- no consideration of quantization,
- standard Fourier (not DCT),
- no recourse to local implementations on the repo (useful in case of set up issues).

