## Background

Probably the simplest type of Wavelet is the co-called 'Haar'.
Unlike most, this is not a continuous function as the value is either 0, 1 or -1.
The Haar mother wavelet is as follows:

$$
    \psi(t) = \begin{cases}
    1 & \text{if} 0 \le t < 1/2,\\
    -1 & \text{if} 1/2 \le t < 1,\\
    0 & \text{otherwise.}
    \end{cases}
$$

... and the scaling function needed to handle the DC term is
$$
    \phi(t) = \begin{cases}
    1 & \text{if} 0 \le t < 1,\\
    0 & \text{otherwise}
    \end{cases}
$$

## Discretizing Haar

We can discretize Haar broadly as follows.
Let $N = 2^n$, then the Haar matrix ${\bf H}_N$ is defined recursively.

$$
    {\bf H}_2 = \frac{1}{\sqrt{2}} \begin{pmatrix}
    1 & 1\\
    1 & -1
    \end{pmatrix}.
$$

Then
$$
    {\bf H}_{2N} = \frac{1}{\sqrt{2}} \begin{pmatrix}
    {\bf H}_N  \otimes (1,1)\\
    {\bf I}_N \otimes (1,-1)
    \end{pmatrix},
$$
where ${\bf I}_N$ is the identity matrix and $\otimes$ denotes the
[Kronecker product](https://en.wikipedia.org/wiki/Kronecker_product).

This results in
$$
\begin{align*}
    {\bf H}_4 &= \frac{1}{ \sqrt{4} } \begin{pmatrix}
    1           & 1         & 1         & 1\\
    1           & 1         & -1        & -1\\
    \sqrt{2}    & -\sqrt{2} & 0         & 0\\
    0           & 0         & \sqrt{2}  & -\sqrt{2}
    \end{pmatrix}\\
\end{align*} 
$$

and

$$
\begin{align*}
    {\bf H}_8 &= \frac{1}{ \sqrt{8} } \begin{pmatrix}
    1           & 1         & 1         & 1         & 1         & 1         & 1         & 1\\
    1           & 1         & 1         & 1         & -1        & -1        & -1        & -1\\
    \sqrt{2}    & \sqrt{2}  & -\sqrt{2} & -\sqrt{2} & 0         & 0         & 0         & 0\\
    0           & 0         & 0         & 0         & \sqrt{2}  & \sqrt{2}  & -\sqrt{2} & -\sqrt{2}\\
    2           & -2        & 0         & 0         & 0         & 0         & 0         &  0\\
    0           & 0         & 2         & -2        & 0         & 0         & 0         &  0\\
    0           & 0         & 0         & 0         & 2         & -2        & 0         &  0\\
    0           & 0         & 0         & 0         & 0         & 0         & 2         &  -2
    \end{pmatrix}.
\end{align*}
$$

## Haar matrix decomposition

The Haar matrix can be decomposed by computing averages and differences.
For all $N$ powers of $2$, let
$$
    \Delta_N = \frac{1}{\sqrt{2}} \begin{pmatrix}
    1 & 1 & 0 & 0 & \dots & 0 & 0\\ 
    0 & 0 & 1 & 1 & \dots & 0 & 0\\
    \vdots & \ddots & \dots & \dots & \dots & 1 & 1\\
    1 & -1 & 0 & 0 & \dots & 0 & 0\\ 
    0 & 0 & 1 & -1 & \dots & 0 & 0\\
    \vdots & \ddots & \dots & \dots & \dots & 1 & -1
    \end{pmatrix},
$$
so that
$$
\begin{align*}
    \Delta_2 &= \frac{1}{\sqrt{2}} \begin{pmatrix}
    1 & 1\\
    1 & -1
    \end{pmatrix},\\
    \Delta_4 &= \frac{1}{\sqrt{2}} \begin{pmatrix}
    1 & 1 & 0 & 0\\
    0 & 0 & 1 & 1\\
    1 & -1 & 0 & 0\\
    0 & 0 & 1 & -1
    \end{pmatrix},\\
    \Delta_8 &= \frac{1}{\sqrt{2}} \begin{pmatrix}
    1 & 1 & 0 & 0 & 0 & 0 & 0 & 0\\
    0 & 0 & 1 & 1 & 0 & 0 & 0 & 0\\
    0 & 0 & 0 & 0 & 1 & 1 & 0 & 0\\
    0 & 0 & 0 & 0 & 0 & 0 & 1 & 1\\
    1 & -1 & 0 & 0 & 0 & 0 & 0 & 0\\
    0 & 0 & 1 & -1 & 0 & 0 & 0 & 0\\
    0 & 0 & 0 & 0 & 1 & -1 & 0 & 0\\
    0 & 0 & 0 & 0 & 0 & 0 & 1 & -1
    \end{pmatrix}.
\end{align*}
$$

With this we can decompose any Haar matrix.
For exmaple, ${\bf H}_8$ decomposes as follows:

$$
\begin{align*}
    {\bf H}_8 &= \left(\begin{array}{c|c}
    \Delta_2 & {\bf 0}\\
    \hline
    {\bf 0} & {\bf I}_6
    \end{array} \right)
    \left(\begin{array}{c|c}
    \Delta_4 & {\bf 0}\\
    \hline
    {\bf 0} & {\bf I}_4
    \end{array} \right)
    \left(\begin{array}{c|c}
    {\Delta_8}
    \end{array} \right)\\
    {\bf H}_8 &=
        \left( \begin{array}{cc|cccccc}
    c & c & 0 & 0 & 0 & 0 & 0 & 0\\
    c & -c & 0 & 0 & 0 & 0 & 0 & 0\\
    \hline
    0 & 0 & 1 & 0 & 0 & 0 & 0 & 0\\
    0 & 0 & 0 & 1 & 0 & 0 & 0 & 0\\
    0 & 0 & 0 & 0 & 1 & 0 & 0 & 0\\
    0 & 0 & 0 & 0 & 0 & 1 & 0 & 0\\
    0 & 0 & 0 & 0 & 0 & 0 & 1 & 0\\
    0 & 0 & 0 & 0 & 0 & 0 & 0 & 1
    \end{array} \right)
    \left( \begin{array}{cccc|cccc}
    b & b & 0 & 0 & 0 & 0 & 0 & 0\\
    0 & 0 & b & b & 0 & 0 & 0 & 0\\
    b & -b & 0 & 0 & 0 & 0 & 0 & 0\\
    0 & 0 & b & -b & 0 & 0 & 0 & 0\\
    \hline
    0 & 0 & 0 & 0 & 1 & 0 & 0 & 0\\
    0 & 0 & 0 & 0 & 0 & 1 & 0 & 0\\
    0 & 0 & 0 & 0 & 0 & 0 & 1 & 0\\
    0 & 0 & 0 & 0 & 0 & 0 & 0 & 1
    \end{array} \right)
    \left( \begin{array}{cccccccc}
    a & a & 0 & 0 & 0 & 0 & 0 & 0\\
    0 & 0 & a & a & 0 & 0 & 0 & 0\\
    0 & 0 & 0 & 0 & a & a & 0 & 0\\
    0 & 0 & 0 & 0 & 0 & 0 & a & a\\
    a & -a & 0 & 0 & 0 & 0 & 0 & 0\\
    0 & 0 & a & -a & 0 & 0 & 0 & 0\\
    0 & 0 & 0 & 0 & a & -a & 0 & 0\\
    0 & 0 & 0 & 0 & 0 & 0 & a & -a
    \end{array} \right),
\end{align*}
$$
where $a = b = c = \frac{1}{\sqrt{2}}$.

Let these three constituent matrices be ${\bf C}$, ${\bf B}$, and ${\bf A}$.
The product should be read from right to left: ${\bf H}_8 = {\bf C}{\bf B}{\bf A}$:
1. First, ${\bf A}$ computes the four averages of adjacent points, and keeps their differences in order to remain reversible.
2. Second, ${\bf B}$ does the same as ${\bf A}$, but only for the four averages (leaving the differences untouched), thus creating two more differences.
3. Finally, ${\bf C}$ computes the average of the remaining two averages, to get one final average and seven other differences.


## Task

- Type: Implementation
- Task:
    Implement the examples above for ${\bf H}_2$ and ${\bf H}_8$.
    Create the identity matrix (${\bf I}_N$) for scratch.
    and use `np.kron` for the Kronecker product ($\otimes$).
- Reference implementation: `haar.h_2`, `haar.h_8` etc.