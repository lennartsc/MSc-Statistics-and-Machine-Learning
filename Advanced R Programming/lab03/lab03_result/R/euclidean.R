# 1.1.1 euclidean()

#' Title euclidean() returns the gcd
#'
#' @param a first parameter
#' @param b second parameter
#'
#' @return the gcd
#' @export
#' @source \href{https://en.wikipedia.org/wiki/Euclidean_algorithm}{Wikipedia}
#' @examples euclidean(100,1000)
euclidean <- function(a,b){
  a <- abs(a)
  b <- abs(b)
  if(a == 0 | b == 0 | is.na(a) | is.na(b) | !is.numeric(a) | !is.numeric(b)){stop("incorrect inputs")}
  if(a > b){
    temp <- b
    b <- a
    a <- temp
  }
  r <- b%%a
  return(ifelse(r, euclidean(a, r), a))
}
