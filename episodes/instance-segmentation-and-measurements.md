---
title: 'Instance segmentation and measurements'
teaching: 30
exercises: 10
---

:::::::::::::::::::::::::::::::::::::: questions

- How do we perform instance segmentation in Napari?
- How do we measure cell size with Napari?
- How do we save our work to create re-usable workflows?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Use simple morphological operations to clean up a segmentation.

- Use connected components labelling on a thresholded image.

- Calculate the number of cells and average cell size.

- Save and edit your workflow to re-use on subsequent images.

- Perform more complex cell shape analysis using the regionprops plugin.

::::::::::::::::::::::::::::::::::::::::::::::::

In this lesson we'll continue to work with the Cells (3D + 2Ch) image we've
been using in past lessons. We will use Napari's Python console
to perform our workflow. At the end of the lesson we will save our console
session to a Python script that we can then re-use to easily repeat our
workflow on new images.

The first steps assume you are starting a new session, if you have come
straight from the last lesson and already have a mask image you
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

We now have a mask image with each pixel classified as either cell nuclei
(pixel value 1) or not (pixel value 0). Try running the following code in
the console.

```python
# We're going to need some functions from the Numpy library.
import numpy as np

# How many pixels are there in total in the image?
total_pixels = semantic_seg.size

# How many pixels are labelled as cell nuclei (pixel value = 1)?
# We'll use Numpy's count_nonzero method.
nuclei_pixels = np.count_nonzero(semantic_seg)

# Now we can work out what percentage of the image is cell nuclei
nuclei_percent = nuclei_pixels / total_pixels * 100

# And write the results to the console with some formatting.
# The ":2f" part tells Python to only print 2 decimal points.

print(f"Percent Nuclei = {nuclei_percent:.2f}%")

```

```output
Percent Nuclei = 19.47%
```

