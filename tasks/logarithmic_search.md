## Background

In [`distortion`](https://github.com/MarkGotham/Data_Compression/blob/main/distortion.ipynb)
we met 'block search' where the expectation is that
the closest match for an object within neighbouring frames is
also in (nearly) neighbouring positions.

Logarithmic search considers an alternative,
in which we make no such assumption at the outset
and work in a more 'top down' fashion.
Logarithmic search:
- starts in the middle position
- bisects the available space in each direction
- takes the best match and continues to iterate from there.


## An example of logarithmic search

For example, consider a 17x17 grid where the
best match is to be found at position `(4, 15)`
(but we don't know that in advance).

The search start at the central position,
('X' marks that point: `(8, 8)`)
and we compare that value here with those that bisect the remaining space in each direction:
('?' indicates these positions:
`(12, 8)`, `(4, 8)`,
`(8, 12)`, `(8, 4)`.)

$$
\begin{pmatrix}
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & ? & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & ? & . & . & . & X & . & . & . & ? & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & ? & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
\end{pmatrix}
$$

Seeing that the best result is at `(4, 8)`,
we move to re-center on that position and check: 
`(0, 8)`, `(4, 12)`, `(4, 4)`.
This round could include checking `(8, 8)`, though we've already seen that one,
so don't need to.
Let's mark that with empty parentheses `()`.

$$
\begin{pmatrix}
. & . & . & . & . & . & . & . & ? & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & ? & . & . & . & X & . & . & . & ? & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & () & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
\end{pmatrix}
$$

Now `(4, 12)` is best so we start again there,
still looking 4 steps in each direction: 
`(8, 12)`, `(0, 12)`, 
and `(4, 16)`.
(We've seen `(4, 8)`).

$$
\begin{pmatrix}
. & . & . & . & . & . & . & . & . & . & . & . & ? & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & () & . & . & . & X & . & . & . & ?\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & ? & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
\end{pmatrix}
$$

As `(4, 12)` is still the best fit (unchanged),
we remain at that position and narrow the scope, 
looking not 4 steps in each direction, but 2:
i.e., the positions
`(6, 12)`, `(2, 12)`,
`(4, 14)`, `(4, 10)`.

$$
\begin{pmatrix}
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & ? & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & ? & . & X & . & ? & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & ? & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
\end{pmatrix}
$$

Now `(4, 14)` is the best fit, so we move there
looking 2 steps in each direction.
i.e.,
`(6, 14)`, `(2, 14)`, and `(4, 16)`.
(We've seen `(4, 12)`).

$$
\begin{pmatrix}
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & ? & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & () & . & X & . & ?\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & ? & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
\end{pmatrix}
$$

The position `(4, 14)` is still the best fit,
so we stay there
and reduce the step size one final time to 1 step in each direction.



we continue the process,
starting there, bisecting the space,
(and ignoring positions already checked)

$$
\begin{pmatrix}
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & ? & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & () & X & ? & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & ? & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
\end{pmatrix}
$$

Of these, `(4, 15)` is best, and 
because we've had a round of step size 1,
we can end here and return the result.


## Mathematically formalised

The initial step size is
$s = 2^{\lfloor \log_2 d \rfloor - 1}$.
When we are at position $(a,b)$, with step size $s$,
we compute the values at $(a,b)$ along with
four other points whose position is defined relative to $(a,b)$:
$$
(a+s,b),
(a-s, b),
(a, b+s),
(a, b-s).
$$
There are two possibilities here.
Either:
1. the best match is still $(a,b)$, in which case we
    - we shrink the **search area**: $s \gets s/2$.
    - keep the same **position**.
2. if the best match has moved, 
    - we move **position** to the new best match,
    - keep the **search area** (step size, $s$) unchanged

This process continues until a final round in which $s = 1$.


## Task

- Type: Implement
- Task:
    - Create two a fake 'frame' of zeros and occasional values as above. Implement logarithmic search.
- Reference implementation:
    `video.{make_test_array_log, logarithmic_search}`
