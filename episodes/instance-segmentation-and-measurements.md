---
title: 'Instance Segmentation and Measurements'
teaching: 30
exercises: 10
---

:::::::::::::::::::::::::::::::::::::: questions 

- How do we perform instance segmentation in Napari?
- How do we measure cell size with Napari?
- How do we save our work to create re-usable work flows.

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Perform a workflow to create an instance segmentation.

- Use python to measure the cell sizes.

::::::::::::::::::::::::::::::::::::::::::::::::

In this lesson we'll continue to work with the Cells (3D + 2Ch) image we've
been using in past lessons. We will use Napari's Python console 
to perform our workflow. At the end of the lesson we will save our console
session to a Python script that we can then re-use to easily repeat our
workflow on new images.

The first steps assume you are starting a new session, if you have come 
straight from the last lesson and already have a binary mask image you 
can skip them.

First, let's open one of Napari's sample images with:

`File > Open Sample > napari builtins > Cells (3D + 2Ch)`

Open Napari's console by pressing the ![](
https://raw.githubusercontent.com/napari/napari/main/napari/resources/icons/console.svg
){alt="A screenshot of Napari's console button" height='30px'} button, 
then copy and paste the code below.

```python
from skimage.filters import threshold_otsu, gaussian

image = viewer.layers["nuclei"].data

blurred = gaussian(image, sigma=3)
threshold = threshold_otsu(blurred)

semantic_seg = blurred > threshold
viewer.add_labels(semantic_seg)
```
![](fig/semantic-seg-napari.png){alt="A screenshot of a rough semantic
segmentation of nuclei in Napari"}

And you should see the image above. You are now ready to begin this lesson.

## Our first measurement

We now have a binary image with each pixel classified as either cell nuclei
(True) or not (False). Try running the following code in the console.
 
```python
# We're going to need some functions from the Numpy library.
import numpy as np

# How many pixels are there in total in the image?
total_pixels = semantic_seg.size

# How many pixels are labelled as cell nuclei?
# We'll use Numpy's count_nonzero method.
nuclei_pixels = np.count_nonzero(semantic_seg)

# Now we can work out what percentage of the image is cell nuclei
nuclei_percent = nuclei_pixels / total_pixels * 100

# And write the results to the console with some formatting. 
# The ":2f" part tells Python to only print 2 decimal points.

print (f"Percent Nuclei = {nuclei_percent:.2f}%")

```

```output
Percent Nuclei = 19.47%
```

Is know the percentage of pixels that are classed as nuclei sufficient 
for our purposes? Thinking back to some of the research questions 
we discussed in the [episode on designing an experiment](
designing-a-light-microscopy-experiment.md#define-your-research-question)

from skimage.filters import threshold_otsu, gaussian
from skimage.morphology import binary_erosion, ball
from skimage.segmentation import expand_labels
from skimage.measure import label

image = viewer.layers["nuclei"].data

blurred = gaussian(image, sigma=3)
threshold = threshold_otsu(blurred)
semantic_seg = blurred > threshold

viewer.add_labels(semantic_seg)

eroded = binary_erosion(semantic_seg, footprint=ball(10))
instance_seg = label(eroded)
instance_seg = expand_labels(instance_seg, distance=10)

viewer.add_labels(instance_seg)

#we only want to measure whole nuclei. 
tools > segmentation post processing > remove 

pixels = []
for cell in range (final_image.max() + 1):
    ...:     pixels.append(np.count_nonzero(final_image == cell))

np_pix = np.array(pixels)

#total cells = 60 * 256 * 256
np_pix.sum()

#average cell size
np_pix[1:].mean()
#std deviation of cell size
np_pix[1:].std()
max() min () etc.

How would you measure distances. You'd have to fit an ellipse or similar.

can do marching cubes, then if so desired you could find the maximum distance between two points in the mesh:
vertices, faces, normals, value = marching_cubes(final_image, level = 10)

viewer.add_surface((vertices, faces, value))
%save current_session ~0/

then 
execfile('current_session.py')
load current_session.py seems nicer

::::::::::::::::::::::::::::::::::::: keypoints 

- Using Napari's Python console we can access a large library of image processing functions.

- We can use Python's help function to get information on what each function does.

- We can assemble these functions into our own custom function to automate image analysis tasks.

::::::::::::::::::::::::::::::::::::::::::::::::