Is knowing the percentage of pixels that are classed as nuclei sufficient
for our purposes? Thinking back to some of the research questions
we discussed in the [episode on designing an experiment](
designing-a-light-microscopy-experiment.md#define-your-research-question)
, if the percentage changes over time we can infer that something is
happening but what? We can't say whether the nuclei are changing in
number or in size or shape. For most research questions we will need a more
informative measurement.

:::::::::::::::::::::::: callout

### Saving and repeating your work

Let's assume that measuring percentage of nuclei is sufficient for your
research question. How do we automate and repeat this workflow on new
images. The Napari Python console has a built in save function.
```python
# Save current session to a file called measure_percent.py
%save measure_percent ~0/
```
Delete the semantic_seg layer from the viewer and run:
```python
load measure_percent.py
```
After pressing enter you should see the calculated percent nuclei and
the semantic_seg layer should reappear. We will reuse the save function
at the end of this lesson.
::::::::::::::::::::::::

## Counting the Nuclei

We now need to count the number of nuclei in the image. We can use the
the [label](
https://scikit-image.org/docs/stable/api/skimage.measure.html#skimage.measure.label)
function from scikit-image. The label function will go through the image
and assign each connected region a unique integer value. Let's try it.

```python
# Import the label function
from skimage.measure import label

# Run the label function on the mask image
instance_seg = label(semantic_seg)

# Add the result to the viewer
viewer.add_labels(instance_seg)
```
![](fig/instance_segmentation_wrong.png){
alt="A screenshot of an instance segmentation of nuclei with some
incorrectly joined instances."}
You should see the above image in the Napari viewer. The different colours
are used to represent different nuclei. The instance segmentation assigns
a different integer value to each nucleus, so counting the number of
nuclei can be done very easily by taking the maximum value of the instance
segmentation image.

```python

# Calculate number of nuclei from instance segmentation
print(f"Number of Nuclei = {instance_seg.max()}")
```
```output
Number of Nuclei = 18
```

We can reuse Numpy's `count_nonzero` function on an individual nucleus by
specifying an integer value between 1 and 18

```python
# How many pixels are there in nucleus 1
nucleus_id = 1
print(f"There are {np.count_nonzero(instance_seg == nucleus_id)}",
      f" pixels in nucleus {nucleus_id}")
```

```output
There are 43945  pixels in nucleus 1
```

More usefully we can can count the number of pixels in each of the nuclei
and add them to a python list.

```python
# Create an empty list
nucleus_pixels = []
number_of_nuclei = instance_seg.max()
# Go through each nucleus,
for nucleus_id in range(1, number_of_nuclei + 1):
  # And append the number of pixels to the list
  nucleus_pixels.append(np.count_nonzero(instance_seg == nucleus_id))
print(nucleus_pixels)
```
```output
[43945, 27187, 202258, 47652, 54018, 113935, 79226, 102444, 34421, 35227, 14525, 3258, 2000, 240, 155, 4709, 522, 7]
```
Knowing the size of each nucleus in pixels is of limited value. We should be
measuring in physical units, to do that we need to know the pixel size.
In the lesson on [filetypes and metadata](
filetypes-and-metadata.md#pixel-size) we learnt how to inspect the image
metadata to determine the pixel size. Unfortunately the sample image
we're using in this lesson has no metadata, so for the purposes of
demonstration we'll assume a pixel size of 0.20&mu;m (x axis),  0.20&mu;m
(y axis) and 0.35&mu;m (z axis). We can then convert pixel size to
physical size.

```python
# Let's keep everything in micrometres
pixel_size = 0.2 * 0.2 * 0.35

# We can mutliply all nuclei by the pixel size by first converting the
# nucleus_pixels to a numpy array.
nucleus_um = pixel_size * np.array(nucleus_pixels)

```

We can then do some statistical analysis.

```python
# Use Numpy's peak to peak function (ptp) to find the range.
print(f"Range of Nucleus sizes = {np.ptp(nucleus_um)} cubic micrometres.")

# Find the mean nucleus size
print(f"Nucleus size mean = {np.mean(nucleus_um):.2f} cubic micrometres.")

# And the standard deviation
print(f"Nucleus size standard dev. = {np.std(nucleus_um):.2f} cubic micrometres.")
```
```output
Range of Nucleus sizes = 2831.51 cubic micrometres.
Nucleus size mean = 595.57 cubic micrometres.
Nucleus size standard dev. = 727.61 cubic micrometres.
```

Do these numbers reflect what we can see in the original images? Whilst
there is visible variation in the size of the nuclei, it is not of the
scale implied by these numbers. The fact that the standard deviation is
larger than the mean value suggests an extreme variation in the
nuclei size that is not apparent in the images. There are two reasons
for this, firstly the labelling has not correctly identified each separate
every nucleus, and secondly we haven't treated nuclei at the edge of the
image correctly.

Looking at the labelling problem first, there are several instances of
nuclei that look separate being labelled as a single nucleus. Referring
 to the image of instance segmentation above, we can see that the 4 nuclei
at the bottom left have all been given a single label (light purple).
Three of them are visibly touching, so it is not surprising that they have been labelled as a single nucleus.
What about the fourth apparently separate nucleus? We should remind ourselves
that this a 3 dimensional image.

You may remember from our [first lesson](imaging-software.md#d3d) that
we can change to 3D view mode by pressing the ![](
https://raw.githubusercontent.com/napari/napari/main/napari/resources/icons/2D.svg
){alt="Napari's 2D/3D toggle" height='30px'} button.
Try it now.

![](fig/instance_segmentation_wrong3d.png){
alt="A screenshot of an instance segmentation of nuclei in 3D mode with some
incorrectly joined instances."}
You should see the image rendered in 3D, with a clear join between the
upper most light purple nucleus and its neighbour. So now we understand why the
instance labelling has failed, what can we do to fix it?

::::::::::::::::::::::::: challenge

### Erode the semantic segmentation so all nuclei are separate
In order to use the label function to count the cell nuclei we first need
to make sure all the nuclei are separate. We can do this by reducing the
apparent size of the nuclei by eroding the image. scikit-image's
[binary_erosion](
https://scikit-image.org/docs/stable/api/skimage.morphology.html#skimage.morphology.binary_erosion)
function is a good tool to do this. The function sets a pixel to the
minimum value in the neighbourhood defined by a 'footprint' parameter.
We'll use scikit-image's [ball](
https://scikit-image.org/docs/stable/api/skimage.morphology.html#skimage.morphology.ball)
function to generate a sphere to use as the footprint. We can change
the radius of the footprint to control the amount of erosion. Try eroding
the `semantic_seg` layer with different integer values for the radius.
What radius do you need to ensure all nuclei are separate?

```python
from skimage.morphology import binary_erosion, ball

# With radius = 1
radius = 1
eroded_mask = binary_erosion(semantic_seg, footprint = ball(radius))
viewer.add_labels(eroded_mask, name = f'eroded ball {radius}')
```

:::::::::::::::::::::::::solution

```python
# We can use a for loop to test many values of radius. This will test all
# integers from 1 to 10
for radius in range(1,11):
  eroded_mask = binary_erosion(semantic_seg, footprint = ball(radius = 1))
  viewer.add_labels(eroded_mask, name = f'eroded ball {radius}')

```

![](fig/binary_mask_no_erosion.png){
alt="A screenshot of a semantic segmentation mask before erosion."}
The first image shows the mask without any erosion for comparison.

![](fig/binary_mask_erosion_1.png){
alt="A screenshot of a semantic segmentation mask eroded with a ball of
radius 1."}
Erosion with a radius of 1 makes a small difference, but the nuclei remain
joined.

![](fig/binary_mask_erosion_5.png){
alt="A screenshot of a semantic segmentation mask eroded with a ball of
radius 5."}
Erosion with a radius of 5 makes a more noticeable difference,
but some nuclei remain joined.

![](fig/binary_mask_erosion_10.png){
alt="A screenshot of a semantic segmentation mask eroded with a ball of
radius 10."}
Erosion with a radius of 10 separates all nuclei.


:::::::::::::::::::::::::
:::::::::::::::::::::::::

Now we have separate nuclei, lets try creating instance labels
again.

```python
eroded_semantic_seg = viewer.layers['eroded ball 10'].data

instance_seg = label(eroded_semantic_seg)

viewer.add_labels(instance_seg)

print(f"Number of Nuclei after erosion  = {instance_seg.max()}")
```

```outout
Number of Nuclei after erosion  = 19
```

![](fig/instance_segmentation_eroded.png){
alt="Instance segmentation on the eroded segmentation mask"}
Looking at the image above, there are no longer any incorrectly joined
nuclei. The absolute number of nuclei found hasn't changed much as the
erosion process has removed some partial nuclei around the edges of the
image.

Performing any size or shape analysis on these nuclei will be flawed, as
they are heavily eroded. We can largely undo much of the erosion by using
the scikit-images [expand labels](
https://scikit-image.org/docs/stable/api/skimage.segmentation.html#skimage.segmentation.expand_labels)
function.

```python
from skimage.segmentation import expand_labels

viewer.layers.remove('instance_seg')

instance_seg = expand_labels(instance_seg, 10)

viewer.add_labels(instance_seg)
```
![](fig/instance_segmentation_expanded.png){
alt="Expanded instance segmentation on the eroded segmentation mask"}
There are now 19 apparently correctly labelled nuclei that appear to be
the same shape as in the original mask image.

:::::::::::::::::::::::::challenge

### Is the erosion completely reversible?
In order to create a correct instance segmentation we have performed a
mask erosion followed by a label expansion. This is a common image
operation often used to remove back ground noise, known as as `opening`,
or an erosion followed by a dilation. In addition to helping us separate
instances it will have the effect of removing objects smaller than the
erosion mask, in this case a sphere with radius 10 pixels.
If we compare the eroded and expanded image with the original mask,
what will we see?

:::::::::::::::::::::::::solution

![](fig/instance_segmentation_vs_semantic_segmentation.png){
alt="A comparison between the expanded instance segmentation and the
original semantic segmentation showing some mismatch between the borders."}
Looking at the above image we can see some small mismatches around the
edges of most of the nuclei. Will the effect of this on the accuracy of
our results be significant?

:::::::::::::::::::::::::
:::::::::::::::::::::::::
## Removing Border Cells
If we do a pixel count on the instance segmentation now, we will still get
some unrealistically small nuclei as some nuclei are only partially in the
image. We can remove these from our analysis using scikit-image's
[clear border](
https://scikit-image.org/docs/stable/api/skimage.segmentation.html#skimage.segmentation.clear_border)
function.

```python

from skimage.segmentation import clear_border

viewer.layers.remove('instance_seg')

instance_seg = clear_border(instance_seg)

viewer.add_labels(instance_seg)
```

![](fig/instance_segmentation_clear_border.png){
alt="The instance segmentation with any nuclei crossing the image boundary
removed"}
We now have an image with 11 clearly labelled nuclei. Let's check the
nuclei count as we did above.

```python
# First count the nuclei
number_of_nuclei = instance_seg.max()
print(f"There are {number_of_nuclei} individual nuclei")
```
```output
There are 19 individual nuclei
```
What's happened here? When we ran `clear_borders` the pixels corresponding
to border nuclei were set to zero, however the total number of labels
in the image was not changed, so whilst there are 19 labels in the
image some of them have no corresponding pixels. The easiest way to
correct this is to re label the image.
```python
instance_seg = label(instance_seg)
number_of_nuclei = instance_seg.max()
print(f"There are {number_of_nuclei} individual nuclei")
```
```output
There are 11 individual nuclei
```
Now let's re-run our measurement script from above.

```python
# Create an empty list
nucleus_pixels = []
# Go through each nucleus,
for nucleus_id in range(1, number_of_nuclei + 1):
  # And append the number of pixels to the list
  nucleus_pixels.append(np.count_nonzero(instance_seg == nucleus_id))

# Convert size in pixels to size in cubic micrometres
nucleus_um = pixel_size * np.array(nucleus_pixels)

# Use Numpy's peak to peak function (ptp) to find the range.
print(f"Range of Nucleus sizes = {np.ptp(nucleus_um):.2f} cubic micrometres.")

# Find the mean nuclei size
print(f"Nucleus size mean = {np.mean(nucleus_um):.2f} cubic micrometres.")

# And the standard deviation
print(f"Nucleus size standard dev. = {np.std(nucleus_um):.2f} cubic micrometres.")
```
```output
Range of Nucleus sizes = 413.56 cubic micrometres.
Nucleus size mean = 611.29 cubic micrometres.
Nucleus size standard dev. = 121.54 cubic micrometres.
```
These numbers provide a good quantitative measure of the quantity and
size of cell nuclei suitable for an experiment investigating how these
quantities change over time.

We can save our work from the console for re-use on data from subsequent
time points, creating a repeatable measurement workflow.

```python
%save measurement_workflow ~0/
```
This will create a Python file `measurement_pipepine.py` that we can
load into the Napari console and re-run. You may choose to edit the file
with any text editor to remove some of the redundant steps we've made
whilst learning.

::::::::::::::::::::::::::::::::::::: keypoints

- We use a workflow of standard image processing functions to get from
an image to a measurement.

- The Napari console can be used to test various functions and develop the
workflow.

- The console's save and load functions allow to create a reproducible
image processing workflow.

::::::::::::::::::::::::::::::::::::::::::::::::

