## Background

There are several approaches to video image comparison and compression.
In [`explore_scene_detect`](https://github.com/MarkGotham/Data_Compression/blob/main/explore_scene_detect.ipynb)
we experimented with off-the-shelf methods for the detection of scene changes.
Scene change detection typically considers whether _all_ pixels are similar:
a large change overall indicates a likely scene change.

Then, in [`distortion`](https://github.com/MarkGotham/Data_Compression/blob/main/distortion.ipynb)
we met 'block search' where the expectation is that:
- most pixels are very similar from one frame to the next,
- there is a change to a part of the image (typically a "subject" in the foreground), 
- the closest match for an object within neighbouring frames is in a nearby positions.

Logarithmic search considers an alternative in which we:
- are still seeking a match, 
- make no such assumption _where_ the match is.

That is, in block search, there's a similar match _nearby_;
in logarithmic search, there's a match _somewhere_ in the frame.
This makes logarithmic search more suitable for larger or more unpredictable motions.

Logarithmic search works in a more 'top down' fashion, it:
- starts in the middle position
- bisects the available space in each direction
- takes the best match and continues to iterate from there.

> **_FAQs and important notes_**
>
> **Assumption:** logarithmic search assumes there is one clear best match.
> If that's not the case (e.g., there are two equally good candidates far apart),
> the algorithm may not perform well.
> 
> **Coordinate convention:** throughout this notebook, positions are given as `(row, col)`, where row 0 is the top of the grid and col 0 is the left.
> I.e., Rows increase from top to bottom, columns increase from left to right.
> 
> **Why "logarithmic"?** The step size halves each time we stay in place, so the number of iterations scales as $O(\log_2 d)$, where $d$ is the grid dimension.


## An example of logarithmic search

For example, consider a 17x17 grid where the
best match is to be found at position `(4, 15)`
(but we don't know that in advance).

**Round 1 — step size 4, centre `(8, 8)`**

The search starts at the central position
('X' marks that point: `(8, 8)`),
and we compare that value with those that bisect the remaining space in each direction
('?' indicates these positions:
`(4, 8)`, `(12, 8)`,
`(8, 4)`, `(8, 12)`).

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

**Summary:**
- Centre `(8,8)`, step 4, candidates `(4,8)`, `(12,8)`, `(8,4)`, `(8,12)`.
- Best: `(4,8)` → move there and keep step size.

---

**Round 2 — step size 4, centre `(4, 8)`**

We re-centre on `(4, 8)` and check:
`(0, 8)`, `(8, 8)`, `(4, 4)`, `(4, 12)`.
We have already evaluated `(8, 8)`, so we skip it
(marked `()` below).

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

**Summary:**
- Centre `(4,8)`, step 4, new candidates `(0,8)`, `(4,4)`, `(4,12)`, skip `(8,8)`.
- Best: `(4,12)` → move there, keep step size.

---

**Round 3 — step size 4, centre `(4, 12)`**

Now `(4, 12)` is best, so we start again there,
still looking 4 steps in each direction:
`(0, 12)`, `(8, 12)`, `(4, 8)`, `(4, 16)`.
We have already seen `(4, 8)`, so we skip it.

$$
\begin{pmatrix}
. & . & . & . & . & . & . & . & . & . & . & . & ? & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & () & . & . & . & . & . & . & . & X & . & . & . & ?\\
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

**Summary:**
- Centre `(4,12)`, step 4, new candidates `(0,12)`, `(8,12)`, `(4,16)`, skip `(4,8)`.
- Best: still `(4,12)` → stay there and halve step size to 2.

---

**Round 4 — step size 2, centre `(4, 12)`**

As `(4, 12)` is still the best fit (unchanged),
we remain at that position and narrow the scope,
looking not 4 steps in each direction, but 2:
i.e., `(2, 12)`, `(6, 12)`, `(4, 10)`, `(4, 14)`.

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

**Summary:**
- Centre `(4,12)`, step 2, candidates `(2,12)`, `(6,12)`, `(4,10)`, `(4,14)`.
- Best: `(4,14)` → move there, keep step size 2.

---

**Round 5 — step size 2, centre `(4, 14)`**

Now `(4, 14)` is the best fit, so we move there,
looking 2 steps in each direction:
`(2, 14)`, `(6, 14)`, `(4, 12)`, `(4, 16)`.
We have already seen `(4, 12)`.

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

**Summary:**
- Centre `(4,14)`, step 2, new candidates `(2,14)`, `(6,14)`, `(4,16)`, skip `(4,12)`.
- Best: still `(4,14)` → stay there an halve step size to 1.

---

**Round 6 — step size 1, centre `(4, 14)`**

We reduce the step size one final time to 1 and check:
`(3, 14)`, `(5, 14)`, `(4, 13)`, `(4, 15)`.
All four are new.

$$
\begin{pmatrix}
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & . & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & . & ? & . & .\\
. & . & . & . & . & . & . & . & . & . & . & . & . & ? & X & ? & .\\
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

**Summary:**
- Centre (4,14), step 1, candidates (3,14), (5,14), (4,13), (4,15).
- Best: (4,15).
- Because we've completed a round with step size 1,
we stop here and return `(4, 15)` as the final answer.

---

## Mathematically formalised

Let $d$ be the side length of the search grid minus 1 (e.g., $d = 16$ for a 17×17 grid).
The initial step size is:
$$s = 2^{\lfloor \log_2 d \rfloor - 1}$$

For our 17×17 example: $\lfloor \log_2 16 \rfloor - 1 = 3$, so $s = 2^3 / 2 = 4$.

When we are at position $(a, b)$ with step size $s$,
we compute the match quality at $(a, b)$ along with four candidate positions:
$$
(a+s,\, b),\quad
(a-s,\, b),\quad
(a,\, b+s),\quad
(a,\, b-s).
$$
Candidates that fall outside the grid boundaries are clamped to the nearest valid index.
Candidates already evaluated in a previous round are skipped.

There are two possibilities:

1. **The best match is still $(a, b)$** (no improvement): 
    - halve the step size: $s \gets s/2$,
    - keep the same position.
2. **The best match has moved** to a new position $(a', b')$:
    - move to $(a', b')$,
    - keep the step size $s$ unchanged.

This process continues until the completion of a round in which $s = 1$, at which point the current best position is returned.


## Task

- Type: Implement
- Task:
    - Create a fake 'frame' of zeros with occasional non-zero values as above.
    - Implement logarithmic search.
- Reference implementation:
    `video.{make_test_array_log, logarithmic_search}`
