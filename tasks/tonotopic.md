## Background

When the basilar membrane converts pressure waves into electric signals,
it is effectively ‘reading’ the frequencies of those waves.
Different frequencies register as different positions along the basilar membrane.

More specifically:
- The sound frequency (`f`) is approximately inversely proportional to the log of the length (`x`) along the basilar membrane (total length `L`) as measured from the entrance of the sound into the ear. I.e.,
- higher frequencies correspond to shorter distances (cf. wavelengths) and are detected nearer the base of the membrane (i.e., the ‘start’ as sound travel in from the outer ear)
- likewise, vice versa, lower frequencies are detected further along the membrane, nearer the apex (i.e., the other end, though recall that it wraps around, so ‘further along’ is not quite the same as ‘further in’).

As frequency sensitivity is location-specific on the basilar membrane, it is said to be 'tonotopic'.


## Task

- Type: Implement
- Task: Make a function approximating the relationship between $f$, $x$, and $L$ such that:
  - the total length $L = 30mm$, 
  - linear positive steps in the length ($x$) equate to log descent in ($f$), connecting (0,20000)
  via (10,2000), and (20,200) to (30,20).
- Reference implementation: `tonotopic.plot_tonotopic()`
