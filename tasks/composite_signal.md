## Background

As discussed, simple sounds are periodic.
The simplest consist of a single periodic sine wave.
This is a synthetic sound: nature is almost more complex.
A first step towards more realistic sounds involves
combining one frequency – the 'fundamental' – with 'partials':
other periodic signals with frequencies at integer multiples of the fundamental.

## Task

- Type: Implement roundtrip.
- Task: Generalise the creation of composite signals as follows:
    - Chose a fundamental frequency e.g., 100Hz 
    - Create a periodic function with that frequency (sin or cos). 
    - Create further periodic functions with integer multiples of this frequency (n) and lower amplitudes, e.g.:
      - for every integer multiple (2, 3, 4, ...)
      - the amplitude is reduced (1/2, 1/3, 1/4, ... )
    - Combine them to make a pseudo-realistic composite waveform.
      - Hint: `Audio({time_array_1} + {time_array_1}, rate=sr)`
    - Plot the composite signal and all components (_time_ against amplitude)
    - Apply DFT to this function 
      - Bonus: Implement DFT from scratch.
    - Plot this DFT (_frequency_ against amplitude)
    - Verify that the DFT returns the same frequency:amplitude pairs that you input.
- Reference implementation: `composite_signal.run()` (and for the bonus DFT from scratch see the `fourier` task).
