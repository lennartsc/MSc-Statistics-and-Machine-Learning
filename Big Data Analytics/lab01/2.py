from pyspark import SparkContext

# Setting up Spark's execution environment.
sc = SparkContext(appName = "assignment2")

# Creating RDD.
temperature_file = sc.textFile("/user/x_lensc/data/temperature-readings.csv")

# Splitting lines.
lines = temperature_file.map(lambda line: line.split(";"))

# Using all readings.

## Extracting year-month(key) and temperature(value).
year_month_temperature = lines.map(lambda x: (x[1][0:7], float(x[3])))
## Filtering for period 1950-2014 and temperatures larger 10 degrees.
year_month_temperature = year_month_temperature.filter(lambda x: int(x[0][0:4]) in range(1950, 2015) and x[1] > 10)
## Mapping count of 1 to each filtered reading.
year_month_counts = year_month_temperature.map(lambda x: (x[0], 1))
## Adding up counts for each key(year-month)
year_month_counts = year_month_counts.reduceByKey(lambda x,y: x+y)
## Printing result.
print("\nExtract of results using all readings:\n")
print(year_month_counts.take(10))

# Using only distinct readings.

## Extracting year-month(key) and temperature, station number (value).
year_month_temperature = lines.map(lambda x: (x[1][0:7], (float(x[3]), x[0])))
## Filtering for period 1950-2014 and temperatures larger 10 degrees.
year_month_temperature = year_month_temperature.filter(lambda x: int(x[0][0:4]) in range(1950, 2015) and x[1][0] > 10)
## Mapping count of 1 to each filtered reading and keeping distinct pairs.
year_month_counts = year_month_temperature.map(lambda x: (x[0], (x[1][1], 1))).distinct()
## Extracting year-month(key) and count(value).
year_month_counts = year_month_counts.map(lambda x: (x[0], x[1][1]))
## Adding up counts for each key(year-month)
year_month_counts = year_month_counts.reduceByKey(lambda x,y: x+y)
## Printing result.
print("\nExtract of results using distinct readings:\n")
print(year_month_counts.take(10))

# Closing Spark's execution environment.
sc.stop()
