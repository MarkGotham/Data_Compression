## Background

First [`composite`](https://github.com/MarkGotham/Data_Compression/blob/main/composite.ipynb)
created a roundtrip with a composite signal and Fourier transform on it.
Then [`masking`](https://github.com/MarkGotham/Data_Compression/blob/main/masking.ipynb)
explored the effect of noise masking a sound in _theory_.
This notebook provides a space for experimenting with combined sound and noise signals in _practice_.


## Task

- Type: Explore/experiment
- Task:
  - Play around with the frequency and amplitude of
    - the periodic signal (and or composite signal),
    - the noise (in which case, by filtering the frequency _range_)
  - Note your limits: when do you stop hearing the signal?
- Bonus tasks:
  - Go to the `masking` functions and see how well they match your experience.
  - Write a function to filter the noise, to clear the noise spectrum around a signal periodicity. 
  - Plot Fourier transforms of the white noise and the filtered noise to compare.
