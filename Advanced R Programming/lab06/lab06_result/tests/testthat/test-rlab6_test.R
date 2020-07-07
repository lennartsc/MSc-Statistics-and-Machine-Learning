context("test-rlab6_test.R")

set.seed(42)
n <- 2000
knapsack_objects <- data.frame(
  w=sample(1:4000, size = n, replace = TRUE),
  v=runif(n = n, 0, 10000)
)

test_that("brute_force_knapsack works", {
  expect_silent(bfk <- brute_force_knapsack(x = knapsack_objects[1:8,], W = 3500))
  expect_named(bfk, c("value", "elements"))
})


test_that("functions rejects errounous input.", {
  expect_error(brute_force_knapsack("hej", 3500))
  expect_error(brute_force_knapsack(x = knapsack_objects[1:8,], W = -3500))
})

test_that("Function return correct results.", {
  bfk <- brute_force_knapsack(x = knapsack_objects[1:8,], W = 3500)
  expect_equal(round(bfk$value), 16770)
  expect_true(all((bfk$elements) %in% c(5, 8)))

  bfk <- brute_force_knapsack(x = knapsack_objects[1:12,], W = 3500)
  expect_equal(round(bfk$value), 16770)
  expect_true(all((bfk$elements) %in% c(5, 8)))

  bfk <- brute_force_knapsack(x = knapsack_objects[1:8,], W = 2000)
  expect_equal(round(bfk$value), 15428)
  expect_true(all((bfk$elements) %in% c(3, 8)))

  bfk <- brute_force_knapsack(x = knapsack_objects[1:12,], W = 2000)
  expect_equal(round(bfk$value), 15428)
  expect_true(all((bfk$elements) %in% c(3, 8)))

  start.time <- Sys.time()
  brute_force_knapsack(x = knapsack_objects[1:16,], W = 2000)
  end.time <- Sys.time()
  time.taken <- end.time - start.time
  expect_true(as.numeric(time.taken) >= 0.00)
})

test_that("knapsack_dynamic works", {
  expect_silent(bfk <- knapsack_dynamic(x = knapsack_objects[1:8,], W = 3500))
  expect_named(bfk, c("value", "elements"))
})


test_that("functions rejects errounous input.", {
  expect_error(knapsack_dynamic("hej", 3500))
  expect_error(knapsack_dynamic(x = knapsack_objects[1:8,], W = -3500))
})

test_that("Function return correct results.", {
  bfk <- knapsack_dynamic(x = knapsack_objects[1:8,], W = 3500)
  expect_equal(round(bfk$value), 16770)
  expect_true(all((bfk$elements) %in% c(5, 8)))

  bfk <- knapsack_dynamic(x = knapsack_objects[1:12,], W = 3500)
  expect_equal(round(bfk$value), 16770)
  expect_true(all((bfk$elements) %in% c(5, 8)))

  bfk <- knapsack_dynamic(x = knapsack_objects[1:8,], W = 2000)
  expect_equal(round(bfk$value), 15428)
  expect_true(all((bfk$elements) %in% c(3, 8)))

  bfk <- knapsack_dynamic(x = knapsack_objects[1:12,], W = 2000)
  expect_equal(round(bfk$value), 15428)
  expect_true(all((bfk$elements) %in% c(3, 8)))

  start.time <- Sys.time()
  knapsack_dynamic(x = knapsack_objects[1:16,], W = 2000)
  end.time <- Sys.time()
  time.taken <- end.time - start.time
  expect_true(as.numeric(time.taken) >= 0.00)
})

test_that("Correct object is returned", {
  expect_silent(gk <- greedy_knapsack(x = knapsack_objects[1:8,], W = 3500))
  expect_named(gk, c("value", "elements"))
})

test_that("functions rejects errounous input.", {
  expect_error(greedy_knapsack("hej", 3500))
  expect_error(greedy_knapsack(x = knapsack_objects[1:8,], W = -3500))
})

test_that("Function return correct results.", {
  gk <- greedy_knapsack(x = knapsack_objects[1:8,], W = 3500)
  expect_equal(round(gk$value), 15428)
  expect_true(all((gk$elements) %in% c(3, 8)))

  gk <- greedy_knapsack(x = knapsack_objects[1:12,], W = 3500)
  expect_equal(round(gk$value), 15428)
  expect_true(all((gk$elements) %in% c(3, 8)))

  gk <- greedy_knapsack(x = knapsack_objects[1:8,], W = 2000)
  expect_equal(round(gk$value), 15428)
  expect_true(all((gk$elements) %in% c(3, 8)))

  gk <- greedy_knapsack(x = knapsack_objects[1:12,], W = 2000)
  expect_equal(round(gk$value), 15428)
  expect_true(all((gk$elements) %in% c(3, 8)))

  st <- system.time(gk <- greedy_knapsack(x = knapsack_objects[1:16,], W = 2000))
  expect_true(as.numeric(st)[2] <= 0.01)

  gk <- greedy_knapsack(x = knapsack_objects[1:800,], W = 3500)
  expect_equal((gk$value), 192647)

  gk <- greedy_knapsack(x = knapsack_objects[1:1200,], W = 3500)
  expect_equal((gk$value), 270290)
})
