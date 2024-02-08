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
#Save current session to a file called measure_percent.py
%save measure_percent ~0/
```
Delete the semantic_seg layer grom the viewer and run:
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
and assign each connected region a unique integer value. Let's try it

```python
#Import the label function
from skimage.measure import label

#Run the label function on the binary mask image
instance_seg = label(semantic_seg)

#Add the result to out viewer
viewer.add_labels(instance_seg)
```
![](fig/instance_segmentation_wrong.png){
alt="A screenshot of an instance segmentation of nuclei with some 
incorrectly joined instances."}
You should see the above image in the Napari viewer. The different colours
are used to represent different nuclei. Does it look right? 

There are several instances of nuclei that are clearly separate being
labelled as a single nuclei. Looking at the 4 nuclei at the bottom left that have all been labelled light blue, we can see that 3 of them are touching,
 so it is not surprising that they have been labelled as a single nuclei.
What about the forth apparently separate nuclei? We should remind ourselves
that this a 3 dimensional image. 
 
You may remember from our [first lesson](imaging-software.html#d3d) that 
we can change to 3D view mode by pressing the ![](
https://raw.githubusercontent.com/napari/napari/main/napari/resources/icons/2D.svg
){alt="A screenshot of Napari's 2D/3D toggle button" height='30px'} button.
Try it now.

![](fig/instance_segmentation_wrong3d.png){
alt="A screenshot of an instance segmentation of nuclei in 3D mode with some 
incorrectly joined instances."}
You should see the image rendered in 3D, with a clear join between the 
upper most light blue nuclei and its neighour. So now we understand why the
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
the semantic_seg layer with different integer values for the radius. 
What radius do you need to ensure all nuclei are separate?

```python
from skimage.morphology import binary_erosion, ball

#With radius = 1
radius = 1
eroded_mask = binary_erosion(semantic_seg, footprint = ball(radius = 1))
viewer.add_labels(eroded_mask, name = f'eroded ball {radius}')
```

:::::::::::::::::::::::::solution

```python
#We can use a for loop to test many values of radius. This will test all
#integers from 1 to 10
for radius in range(1,11):
  eroded_mask = binary_erosion(semantic_seg, footprint = ball(radius = 1))
  viewer.add_labels(eroded_mask, name = f'eroded ball {radius}')

```

![](fig/binary_mask_no_erosion.png){
alt="A screenshot of a semantic segmentation mask before erosion."}
The first image shows the binary mask without any erosion for comparison.

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

Now we have separate nuclei lets try creating instance labels 
again.

```python
eroded_semantic_seg = viewer.layers['eroded ball 10'].data

instance_seg = label(eroded_semantic_seg)

viewer.add_labels(instance_seg)
```


![](fig/instance_segmentation_eroded.png){
alt="Instance segmentation on the eroded segmentation mask"}

[expand labels](
https://scikit-image.org/docs/stable/api/skimage.segmentation.html#skimage.segmentation.expand_labels)


from skimage.filters import threshold_otsu, gaussian

```python
from skimage.segmentation import expand_labels
```
![](fig/instance_segmentation_expanded.png){
alt="Expanded Instance segmentation on the eroded segmentation mask"}

:::::::::::::::::::::::::challenge

### Is the erosion reversible?

:::::::::::::::::::::::::solution
Almost
![](fig/instance_segmentation_vs_semantic_segmentation.png){
alt="A comparison between the expanded instance segmentation and the
original semantic segmentation showing some mismatch between the borders."}

:::::::::::::::::::::::::
:::::::::::::::::::::::::

[clear border](
https://scikit-image.org/docs/stable/api/skimage.segmentation.html#skimage.segmentation.clear_border)

```python

from skimage.segmentation import clear_border
instance_seg_clear=clear_border(instance_seg)
viewer.add_labels(instance_seg_clear)
```

![](fig/instance_segmentation_clear_border.png){
alt="The instance segmentation with any nuclei crossing the image boundary
removed"}

image = viewer.layers["nuclei"].data


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

