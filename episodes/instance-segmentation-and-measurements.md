---
title: 'Instance Segmentation and Measurements'
teaching: 30
exercises: 10
---

:::::::::::::::::::::::::::::::::::::: questions 

- How do we automate instance segmentation in Napari?
- How do we use the results of instance segmentation to automate measurements.

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Write a Python function to automate instance segmentation for a sample image.

- Write a Python function to automate cell measurement for a sample image.

- Apply scripts to a sample image to generate a cell count.

::::::::::::::::::::::::::::::::::::::::::::::::


```python
from skimage.filters import threshold_otsu, gaussian
from skimage.morphology import binary_erosion, ball
from skimage.segmentation import expand_labels
from skimage.measure import label

image = viewer.layers["nuclei"].data

def binary_mask(image):
  blurred = gaussian(image, sigma=3)
  threshold = threshold_otsu(blurred)

  semantic_seg = blurred > threshold
  return semantic_seg

def instance_segmentation(image):
  """
  Creates an instance segmentation of a binary image.
  """
  eroded = binary_erosion(semantic_seg, footprint=ball(10))
  instance_seg = label(eroded)
  instance_seg = expand_labels(instance_seg, distance=10)
  return instance_seg

viewer.add_labels(instance_seg)
```

::::::::::::::::::::::::::::::::::::: keypoints 

- Using Napari's Python console we can access a large library of image processing functions.

- We can use Python's help function to get information on what each function does.

- We can assemble these functions into our own custom function to automate image analysis tasks.

::::::::::::::::::::::::::::::::::::::::::::::::

