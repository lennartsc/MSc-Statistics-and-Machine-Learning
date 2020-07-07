context("test-testing_package.R")

test_that("get_data works", {
  expect_error(get_data(1,1))
  expect_error(get_data(1,X))
})
