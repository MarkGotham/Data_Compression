## Background

One way to encode colour images is with:
- a rectangular grid of pixels (the more pixels, the more detail)
- 'RGB' values for each pixel, registering the relative strength of red (R), green (G), and blue (B).  


## Task

1. Type: Explore
   - Import an image library and cat picture e.g.,:
     - Import the `scikit-image` library (`import skimage as ski`)
     - Open their stock image of a cat (`cat = ski.data.chelsea()`, `ski.io.imshow(cat)`, `ski.io.show()`)
   - Explore the `shape` of the image (`cat.shape`)
   - Retrieve individual pixels and individual colour (RGB) profiles of each pixel
2. Type: Implement
   - Write a function to modify the colour profile by weighting the R, G, B components of each pixel.

Reference implementations are in the notebook (below), e.g. `modify_colour()`.
