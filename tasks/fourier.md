## Background

Much of the data we work with is periodic, or at least it can be _approximated_ with periodic functions.

Given the shared basis in waves, this applies to both sound and image data.

The Fourier series and Fourier transform serve to extract and handle that periodicity
in ways that have proven widely useful, including for data compression.

Now for some maths.

$F = Af$, where 
$f$ is a time signal,
$F$ is the discrete Fourier transform (DFT),
and $A$ is an $N$x$N$ matrix with coefficients

$a_{i,j} = \frac{1}{\sqrt{N}} e^{- i \frac{2\pi}{N} ij}$.

For example, where $N=4$s:
$$
    {\bf A} = \frac{1}{\sqrt{4}} \begin{pmatrix}
    1 & 1 & 1 & 1\\
    1 & -i & -1 & i\\
    1 & -1 & 1 & -1\\
    1 & i & -1 & -i
    \end{pmatrix}
$$

## Task

- Type: Implement
- Tasks:
  1. Implement a matrix DFT (of `A` above) from scratch.
     - import: only `numpy`
     - args: only `n` (`n=4` in this example).
  2. Now take your answer to part 1 of this task and modify it to take in a signal `x` of length `n` and return the DFT. 
     - Hint: use x[i]
  3. Finally, write a combined function that computes the DFT, including an internal step for matrix `A`. 
     - Hint: use `np.dot(x, square_dft_matrix(n))`
- Reference implementations:
  1. `fourier.square_dft_matrix()`
  2. `fourier.dft()`
  3. `fourier.dft_at_once()`
