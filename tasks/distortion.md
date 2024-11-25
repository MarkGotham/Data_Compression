## Background

Video compression is based on two kinds of redundancy:
- Spatial redundancy: Each frame (effectively an image) features 'redundancy' in pixel correlation.
    (each pixel is likely to be similar to its immediate neighbours).
- Temporal redundancy:
    Most frames in a video are likely to be very similar to its immediate neighbour (predecessor and successor).

A typical technique for video compression involves:
- encoding the first frame using a still image compression method.
- encodes several successive frames in terms of their difference from the frame before.


## Motion Compensation

Not only are successive frames generally similar,
but more specifically, it is common for a part (or 'block') in one frame 
to move to a different location in the next frame,
e.g., an object moving against a static background.
This can be expressed in terms of the 'block's
- previous location,
- current location
- boundaries (size)

Motion compensation is:
- effective if objects are just translated (moved up/down and side/side)
- not so effective if objects are scaled (made bigger/smaller) or rotated.


## Example

Here's an 8x8 matrix, that's mostly 0s, apart from a few 1s:
$$
\begin{pmatrix}
0 & 0 & 0 & 0 & 0 & 0 & 0 & 0\\
0 & 1 & 1 & 1 & 0 & 0 & 0 & 0\\
0 & 1 & 0 & 1 & 0 & 0 & 0 & 0\\
0 & 1 & 1 & 1 & 0 & 0 & 0 & 0\\
0 & 0 & 0 & 0 & 0 & 0 & 0 & 0\\
0 & 0 & 0 & 0 & 0 & 0 & 0 & 0\\
0 & 0 & 0 & 0 & 0 & 0 & 0 & 0\\
0 & 0 & 0 & 0 & 0 & 0 & 0 & 0\\
\end{pmatrix}
$$


And here's the same 8x8 grid, and the same 'figure', shifted:
$$
\begin{pmatrix}
0 & 1 & 1 & 1 & 0 & 0 & 0 & 0\\
0 & 1 & 0 & 1 & 0 & 0 & 0 & 0\\
0 & 1 & 1 & 1 & 0 & 0 & 0 & 0\\
0 & 0 & 0 & 0 & 0 & 0 & 0 & 0\\
0 & 0 & 0 & 0 & 0 & 0 & 0 & 0\\
0 & 0 & 0 & 0 & 0 & 0 & 0 & 0\\
0 & 0 & 0 & 0 & 0 & 0 & 0 & 0\\
0 & 0 & 0 & 0 & 0 & 0 & 0 & 0\\
\end{pmatrix}
$$

Finally, this is the motion from the first state to the second that we're trying to capture: 
$$
\begin{pmatrix}
0 & 0 & 0 & 0 & 0 & 0 & 0 &0\\
0 & \uparrow & \uparrow & \uparrow & 0 & 0 & 0 & 0\\
0 & \uparrow  & \uparrow & \uparrow & 0 & 0 & 0 & 0\\
0 & \uparrow & \uparrow & \uparrow & 0 & 0 & 0 & 0\\
0 & 0 & 0 & 0 & 0 & 0 & 0 &0\\
0 & 0 & 0 & 0 & 0 & 0 & 0 &0\\
0 & 0 & 0 & 0 & 0 & 0 & 0 &0\\
0 & 0 & 0 & 0 & 0 & 0 & 0 &0\\
\end{pmatrix}
$$


## Measuring Change

In principle, the block that we're tracking can have any shape.
In practice, we tend to limit search to equal size square blocks.
The encoder scans the current frame block by block.
For each block $B$ it searches the neighbouring frame for a similar block $C$.
Finding such a block, the encoder writes the difference between its past and present locations on the output.
This difference is of the form
$$
    (C_x - B_x, C_y - By) = ( \Delta_x, \Delta_y),
$$
so it is called a _motion vector_. 


## Block Search

The search for matching elements is normally restricted to
a small area (called the _search area_) around the references block $B$.
The size of the search is defined by the maximum displacement parameters $dx$ and $dy$.
These parameters specify the maximum horizontal and vertical distances, in pixels,
between $B$ and any matching block in the previous frame.
If $B$ is a square with side $b$, the search area will contain $(b + 2dx)(b + 2dy)$ pixels
and will consist of $(2dx+1)(2dy +1)$ distinct, overlapping $b \times b$ squares.
The number of candidate blocks in this area is therefore proportional to $dxdy$.

## Distortion measure

The distortion measure selects the best match for block $B$ in the neighbouring frame.
The difference can be measures in several ways including the following.

The **Mean absolute error** (or 'mean absolute difference') calculates the 
average of the absolute differences between a pixel $B_{i,j}$ in $B$ and its counterpart $C_{i,j}$ in block $C$:
$$
    \frac{1}{b^2} \sum_{i=1}^b \sum_{j=1}^b \left| B_{i,j} - C_{i,j}  \right|.
$$
This measure is calculated for each of the $(2dx+1)(2dy +1)$ distinct, overlapping
$b \times b$ candidate blocks, and the smallest distortion (say, for block $\hat{C}$) is examined.
If it is smaller than the _search threshold_,
then $\hat{C}$ is selected as the match for $B$.
Otherwise, there is no match for $B$, and $B$ has to be encoded without motion compensation.

The **mean square difference** is similar:
$$
    \frac{1}{b^2} \sum_{i=1}^b \sum_{j=1}^b ( B_{i,j} - C_{i,j}  )^2.
$$

Finally, the **pel difference classification** (PDC) counts how many differences
$|B_{i,j} - C_{i,j}|$ are below a given PDC parameter $p$.


## Task

- Type: Implement
- Task:
    - Create two fake 'frames'
        (arrays of the same shape)
        and chose values of
        $B$ (position), 
        $b$ (size),
        and the maximum displacement parameters
        $dx$ and $dy$.
    - Implement a function returning each of the distinct,
        overlapping blocks for comparison and 
        confirm that there are $(2dx+1)(2dy +1)$ in total.
    - Implement
        'mean absolute difference' and
        'mean square difference' distortion measures.
    - See which of these blocks the
        distortion measures return as most similar
        (and whether they agree).
- Reference implementation:
    `video.{mean_abs_diff},{mean_sq_diff},{block_search}`
