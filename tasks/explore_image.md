## Background

There are many relevant python libraries for our purposes.

In later notebooks, we'll use `scikit-image`
- [Docs](https://scikit-image.org/)
- [Source code](https://github.com/scikit-image/scikit-image)
  - e.g., the function that sets RGB weightings in the source code is [here ('rgb2gray')](https://github.com/scikit-image/scikit-image/blob/v0.22.0/skimage/color/colorconv.py#L912-L955)
- Note:
  - Install: `scikit-image`
  - Import: `import skimage`

Some alternatives include ...
- `pillow` ('general image processing tool')
  - [Docs](https://pillow.readthedocs.io/en/)
  - [Source](https://github.com/python-pillow/Pillow/)
  - Note:
    - This is a fork (and extension) of "PIL": the Python Imaging Library.
    - The [functionality for jpeg-2000 here](https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#jpeg-2000).
- `glymur` (specifically for JPEG2000)
  - [Docs](https://glymur.readthedocs.io/en/latest/how_do_i.html)
  - [Source code](https://github.com/quintusdias/glymur)
- `Opencv` 
  - [Docs](https://docs.opencv.org/4.x/index.html)
  - [Source code](https://github.com/opencv/opencv)
  - Note:
    - Also for video.
    - Install: `pip3 install opencv-python`
    - Import: `import cv2` 


 ## Task

- Type: Explore
- Task: Import and explore `scikit-image` and/or another one of above libraries for handling images.
