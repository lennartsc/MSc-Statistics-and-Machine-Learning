context("test-my-test.R")

context("test-my-test.R")
test_that("package works", {
expect_equal(euclidean(100, 1000), 100)
expect_equal(euclidean(123612, 13892347912), 4)
expect_equal(euclidean(-100, 1000), 100)
expect_equal(dijkstra_man(wiki_graph, 1), c(0,7,9,20,20,11))
expect_equal(dijkstra_man(wiki_graph,3), c(9,10,0,11,11,2))
expect_equal(dijkstra_adv(wiki_graph,1), c(0,7,9,20,20,11))
expect_equal(dijkstra_adv(wiki_graph,3), c(9,10,0,11,11,2))
})

test_that("Error messages are returned for erronous input in the Dijkstra algorithm.", {
  wiki_wrong_graph <- wiki_graph
  names(wiki_wrong_graph) <- c("v1, v3, w")
  expect_error(dijkstra_man(wiki_wrong_graph, 3))
  expect_error(dijkstra_adv(wiki_wrong_graph, 3))
  wiki_wrong_graph <- wiki_graph[1:2]
  expect_error(dijkstra_man(wiki_wrong_graph, 3))
  expect_error(dijkstra_man(wiki_graph, 7))
  expect_error(dijkstra_man(as.matrix(wiki_graph), 3))
  expect_error(dijkstra_adv(wiki_wrong_graph, 3))
  expect_error(dijkstra_adv(wiki_graph, 7))
  expect_error(dijkstra_adv(as.matrix(wiki_graph), 3))
})

test_that("Wrong input throws an error.", {
  expect_error(euclidean("100", 1000))
  expect_error(euclidean(0, 1000))
  expect_error(euclidean(0, NA))
  expect_error(euclidean(100, "1000"))
  expect_error(euclidean(TRUE, "1000"))
})
