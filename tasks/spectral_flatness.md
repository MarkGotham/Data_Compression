## Background

As we've seen, periodic signals can be expressed simply in terms of their period.
Noise is more complex as it is 'spread' across frequency range
(the full range in the case of 'white noise').


## Spectral Flatness

We can measure this relative periodicity in terms of a signal's 'flatness':
the _less_ noisy the signal,
the _lower_ the signal's 'flatness' measure,
the _more_ redundancy,
and the _more_ there is to compress.
Random data (e.g., white noise)
is maximally flat (high flatness value, minimum redundancy);
a sine wave is minimally flat (low flatness value, maximum redundancy).

We compute this
by first taking the 
Power Spectral Density (PSD), which is the 
absolute value of the Fast Fourier Transform (FFT) squared.
The spectral flatness then is given by the 
geometric mean of the PSD
divided by the arithmetic mean of the same.

More formally, flatness is given by
$$
{\frac {\exp \left({\frac {1}{N}}\sum _{n=0}^{N-1}\ln x(n)\right)}{{\frac {1}{N}}\sum _{n=0}^{N-1}x(n)}}.
$$


## Task

- Type: Implement
- Task: Implement the spectral flatness.
- Bonus: Use your function to compare a periodic signal, a noisy signal and the combination of the two.
- Reference implementation:
  - `audio.spectral_flatness()`
