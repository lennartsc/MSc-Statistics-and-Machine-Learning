#' Title Dynamic Program Knapsack
#'
#' @param x The input to function containing the number of items
#' @param W The weights of the items
#'
#' @return NULL
#' @export
#' @source http://www.es.ele.tue.nl/education/5MC10/Solutions/knapsack.pdf
#'
#' @examples set.seed(42)
#' n <- 2000
#' knapsack_objects <- data.frame(w=sample(1:4000, size = n, replace = TRUE), v=runif(n = n, 0, 10000))
#'knapsack_dynamic(x = knapsack_objects[1:8,], W = 3500)
#'
knapsack_dynamic <- function(x, W){

  stopifnot(is.data.frame(x),is.numeric(W))
  stopifnot(W > 0)

  # reorder the items according to their weight to get near the maximum as soon as possible
  x <- x[rev(order(x[,1])),]

  # remove combinations that are invalid from the start
  # only consider items with a weight that is less than the capacity
  x <- x[x[,'w']<=W,]
  elements <- rownames(x)
  w <-(x[,1])
  p <-(x[,2])

  n <- nrow(x)
  # initiate arrays
  x <- logical(n)
  F <- matrix(0, nrow = W + 1, ncol = n)
  G <- matrix(0, nrow = W + 1, ncol = 1)

  # forwarding part
  for (k in 1:n) {
    F[, k] <- G
    H <- c(numeric(w[k]), G[1:(W + 1 - w[k]), 1] + p[k])
    G <- pmax(G, H)
  }
  fmax <- G[W + 1, 1]

  # backtracking part
  f <- fmax
  j <- W + 1
  for (k in n:1) {
    if (F[j, k] < f) {
      x[k] <- TRUE
      j <- j - w[k]
      f <- F[j, k]
    }
  }

  inds <- which(x)
  elem <- elements[x]
  prof <- round(sum(p[inds]))
  elem <- noquote(elem)
  return(list(value = prof, elements = elem))
}
