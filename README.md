# Image Analysis with Napari for Microscopy

A lesson teaching the fundamentals of analysing image data acquired via light microscopy experiments.

## Lesson Content

This lesson focuses on the use of [napari](https://napari.org/), a Python-based image viewer, for all image processing steps.
It also covers the basics of how to design a light microscopy experiment and optimise acquisition settings for a given research question.

## Contribution

Contributions are very welcome - please make a suggestion or correct an error by [raising an issue](https://github.com/HealthBioscienceIDEAS/microscopy-novice/issues).

See the [CONTRIBUTING.md file](CONTRIBUTING.md) for contribution guidelines.

## Acknowledgements

These lessons were initially developed as part of the [Health and Biosciences IDEAS](https://healthbioscienceideas.github.io/) project, which is a training initiative funded by [UKRI Innovation Scholars](https://www.ukri.org/opportunity/innovation-scholars-data-science-training-in-health-bioscience/) (MR/V03863X/1). 

Continued support for this project is provided in part by the [UKRI Digital Research Skills Catalyst](https://digitalskillscatalyst.ac.uk/). 
The Catalyst Project is funded by UKRI Digital Research Infrastructure Programme from October 2024 to March 2027. Project reference: UKRI/ST/B000299/1.

## Development

This course is developed using the [Carpentries Workbench](https://carpentries.github.io/workbench/).
The *sandpaper* R package is the main driver used to configure and build the
website (see installation instructions [below](#building-the-lesson-locally)).

For a comprehensive guide on how to use *sandpaper*, check out the
[documentation](https://carpentries.github.io/sandpaper-docs/).

When making changes, please create a new branch and open a Pull Request. Don't
push directly to `main`.

```sh
## Create new branch
git checkout main
git pull origin main
git switch -c <username>/<my_awesome_edits>
```

The basic workflow looks something like this (it's recommended, though not
necessary, to run this in
[RStudio](https://posit.co/download/rstudio-desktop/)):

```r
## Add new episode in plain Markdown format (use `create_episode_Rmd` for RMarkdown)
sandpaper::create_episode_md("Episode name")
## ...... Edit new episode md contents ......

## Preview site
sandpaper::serve()

## ...... Make further changes, the website preview should update automatically ......
## ...... Rinse and repeat ......
```

When you're happy, commit, push and open a PR on GitHub. This will trigger the
[*sandpaper* PR validation and preview
workflows](https://carpentries.github.io/sandpaper-docs/pull-request.html) to
validate and preview the new content. Once the PR gets approved, merge it into
`main` and wait for the github actions to complete, after which the updates 
should be visible on the
[website](https://healthbioscienceideas.github.io/microscopy-novice/)

### Building the lesson locally

The [*sandpaper*](https://github.com/carpentries/sandpaper) package is used to
build the lesson website. We created a fork of [*varnish*](https://github.com/HealthBioscienceIDEAS/varnish) to style the lesson website with **IDEAS** branding.

To install these forks locally, run the following from within an R session:

```r
## Install devtools
install.packages("remotes")

## Install HealthBioscienceIDEAS/varnish 
remotes::install_github("HealthBioscienceIDEAS/varnish", dependencies = TRUE)
```

Then to build the lesson locally, from within the `microscopy-novice` directory, run

```r
sandpaper::build_lesson()
```

That _should_ open the built home page in a browser window automatically, but
if not, you can find the built HTML files in the `site/` directory.
