## Background

Cones detect colour in the visible range using three different pigments 
specialising in different wavelengths
called "short", "medium" and "long" (SML),
and corresponding broadly to the colours we know as "red", "green", and "blue" (RGB).

| SML | Full   | Approx. peak ($λ$, nm) | Approx. colour |
|-----|--------|------------------------|----------------|
| S   | Short  | 560                    | Red            |
| L   | Long   | 530                    | Green          |
| M   | Medium | 420                    | Blue           |


## Task

1. Type: Model
    - Task: Plot approximate Gaussian curves for the SML cone cells, with the peak values given and a σ of 20 nm. 
    - Reference implementation: `rgb_theory.plot_resp()`
2. Type: Model data 
   - Task:
     - Retrieve data for RGB sensitivity. For example, the `./linss2_10e_1.csv` file
     provided has cone sensitivity data from [Stockman & Sharpe (2000)](http://cvrl.ucl.ac.uk/cones.htm):
       - Source: Stockman & Sharpe (2000)
         - “Description: 2-deg fundamentals based on the Stiles Burch 10-deg CMFs (adjusted to 2-deg)” 
         - Units: Energy (linear)
         - Stepsize: 1nm 
     - Plot curves for the RGB/SML cone cells from this data 
   - Reference implementation: `rgb_data.plot_rgb_csv()`
