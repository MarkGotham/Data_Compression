## Background

Audio compression is based on human perception.
Successful compression achieves a good compression ratio
(small file size when compressed)
with the result being hardly noticeably different from the original.
This is achieved by identifying redundancy of the data as defined by how noticeable it is to human listeners.

We start by observing that a healthy human's sound perception is incredible.
We detect a sound pressure variation of only $2 \times 10^{-5}$ Pascals rms.
This is the reference against which sound pressure level (SPL) is measured.
The sensation of loudness increases logarithmically with the SPL and so it is measured in deciBel,
spanning approximately from 0 to 130 dB.

At the quiet end, we can barely hear.
At the loud end there a pain threshold.
It is not, however, equally sensitive across this range.
- the minimum of $2 \times 10^{-5}$ Pascals set as the value of 0dB falls at c.5k Hz.
- the approximate frequency range for high-quality audio is 20 Hz to 20,000 Hz (as discussed)
- there is disproportionate effect of level reduction on the lower, 'bass' end (c.20–200Hz)


## Critical bands

As discussed, we detect sound by vibrations of the membrane in the inner ear.
This membrane is highly - but not infinitely - sensitive.
When one area vibrates at a given frequency, 
so nearby areas are forced to vibrate at the same frequency with an amplitude that decreases with distance.

There is, therefore a finite width to the vibration envelope.
The psychoacoustical term to describe this is **critical bandwidth**.

There are many functions for expressing frequency scale in terms of perceptually equal distances.
I.e., these models attempt to fix equal steps according to what listeners judge to be equal in distance from one another.
[Some are listed here](https://en.wikipedia.org/wiki/Bark_scale)
and a few are implemented in the repo
([`audio.py`](https://github.com/MarkGotham/Data_Compression/blob/main/implementations/audio.py))
(with thanks to A. Lerch as detailed on the repo):
- `audio.<schroeder>`,
- `audio.<terhardt>`,
- `audio.<zwicker>`,
- `audio.<traunmuller>`,

One of the earliest and best known is the so-called 'Bark' scale, named after Heinrich Barkhausen
who pioneered early subjective measurements of loudness.

$$
    1 \text{ Bark} = \begin{cases}
    f/100
    &
    \text{if } f \le 500Hz,
    \\
    9 + 4 \log_2 (f/1000)
    &
    \text{if } f \geq 500Hz
    \end{cases}
$$


$$
    \text{Critical bandwidth} = \begin{cases}
    100
    &
    \text{if } f \le 500Hz,
    \\
    0.2 \times f
    &
    \text{if } f \geq 500Hz
    \end{cases}
$$


## Task

- Type: Implement
- Task:
    Re-create a version of
    [this plot of critical bands from wikimedia](https://commons.wikimedia.org/wiki/File:Bark_scale.png).
    Plot the Bark scale data
    with either or both of:
    - mid-frequency against bandwidth (both Hz)
    - 'Bark' (1–24) against the corresponding frequencies,
        using mid-frequency and 
        using 'error bars' to represent the critical bands
        (given here as 'upper' / 'lower').
- Bonus: add one or more lines of best fit.
- Reference implementation:
    `audio.plot_bark()` for one with 'error bars', or `audio.plot_bark_models()` for several forms.
    Use the data provided in `data/bark.csv` and load it with `audio.bark_data`.


## Also on this repository

- The [`wavelength`](https://github.com/MarkGotham/Data_Compression/blob/main/wavelength.ipynb)
notebook introduces sound in nature;
- Then [`tonotopic`](https://github.com/MarkGotham/Data_Compression/blob/main/tonotopic.ipynb)
takes us into the inner ear,
- Finally, this topic (Bark) begins our account of perception beyond physiology.
