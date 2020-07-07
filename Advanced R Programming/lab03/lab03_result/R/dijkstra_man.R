#' Title
#'
#' @param graph the input dataframe which represents a network
#' @param init_node the node for which the distance to other nodes must be calculated
#'
#' @return returns a vector with distances to other nodes
#' @export
#' @source \href{https://en.wikipedia.org/wiki/Dijkstra\%27s_algorithm}{Wikipedia}
#'
#' @examples wiki_graph <-
#' data.frame(v1=c(1,1,1,2,2,2,3,3,3,3,4,4,4,5,5,6,6,6),
#' v2=c(2,3,6,1,3,4,1,2,4,6,2,3,5,4,6,1,3,5),
#' w=c(7,9,14,7,10,15,9,10,11,2,15,11,6,6,9,14,2,9))
#' dijkstra_man(wiki_graph, 1)

dijkstra_man = function(graph, init_node) {
  # checking input
  if(NCOL(graph) != 3){stop("Incorrect dataframe size")}
  if(any(colnames(graph) != c("v1", "v2", "w"))){stop("Incorrect dataframe names")}
  if(init_node >= length(unique(graph[,1]))){stop("Incorrect node selected")}
  if(!is.data.frame(graph) | !is.numeric(init_node)) {
    stop("input is not correct.")
  }
  # initialization of vectors 'nodesToVisit' and 'distances'
  nodesToVisit = c()
  distances = c()
  for (node in unique(graph$v1)) {
    # every distinct node in the graph will be added to the vector 'notesToVisit'
    nodesToVisit = c(nodesToVisit, node)
    # at the beginning, distance to the init_node will be set to zero and to all other notes to infinite
    if(node != init_node) {
      distances[as.character(node)] = Inf
    } else {
      distances[as.character(node)] = 0
    }
  }
  # distance adjustment
  while(length(nodesToVisit) >= 1) {
    # in a loop, always the node of 'nodesToVisit' will the minimal distance to the init_node will be chosen
    currentNode = as.numeric(names(distances)[distances == min(distances[names(distances) %in% nodesToVisit])])[1]
    # for every neigbor of the currentNode, the distance to the init_note will be checked. If the distance is smaller than the currently saved distance, it will be edited.
    for (neighbor in graph[graph$v1 == currentNode,]$v2) {
      if(unname(distances[names(distances) == currentNode]) +
         graph[graph$v1 == currentNode & graph$v2 == neighbor,]$w < (unname(distances[names(distances) == neighbor]))) {
        distances[names(distances) == neighbor] = distances[names(distances) == currentNode] + graph[graph$v1 == currentNode & graph$v2 == neighbor,]$w
      }
    }
    # every node will be just visited once
    nodesToVisit = nodesToVisit[-which(nodesToVisit == currentNode)]
  }
  return(unname(distances))
}
