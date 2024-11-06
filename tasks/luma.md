## Background

Much image data is encoded with the ‘RGB colour model’ which measures the presence of the three colours 
red, green and blue (hence RGB) in a light source.

Compression formats like JPEG use 'transform coding'
part of which involves
a 'colour space transformation',
converting images from RGB into a different colour space called $Y'$$C_B$$C_R$. (a.k.a., 'YCbCr').

This has three components:
- The $Y$ component represents the 'brightness' of a pixel
- $C_B$, & $C_R$ represent the 'chrominance' (split into blue and red components).

If $R$, $G$, and $B$, are the red, green and blue signals,
each with a value between 0 and 1, then our the components of our new colour space are defined by

$$
\begin{align*}
    Y' &= K_R R + K_G G + K_B B,\\
    C_B &= \frac {1}{2} \frac {B-Y'}{1-K_B},\\
    C_R &=\frac {1}{2} \frac {R-Y'}{1-K_R},
\end{align*}
$$
where $K_R$, $K_G$, and $K_B$ are constants that satisfy $K_R + K_G +K_B = 1$.
For instance, 
$$
\begin{align*}
    K_R &= 0.299,\\
    K_G &= 0.587,\\
    K_B &=0.114.
\end{align*}
$$

## Task

- Type: Implementation
- Task: Implement $Y'$, $C_B$, \& $C_R$ using the constants given as default arguments.
- Reference implementation:
    `luma.brightness`,
    `luma.c_b`,
    `luma.c_r`
