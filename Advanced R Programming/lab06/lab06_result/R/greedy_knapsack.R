#' Title Greedy Algorithm Knapsack
#'
#' @param x The input to function containing the number of items
#' @param W The weights of the items
#' @param fast Whether to speed up using Rccp
#'
#' @return NULL
#' @export
#'
#' @examples set.seed(42)
#' n <- 2000
#' knapsack_objects <- data.frame(w=sample(1:4000, size = n, replace = TRUE), v=runif(n = n, 0, 10000))
#'greedy_knapsack(x = knapsack_objects[1:8,], W = 3500)
#'
#' @useDynLib rLab6, .registration = TRUE
#' @importFrom Rcpp sourceCpp

greedy_knapsack <- function(x, W, fast= NULL){

  stopifnot(is.data.frame(x),is.numeric(W))
  stopifnot(W > 0)

  x$v_by_w <- x$v/x$w

  # reorder the items according to their max profit per weight
  x <- x[rev(order(x$v_by_w)),]

  x$max_weight <- W

  # only consider items with a weight that is less than the capacity
  x <- x[x[,'w']<=W,]
  elements <- rownames(x)
  x$running_weight_v_w <- cumsum(x$w)
  x$retain_in_bag_v_w <- ifelse(x$running_weight_v_w <= x$max_weight, "Retain", "Drop")

  x <- x[x$retain_in_bag_v_w == "Retain",]

  elem <- noquote(rownames(x))

  if(!is.null(fast)){
    prof <- round(vectorSum(x$v))
  }else{prof <- round(sum(x$v))}

  elem <- noquote(elem)


  return(list(value = prof, elements = elem))

}
