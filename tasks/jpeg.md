## Background

The JPEG compression routine includes the following steps:
- split images of any size into 8x8 size block
- subtract 128 from each value,
- implement and apply the DCT (a variant of the DFT that only takes the cosines),
- 'quantize' using the 'uniform midtread quantization' where each value in the 8x8 matrix is:
  - divided by the corresponding value in the reference matrix given as **Q** below.
  - rounded each value to the nearest integer using midtread.

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

The reconstruction involves the same process in reverse.


## Task

- Type: Implement
- Task: Implement the quantization and reconstruction processes described above.
- Reference implementation:
  - quantize and reconstruct: `matrix_basics.quantize()` including arguments for:
    - `reconstruct` (bool)
    - the quantization table to use (with **Q** above as default: `matrix_basics.quantization_table`)
  - Sample values are given `jpeg.continuous_tone_pattern`
  - for DCT, create (bonus) or use `jpeg.dct_matrix` and/or [scipy](https://docs.scipy.org/doc/scipy/reference/generated/scipy.fftpack.dct.html)
