#' Title dijkstra_adv is the dataframe method for dijkstra
#'
#' @param df is the input dataframe
#' @param node is the node for which the distances are computed
#'
#' @return returns a vector with distance to all other nodes
#' @export
#' @importFrom dplyr left_join bind_rows
#' @importFrom data.table shift
#'
#' @source \href{https://en.wikipedia.org/wiki/Dijkstra\%27s_algorithm}{Wikipedia}
#'
#' @examples wiki_graph <- data.frame(v1=c(1,1,1,2,2,2,3,3,3,3,4,4,4,5,5,6,6,6),
#'  v2=c(2,3,6,1,3,4,1,2,4,6,2,3,5,4,6,1,3,5),
#'  w=c(7,9,14,7,10,15,9,10,11,2,15,11,6,6,9,14,2,9))
#'  dijkstra_adv(wiki_graph, 1)

dijkstra_adv <- function(df, node) {
  if(NCOL(df) != 3){stop("Incorrect dataframe size")}
  if(any(colnames(df) != c("v1", "v2", "w"))){stop("Incorrect dataframe names")}
  if(node >= length(unique(df[,1]))){stop("Incorrect node selected")}
  if(is.data.frame(df) & is.numeric(node)){
    n <- length(unique(df[,1]))
    colnames(df) <- c("S", "D", "W")
    result <- df

    for(i in 1:n-1){
      df2 <-  dplyr::left_join(x = result, y = df, by = c("D" = "S"))
      df2$W <- df2$W.x + df2$W.y
      df2 <- df2[,c("S", "D.y", "W")]
      colnames(df2)[colnames(df2)=="D.y"] <- "D"
      result <- dplyr::bind_rows(df2, df)
      result$W <- ifelse(result$S == result$D, 0, result$W) # fixing the self reference distance as zero
      result <- result[!duplicated(result),]
      rm(df2)
    }

    # sorting
    result <- result[with(result, order(S, D, W)), ]
    result$concat <- paste(result$S, result$D, sep = "")
    result$lag_concat <- data.table::shift(result$concat, n=1L, fill=0, type=c("lag"), give.names=FALSE)
    result$change_flag <- ifelse(result$concat == result$lag_concat, 0, 1)

    result <- result[result$change_flag == 1,]
    result <- result[, c("S", "D", "W")]

    temp_wide <- reshape2::dcast(result, S ~ D, value.var = "W", fill = 0)
    rownames(temp_wide) <- NULL
    return(as.vector(temp_wide[,node+1]))
  }
  else{stop("Input must be a dataframe")}}
