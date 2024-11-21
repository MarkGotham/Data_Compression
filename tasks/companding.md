## Background

Companding is a portmanteau word combining 'compressing' and 'expanding'.
It uses the fact that the ear requires
more precise samples at low amplitudes (soft sounds)
and less at higher amplitudes.


## Linear, then Non-Linear

Analog-to-Digital converters often map a sound sound to encoding linearly.
If an amplitude $a$ is converted to the number $n$,
then amplitude $2a$ will be converted to the number $2n$.

Then the companding part is non-linear,
mapping the sample not only 
- from a larger to a smaller space (fewer bits)
- but doing this reduction in a way that mirrors human perception.


## $\mu$-law

Two main, standarised companding techniques are the **$\mu$-law** and the **$A$-law**.
The rationale is the same: you can afford to accuracy for some signals more than others.
How that accuracy is reduced is slightly different.
Here, we set out the $\mu$-law.

First, the $sgn$ (signum) function maps all positive numbers to 1, all negative to -1 and 0 stays as 0:

$$
{sgn}(x) = {\begin{cases}-1&{\text{if }}x<0,\\0&{\text{if }}x=0,\\1&{\text{if }}x>0.\end{cases}}
$$

Then the $\mu$-law encodes a sample value $x$ as follows::  

$$
F(x) = {sgn}(x){\dfrac {\ln(1+\mu |x|)}{\ln(1+\mu )}},\quad -1\leq x\leq 1
$$


## Task

- Type:
    Implement.
- Task:
  - Implement the $\mu$-law function.
    - Either with $sgn$ separately or within the function
    - Accept as arguments the input and output bit number or max/min of the range.
- Bonus: plot the function and consider the shape in relation to unequal emphasis on high vs low amplitudes.
- Reference implementation:
  - `audio.mu_law_encode`
  - `audio.plot_mu`