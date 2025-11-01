---
title: Setup
---

## Download Data

During these lessons we will be using two microscopy images and creating images
of our own. Create an empty folder somewhere on your computer to use during the
course, this will be your `working directory`. You can name it anything you
like but we recommend `microscopy-ideas`.

Download
[00001_01.ome.tiff](
https://downloads.openmicroscopy.org/images/OME-TIFF/2016-06/MitoCheck/00001_01.ome.tiff)
 ([CC BY 4.0 Licence](
https://downloads.openmicroscopy.org/images/OME-TIFF/2016-06/MitoCheck/readme.txt))
 from the open microscopy environment pages to your working directory.

Download
[Plate1-Blue-A-12-Scene-3-P3-F2-03.czi](
https://downloads.openmicroscopy.org/images/Zeiss-CZI/idr0011/Plate1-Blue-A_TS-Stinger/Plate1-Blue-A-12-Scene-3-P3-F2-03.czi)
 ([CC BY 4.0 Licence](
https://downloads.openmicroscopy.org/images/Zeiss-CZI/idr0011/readme.txt))
from the open microscopy environment pages to your working directory.

## Install conda

During these lessons we will use the [napari](https://napari.org/stable/)
image viewer and 
[BioIO](https://bioio-devs.github.io/bioio/OVERVIEW.html)
 to load imaging data files of various file formats.
 
We will use conda to install / manage these packages. If you already have
conda installed (e.g. via Miniforge, Anaconda or similar), you can skip to the
[install python packages](#install-python-packages) section below.

Otherwise, download the latest 
[Miniforge distribution of Python](https://conda-forge.org/download/) for your
operating system. Then install as below:

::::::::::::::::::::::::::::::::::::::::::: spoiler

### Windows

- Double click on the downloaded `.exe` file
- If you get a "Windows protected your PC" pop-up from Microsoft Defender 
  SmartScreen, click on "More info" and select "Run anyway"
- Follow through the installer using all of the defaults for installation 
_except_ make sure to check **Add Miniforge3 to my PATH environment variable**.

:::::::::::::::::::::::::::::::::::::::::::
::::::::::::::::::::::::::::::::::::::::::: spoiler

### MacOS or Linux

1. Open a terminal. (for macOS - this is done via 
  `Launchpad > Other Application > Terminal`)
 
2. Type the following into the terminal and click <kbd>Enter</kbd> 
  (or <kbd>Return</kbd> depending on your keyboard).
  ```bash
  cd ~/Downloads
  ```
   
3. Type the following into the terminal, then `Tab` to autocomplete the full 
  file name. The name of the file you just downloaded should appear. 
  Press <kbd>Enter</kbd>.
  ```bash
  bash Miniforge3-
  ```
   
4. Follow the text-only prompts in the terminal. To move through the text, 
  press <kbd>Spacebar</kbd>.
  - Type `yes` and press <kbd>Enter</kbd> to approve the license.
  - Press <kbd>Enter</kbd> to approve the default location for the files.
  - Type `yes` and press <kbd>Enter</kbd> to prepend Miniforge to your PATH 
    (this makes the Miniforge distribution the default Python).

:::::::::::::::::::::::::::::::::::::::::::

If you encounter issues installing / using Miniforge, you can 
[download and install Anaconda](https://www.anaconda.com/download#downloads)
instead.

(The installation instructions above are modified from the 
[Carpentries workshop template](https://github.com/carpentries/workshop-template) 
- [CC BY 4.0](https://github.com/carpentries/workshop-template/blob/gh-pages/LICENSE.md))

## Install python packages

The remaining instructions are written assuming you will be installing and
running the software from a terminal.
Follow the
instructions below to open a terminal on your operating system.

::::::::::::::::::::::::::::::::::::::::::: spoiler

### Opening a Terminal

 - Windows (if you used Miniforge): Click Start > Search for Miniforge Prompt > Click to Open
 - Windows (if you used Anaconda): Click Start > Search for Anaconda Prompt > Click to Open
 - macOS: Launchpad > Other Application > Terminal
 - Linux: Open a terminal window

:::::::::::::::::::::::::::::::::::::::::::

Run the commands below (using the dropdown for your operating system) in the 
terminal. Lines starting with # are comments and do not need to be run.
You can run the commands by copy and pasting them into the terminal and
pressing the <kbd>Enter</kbd> key.

::::::::::::::::::::::::::::::::::::::::::: spoiler

### Windows and Linux

```bash
# Make sure conda is up to date
conda update -n base conda

# This line will create a "virtual environment" (called napari-env)
# that will contain all of the software that will be used in the lessons
conda create -y -n napari-env -c conda-forge python=3.12

# Activate the napari-env virtual environment.
# Running this should change the terminal prompt to '(napari-env)'.
conda activate napari-env

# Install napari and plugins using pip
pip install "napari[all]" napari-bioio-reader bioio-czi
```

:::::::::::::::::::::::::::::::::::::::::::
::::::::::::::::::::::::::::::::::::::::::: spoiler

### MacOS

```bash
# This line will create a "virtual environment" (called napari-env)
# that will contain all of the software that will be used in the lessons
conda create -y -n napari-env -c conda-forge python=3.12 napari pyqt

# Activate the napari-env virtual environment.
# Running this should change the terminal prompt to '(napari-env)'.
conda activate napari-env

# Install czi file reader
pip install napari-bioio-reader bioio-czi
```

:::::::::::::::::::::::::::::::::::::::::::

:::::::::::::::::::::::::::::::::::::: spoiler

## Why is there so much text appearing on the screen?

If you're new to running commands in the terminal you may be alarmed if
running some of these commands results in a lot of text output to the
screen. This is normal and usually helpful for checking things are
working OK. For our purposes you can ignore it. If you see the word
ERROR appear near the end (often highlighted in a different colour)
it is possible something has gone wrong. In this case the best place
to start is any messages in the text expanding on the source of the error.

::::::::::::::::::::::::::::::::::::::

## Post Setup Checks

Before starting the course it is important to check that your setup is working.

::::::::::::::::::::::::::::::::::::::: challenge

## Check napari opens a tiff image.

Any napari installation should be able to open a tiff image. Start napari.
Note that if you're already in the napari-env virtual environment from the
installation steps it is not necessary to run `conda activate napari-env`.
```bash
conda activate napari-env
napari
```
Note: Napari may take a few minutes to open the first time.
You should now see the napari viewer like this ...

![](../episodes/fig/blank-napari-ui.png){alt="A
 screenshot of the default Napari user interface" width='60%'}

Open a file with

`File > Open file(s)...`

- Navigate to the directory where you saved `00001_01.ome.tiff` earlier on.
- Select `00001_01.ome.tiff` and click open.
- If you see a `Choose reader` dialog, select `napari builtins`.

::::::::::::::::::::::::::
::::::::::::::::::: solution

## Expected Output

![If this is what you see your napari installation is working as expected.
If not then please check the installation first
by re-running the above steps and checking for any error messages in the
terminal output. If that fails please get in touch with the course
 organisers for help.](fig/ome_00001.png){alt="A screenshot of freshly
 opened 00001_01.ome.tiff" width='80%'}

Close napari: `File > exit`

::::::::::::::::::::::::::

:::::::::::::::::::: challenge

## Check napari opens a czi image.

During the course we'll be working with czi images. To open these the
BioIO package is needed. Let's check this package is working.

Start napari. Note that if you've already done the previous test (tiff image)
then it should not be necessary to run `conda activate napari-env`.
However, it is necessary to restart napari to ensure the image display
is correctly formatted.

```bash
conda activate napari-env
napari
```

`File > Open file(s)...`

- Navigate to the directory where you saved
`Plate1-Blue-A-12-Scene-3-P3-F2-03.czi` to earlier on.
- Select `Plate1-Blue-A-12-Scene-3-P3-F2-03.czi` and click open.
- If you see a `Choose reader` dialog, select `Bioio Reader`.

Note: the `Bioio Reader` automatically installs the `bioio-bioformats` reader, 
which has additional java dependencies. The first time you open the `czi` image, 
you may see lots of text printed to the terminal as it downloads these extra 
files. This may take up to 5 minutes - so give it some time. This will only 
happen once, and the `czi` image will open much faster next time.

::::::::::::::::::::::::::
::::::::::::::::::: solution

## Expected Output

![If this is what you see your napari and BioIO plugin installation
 is working as expected.
If not then please check the installation first
by re-running the above steps and checking for any error messages in the
terminal output. If that fails please get in touch with the course
 organisers for help.](fig/plate1-blue.png){alt="A
 screenshot of freshly opened Plate1-Blue-A-12-Scene-3-P3-F2-03.czi"
 width='80%'}

Close napari: `File > exit`

::::::::::::::::::::::::::
