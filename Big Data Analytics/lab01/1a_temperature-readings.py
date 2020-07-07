from pyspark import SparkContext
import time

# Storing starting time.
start = time.time()

# Setting up Spark's execution environment.
sc = SparkContext(appName = "assignment1_temperature-readings")

# Creating RDD.
temperature_file = sc.textFile("/user/x_lensc/data/temperature-readings.csv")

# Performing RDD transformations.

## Splitting lines.
lines = temperature_file.map(lambda line: line.split(";"))
## Extracting year(key) and temperature, station_nr (value).
year_temperature = lines.map(lambda x: (x[1][0:4], (float(x[3]), x[0])))
## Filtering for period 1950-2014.
year_temperature = year_temperature.filter(lambda x: int(x[0]) in range(1950, 2015))

# Performing RDD actions.

## Identifying maximum temperature per year in descending order with respect to maximum temperature.
### Aggregating maximum temperature per year.
max_temperatures = year_temperature.reduceByKey(lambda a,b: a if a[0] >= b[0] else b)
### Sorting key-value-pairs by decreasing values.
max_temperatures_sorted = max_temperatures.sortBy(keyfunc = lambda elem: elem[1][0], ascending = False)
### Printing ordered maximum temperatures per year.
print("Extrat of results for data:" + "temperature-readings.csv:")
print("\nMaximum temperature per year (year, (temperature, station nr)) in descending order with respect to maximum temperature:\n")
print(max_temperatures_sorted.take(10))

## Identifying maximum temperature per year in descending order with respect to maximum temperature.
### Aggregating maximum temperature per year.
min_temperatures = year_temperature.reduceByKey(lambda a,b: a if a[0] <= b[0] else b)
### Sorting key-value-pairs by decreasing values.
min_temperatures = min_temperatures.sortBy(keyfunc = lambda elem: elem[1][0], ascending = False)
### Printing ordered maximum temperatures per year.
print("\nMinimum temperature per year (year, (temperature, station nr)) in descending order with respect to maximum temperature:\n")
print(min_temperatures.take(10))

# Closing Spark's execution environment.
sc.stop()

# Calculating running time..
end = time.time()
print("\nRunning time: " + str(end - start))
