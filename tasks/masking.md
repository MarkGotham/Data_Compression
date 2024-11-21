## Background

Beyond the basics, there are some strange properties of auditory perception that are highly relevant to audio data compression.
We can't cover every way of tricking the brain with sound,
but one aspect of this topic we certainly must address is **auditory masking**.
When a person wears a mask, their face cannot be seen.
Auditory masking is an analogy to that for the case of sound: one sound ‘covers’ another so that it cannot be heard.

As with most topics in human perception (auditory or otherwise) we are dealing with a relative rather than absolute effect:
various factors affect whether one sound will mask another completely, partially, or not at all.
Therefore, continuing with the visual analogy, perhaps we should talk not only of 
full masks (whole face) but also 
partial masks (part of the face) and indeed 
veils (full coverage, but partly see-through).

Masking occurs because we have limited resolution in what we can perceive.
This topic of auditory masking extends the discussion of critical bands in
[`bark`](https://github.com/MarkGotham/Data_Compression/blob/main/bark.ipynb).
Put another way,
Bark discussed the basilar membrane's finite frequency resolution,
and masking explores one effect of that.

Are we still talking about data compression here?
Yes!
When a sound is masked, it is not audible and can be removed in a lossy compression algorithm.


## Frequency Masking

Frequency masking is usually discussed in terms of a 
**target signal** (primarily periodic) that we want to hear,
and a **band of noise** (non periodic) that may or not mask the target.
Think of having a conversation in a noisy environment, next to running water, or among many other conversations.

Whether and to what extent the noise will mask the target signal varies as a function of the relative:
1. amplitude. The louder the noise, the more likely it will mask the signal.
2. frequency. Here, we need to know the value (or range for noise) of each in terms of:
   - how close they are to one another. Masking is more likely for closer – especially overlapping – frequencies. 
   - which is higher/lower. Because of asymmetry in the auditory threshold function, the signal is more likely to be masked when it is higher than the noise.

Fletcher (“Auditory Patterns”, Rev. Mod. Phys., 1940)
offered perhaps the first model of absolute hearing threshold according.
This model uses three component functions of frequency ($f$), summed together:

$$
3.64 * ((f / 1000)^{-0.8})
+
-6.5 * (e^{(-0.6 * (f / 1000 - 3.3)^{2})})
+
(10^{-3}) * ((f / 1000)^{4})
$$

## Temporal Masking

Human hearing has a granularity not only in terms of frequency but also temporal sound perception.
We can discriminate between sound events if they are more than c.30 milliseconds apart.
Within that span average the energy during that short time window.
Microphones do not work in that way.
As such, this too is clear area of possible perception-inspired compression.


## Task
 
- Type: Implement
- Task:
    Implement an approximate model of frequency masking using Fletcher's equation.
    - Inputs: a frequency-decibel pair.
    - Return: bool for whether it will be audible (avoid masking).
- Reference implementation: `audio.audible`, `audio.plot_hearing_threshold`.


## Also on this repository

This topic of auditory masking extends the discussion of critical bands in
[`bark`](https://github.com/MarkGotham/Data_Compression/blob/main/bark.ipynb)
and [`explore_noise`](https://github.com/MarkGotham/Data_Compression/blob/main/explore_noise.ipynb)
provides a space for experimenting with sound and noise signals.
