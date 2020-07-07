name = "Lennart Schilling"
liuid = "lensc874"

# ********************************************************************************************
# 1.1 Conditional statements ####

## 1.1.1 sheldon_game(player1, player2)
sheldon_game = function(player1, player2) {
  if(!player1 %in% c("rock","paper","scissors","lizard","spock") |
     !player2 %in% c("rock","paper","scissors","lizard","spock")) {
    stop("at least one of the players did not make an available choice.")
  }
  if(player1 == player2) {
    matchResult = "Draw!"
  } else if(player1 == "rock" & player2 %in% c("scissors","lizard") |
            player1 == "paper" & player2 %in% c("spock","rock") |
            player1 == "scissors" & player2 %in% c("lizard","paper") |
            player1 == "lizard" & player2 %in% c("spock","paper") |
            player1 == "spock" & player2 %in% c("scissors","rock")) {
    matchResult = "Player 1 wins!"
  } else {
    matchResult = "Player 2 wins!"
  }
  return(matchResult)
}

# ********************************************************************************************
# 1.2 for loops ####

## 1.2.1 my_moving_median()
my_moving_median = function(x, n, ...) {
  if(!is.numeric(x)) {
    stop("x is not a numeric vector.")
  }
  if(!is.numeric(n)) {
    stop("n is not a numeric scalar.")
  }
  movingMedian = c()
  for(t in 1:(length(x)-n)) {
    movingMedian = c(movingMedian,median(x[t:(t+n)], ... ))
  }
  return(movingMedian)
}

## 1.2.2 for_mult_table
for_mult_table = function(from, to) {
  if(!is.numeric(from)) {
    stop("argument 'from' is not a numeric scalar.")
  }
  if(!is.numeric(to)) {
    stop("argument 'to' is not a numeric scalar.")
  }
  inputSequence = seq(from = from,
                      to = to,
                      by = 1)
  forMultTable = matrix(data = NA,
                        nrow = length(inputSequence),
                        ncol = length(inputSequence),
                        dimnames = list(inputSequence, inputSequence))
  for(rowname in rownames(forMultTable)) {
    for(colname in colnames(forMultTable)) {
      forMultTable[rowname,colname] = as.numeric(rowname)*as.numeric(colname)
    }
  }
  return(forMultTable)
}

# ********************************************************************************************
# 1.3 while loops ####

## 1.3.1 find_cumsum()
find_cumsum = function(x, find_sum) {
  if(!is.numeric(x)) {
    stop("argument 'x' has to be a numeric vector.")
  }
  if(!is.numeric(find_sum)) {
    stop("argument 'find_sum' has to be a numeric scalar.")
  }
  cumSum = 0
  i = 1
  while(cumSum <= find_sum & i <= length(x)) {
    cumSum = cumSum + x[i]
    i = i+1
  }
  return(cumSum)
}

## 1.3.2 while_mult_table
while_mult_table = function(from, to) {
  if(!is.numeric(from)) {
    stop("argument 'from' is not a numeric scalar.")
  }
  if(!is.numeric(to)) {
    stop("argument 'to' is not a numeric scalar.")
  }
  inputSequence = seq(from = from,
                      to = to,
                      by = 1)
  output = matrix(data = NA,
                  nrow = length(inputSequence),
                  ncol = length(inputSequence),
                  dimnames = list(inputSequence, inputSequence))
  while(sum(is.na(output)) > 0) {
    output[which(is.na(output))[1]] =
      as.numeric(rownames(output)[row(output)[which(is.na(output))[1]]]) *
      as.numeric(colnames(output)[col(output)[which(is.na(output))[1]]])
  }
  return(output)
}

# ********************************************************************************************
# 1.4 repeat and loop controls ####

## 1.4.1 repeat_find_cumsum()
repeat_find_cumsum = function(x, find_sum) {
  if(!is.numeric(x)) {
    stop("argument 'x' has to be a numeric vector.")
  }
  if(!is.numeric(find_sum)) {
    stop("argument 'find_sum' has to be a numeric scalar.")
  }
  cumSum = 0
  i = 1
  repeat {
    cumSum = cumSum + x[i]
    i = i+1
    if(i>length(x) | cumSum > find_sum) {
      break
    }
  }
  return(cumSum)
}

## 1.4.2 repeat_my_moving_median()
repeat_my_moving_median = function(x, n, ...) {
  if(!is.numeric(x)) {
    stop("x is not a numeric vector.")
  }
  if(!is.numeric(n)) {
    stop("n is not a numeric scalar.")
  }
  movingMedian = c()
  t = 1
  repeat {
    movingMedian = c(movingMedian,median(x[t:(t+n)], ...))
    t = t+1
    if(t > (length(x)-n)) {
      break
    }
  }
  return(movingMedian)
}

# ********************************************************************************************
# 1.5 Environment ####

## 1.5.1 in_environment()
in_environment = function(env) {
  return(ls(env))
}

# ********************************************************************************************
# 1.6 Functionals ####

## 1.6.1 cov()
cov = function(X) {
  if(!is.data.frame(X)){
    stop("X is not of class 'data.frame'")
  }
  return(
    unlist(lapply(X, function(X) sd(X)/mean(X)))
  )
}

# ********************************************************************************************
# 1.7 Closures ####

## 1.7.1 moment()
moment = function(i) {
  if(!is.numeric(i)){
    stop("i has to be numeric.")
  }
  return(
    function(x) {
      sum = c()
      mean = mean(x)
      for(elem in x) {
        sum = c(sum, (elem-mean)^i)
      }
      return(mean(sum))
    }
  )
}




