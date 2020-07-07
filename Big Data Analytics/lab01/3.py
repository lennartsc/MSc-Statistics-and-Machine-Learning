from pyspark import SparkContext

# Setting up Spark's execution environment.
sc = SparkContext(appName = "assignment3")

# Creating RDD.
temperature_file = sc.textFile("/user/x_lensc/data/temperature-readings.csv")

# Splitting lines.
lines = temperature_file.map(lambda line: line.split(";"))

# Extracting year-month-day, station number (key) and temperature (value).
station_daily_all = lines.map(lambda x: ((x[1], x[0]), float(x[3])))

# Filtering for period 1960-2014.
station_daily_all = station_daily_all.filter(lambda x: int(x[0][0][0:4]) in range(1960, 2015))

# Aggregating maximum temperature per day and station.
station_daily_max = station_daily_all.reduceByKey(lambda a,b: a if a > b else b)

# Aggregating minimum temperature per day and station.
station_daily_min = station_daily_all.reduceByKey(lambda a,b: a if a < b else b)

# Unioning maximum and minimum daily temperatures per station.
station_daily_minmax = station_daily_max.union(station_daily_min)

# Extracting year-month, station number (key) and daily min and max temperatures (value).
station_monthly_minmax = station_daily_minmax.map(lambda x: ((x[0][0][0:7], x[0][1]), x[1]))

# Aggregating average monthly temperature per station.
station_monthly_avg = station_monthly_minmax.reduceByKey(lambda a,b: (a+b)/2)

# Printing results.
print("Extract of results:\n")
print(station_monthly_avg.take(25))

# Closing Spark's execution environment.
sc.stop()
