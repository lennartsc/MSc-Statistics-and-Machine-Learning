
<!-- README.md is generated from README.Rmd. Please edit that file -->
[![Travis build status](https://travis-ci.com/lennartsc/rLab5.svg?branch=master)](https://travis-ci.com/lennartsc/rLab5)

[![Coverage status](https://codecov.io/gh/lennartsc/rLab5/branch/master/graph/badge.svg)](https://codecov.io/github/lennartsc/rLab5?branch=master)

rLab5
=====

The goal of rLab5 is to create a R package to read from an API, in our case from APIXU.com which provides weather API.

Installation
------------

You can install the released version of rLab5 from [CRAN](https://CRAN.R-project.org) with:

``` r
install.packages("rLab5")
```

And the development version from [GitHub](https://github.com/) with:

``` r
# install.packages("devtools")
devtools::install_github("lennartsc/rLab5")
```

Example
-------

This is a basic example which shows you how to solve a common problem:

``` r
## basic example code
library(rLab5)
get_data("Bangalore", 1)
```
