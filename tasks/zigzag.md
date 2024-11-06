## Background

JPEG reads values from a matrix in a 'zigzag'
from the 'DC coefficient' (0,0) and continuing as shown below.

$$
\begin{pmatrix}
\rightarrow & \swarrow & \rightarrow & \swarrow & \rightarrow & \swarrow & \rightarrow & \swarrow\\
\downarrow & \nearrow & \swarrow & \nearrow & \swarrow & \nearrow & \swarrow & \downarrow\\
\nearrow & \swarrow &\nearrow & \swarrow & \nearrow & \swarrow & \nearrow & \swarrow\\
\downarrow & \nearrow & \swarrow & \nearrow & \swarrow & \nearrow & \swarrow & \downarrow\\
\nearrow & \swarrow & \nearrow & \swarrow & \nearrow & \swarrow & \nearrow & \swarrow\\
\downarrow & \nearrow & \swarrow & \nearrow & \swarrow & \nearrow & \swarrow & \downarrow\\
\nearrow & \swarrow & \nearrow & \swarrow & \nearrow & \swarrow & \nearrow & \swarrow\\
\rightarrow & \nearrow & \rightarrow & \nearrow & \rightarrow & \nearrow & \rightarrow & .\\
\end{pmatrix}
$$


## Task

- Type: Implement
- Task: Implement the zigzag scan to
  - Map from an $M$ x $N$ matrix into a 'flat' list (or $1$ x $MN$ matrix).
  - Bonus: Write the inverse function mapping from $1$ x $MN$ to $M$ x $N$. 
- Reference implementation: `zigzag.transform` (the same function convert both).
