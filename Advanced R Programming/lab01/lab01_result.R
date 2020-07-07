name = "Lennart Schilling"
liuid = "lensc874"

# ********************************************************************************************
# 1.1 Vectors ####

## 1.1.1 my_num_vector()
my_num_vector = function() {
  return(c(log(11, base = 10),
           cos(pi/5),
           exp(pi/3),
           (1173 %% 7) / 19
           )
         )
}

## 1.1.2 filter_my_vector(x, leq)
filter_my_vector= function(x, leq)  {
  x[x >= leq] = NA
  return(x)
}

## 1.1.3 dot_prod(a, b)
dot_prod = function(a, b) {
  return(sum(a*b))
}

## 1.1.4 approx_e(N)
approx_e = function(N) {
  e = 0
  for (i in 0:N) {
    e = e + 1/factorial(i)
  }
  return(e)
}

testNeededSizeOfN = function() {
  e = round(exp(1),5)
  N = 0
  approx_e = approx_e(N)
  while(approx_e != e) {
    N = N+1
    approx_e = approx_e(N)
  }
  return(N)
}
testNeededSizeOfN() # N needs to be 8 to approximate e to the fifth decimal place.

# ********************************************************************************************
# 1.2 Matrices ####

## 1.2.1 my_magic_matrix()
my_magic_matrix = function() {
  return(matrix(c(4,3,8,9,5,1,2,7,6),3,3))
}

## 1.2.2 calculate_elements(A)
calculate_elements = function(A) {
  nElements = 0
  for(i in A) {
    nElements = nElements + 1
  }
  return(nElements)
}

## 1.2.3 row_to_zero(A, i)
row_to_zero = function(A, i) {
  A[i,] = 0
  return(A)
}

## 1.2.4 add_elements_to_matrix(A, x, i, j)
add_elements_to_matrix = function(A, x, i, j) {
  A[i,j] = A[i,j] + x
  return(A)
}
# answer: functionality of the function is clear. Examples helped a lot and should be kept.

# ********************************************************************************************
# 1.3 Lists ####

## 1.3.1 my_magic_list()
my_magic_list = function() {
  return(
    list(
      info = "my own list",
      my_num_vector(),
      my_magic_matrix()
    )
  )
}

## 1.3.2 change_info(x, text)
change_info = function(x, text) {
  x[["info"]] = text
  return(x)
}

## 1.3.3 add_note(x, note)
add_note = function(x, note) {
  x[["note"]] = note
  return(x)
}

## 1.3.4 sum_numeric_parts(x)
sum_numeric_parts = function(x) {
  sumNumericParts = 0
  for (elem in x) {
    if(!is.character(elem)) {
      sumNumericParts = sumNumericParts + sum(elem)
    }
  }
  return(sumNumericParts)
}

# ********************************************************************************************
# 1.4 data.frames ####

## 1.4.1 my.data.frame()
my_data.frame = function() {
  df = data.frame(id = c(1,2,3), 
                  name = c("John","Lisa","Azra"), 
                  income = c(7.3, 0, 15.21), 
                  rich = c(FALSE,FALSE,TRUE)
                  )
  return(df)
}

## 1.4.2 sort_head(df, var.name, n)
sort_head = function(df, var.name, n) {
  df = df[order(-df[var.name]),][1:n,]
  return(df)
}

## 1.4.3 add_median_variable(df, j)
add_median_variable = function(df, j) {
  median = median(df[,j])
  df[df[,j]-median == 0,"compared_to_median"] = "Median"
  df[df[,j]-median > 0,"compared_to_median"] = "Greater"
  df[df[,j]-median < 0,"compared_to_median"] = "Smaller"
  return(df)
}

## 1.4.4 analyze_columns(df, j)
analyze_columns = function(df, j) {
  list = list()
  for(i in 1:2) {
    list[[colnames(df)[j[i]]]] = c(mean = mean(df[,j[i]]),
                                   median = median(df[,j[i]]),
                                   sd = sd(df[,j[i]]))
  }
  list[["correlation_matrix"]] = cor(df[,j])
  return(list)
}

