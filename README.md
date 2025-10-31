# microscopy-novice

    This is the lesson repository for microscopy-novice

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
`main` and wait for the [Build and
Deploy](https://github.com/HealthBioscienceIDEAS/microscopy-novice/actions/workflows/sandpaper-main.yaml)
action to complete, after which the updates should be visible on the
[website](https://healthbioscienceideas.github.io/microscopy-novice/)

### Building the lesson locally

The [*sandpaper*](https://github.com/carpentries/sandpaper) package is used to
build the lesson website. We created a fork of [*varnish*](https://github.com/HealthBioscienceIDEAS/varnish) to style the lesson website with **IDEAS** branding.

To install these forks locally, run the following from within an R session:

```r
## Install devtools
install.packages("remotes")

## Install sandpaper and varnish from the IDEAS forks
## HealthBioscienceIDEAS/varnish is listed as a dependency of sandpaper, so will be installed as well
remotes::install_github("HealthBioscienceIDEAS/sandpaper", dependencies = TRUE)
```

Then to build the lesson locally, from within the `microscopy-novice` directory, run

```r
sandpaper::build_lesson()
```

That _should_ open the built home page in a browser window automatically, but
if not, you can find the built HTML files in the `site/` directory.
