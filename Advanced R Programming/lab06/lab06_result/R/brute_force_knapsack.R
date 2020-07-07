#' Title The Brute Force Knapsnack Solver
#'
#' @param x The input to function containing the number of items
#' @param W The weights of the items
#'
#'
#' @return NULL
#' @export
#' @importFrom utils combn
#' @examples set.seed(42)
#' n <- 2000
#' knapsack_objects <- data.frame(w=sample(1:4000, size = n, replace = TRUE), v=runif(n = n, 0, 10000))
#'brute_force_knapsack(x = knapsack_objects[1:8,], W = 3500)
#'
brute_force_knapsack <- function(x, W){
  original_value = x

    stopifnot(is.data.frame(x),is.numeric(W))
    stopifnot(W > 0)

  # reorder the items according to their weight to get near the maximum as soon as possible
  x <- x[rev(order(x[,1])),]

  # remove combinations that are invalid from the start
  # only consider items with a weight that is less than the capacity
  x <- x[x[,'w']<=W,]
  elements <- rownames(x)
    i=2
    optimum_value = 0
    selected_items = c()
    weights<-c()
    values<-c()
    while(i<=nrow(x))
    {
      w<-as.data.frame(combn(x[,1], i))
      v<-as.data.frame(combn(x[,2], i))

        sumw<-colSums(w) # most time consuming using profvis
        sumv<-colSums(v) # most time consuming using profvis

      weights<-which(sumw<=W)
      if(length(weights) != 0){
        values<-sumv[weights]
        optimum_value<-max(values)
        temp<-which((values)==optimum_value)
        maxValWghtIdx<-weights[temp]
        maxValWght<-w[, maxValWghtIdx]
        j<-1
        while (j<=i){
          selected_items[j]<-which(x[,1]==maxValWght[j])
          j=j+1
        }
      }
      i=i+1

    }
    elem <- subset(original_value, w %in% maxValWght)
    elem <- noquote(rownames(elem))

    return(list(value=round(optimum_value), elements=elem))
}
