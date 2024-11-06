## Background

The information above concerning basic mathematical operations on matrices
should be enough to take on the tasks below.
These are a bit more involved, and also more relevant to operations we'll use in data compression.

## Task

- Type: Implement

- Tasks: Write functions to ...
  1. Get the `shape` (m- and n-dimensions) of any 1- or 2-D array. 
  2. 'Pad' (expand) an array to double the length and width (4x the size in total) with zeros to the right and below.
  3. Reduce an array to half the length and width (1/4 total), taking the top and left most block.
  4. Implement the dot product above for 2-D arrays from scratch.

- Reference implementations:
  1. `matrix_basics.get_m_n()`
  2. `matrix_basics.pad_2x2()`
  3. `matrix_basics.back_to_half()` (this complements `pad_2x2`)
  4. Locally `matrix_basics.dot_from_scratch()`, as well as in `numpy`:
     - `np.dot(a, b)`, `np.matmul(a, b)` and `a @ b` (where a and b are np.arrays)
     - Bonus: check your work with `np.allclose`.