## Background

JPEG involves converting RGB to YCbCr.
JPEG2000 involves similar colour space transformations called 
reversible component transform (RCT) 
and irreversible component transform (ICT).
Being reversible, RCT is used in lossless compression.
ICT is irreversible and therefore involves lossy compression.
Each transformed component is then compressed separately.

More precisely, given a colour image in three colour components (e.g., RGB)
1. first perform a DC level shifting on each component.
    If the pixel values range in the interval from 0 to $2k −1$, then we subtract $2k −1$ from each pixel value.
2. then transform the resulting three components by either RCT or ICT.


## RCT and ICT

Let $I_0, I_1, I_2$ denote the three colour components of a certain pixel (after DC shifting).
Then the RCT is the triple $(Y_0, Y_1, Y_2)$ given by
$$
\begin{align*}
    Y_0 &= \left\lfloor \frac{I_0 + 2 I_1 + I_2}{4} \right\rfloor,\\
    Y_1 &= I_2 - I_1,\\
    Y_2 &= I_0 - I_1.
\end{align*}
$$

The ICT is given by
$$
\begin{align*}
    Y_0 &= 0.299 I_0 + 0.587 I_1 + 0.144 I_2,\\
    Y_1 &= -0.16875 I_0 - 0.33126 I_1 + 0.5 I_2,\\
    Y_2 &= 0.5 I_0 - 0.41869 I_1 - 0.08131 I_2.
\end{align*}
$$


## Task

- Type: Implementation
- Task:
    Implement the RCT and ICT (ir/reversible component transforms)
    directly from RGB tuples
- Hint: don't forget the DC level shifting on each component first.
- Reference implementations:
    `jpeg2000.rct`,
    `jpeg2000.ict`
