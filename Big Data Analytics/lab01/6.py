from pyspark import SparkContext

# Setting up Spark's execution environment.
sc = SparkContext(appName = "assignment6")

# Creating RDD.
temperature_file = sc.textFile("/user/x_lensc/data/temperature-readings.csv")

# Splitting lines.
lines = temperature_file.map(lambda line: line.split(";"))

# Calculating monthly average temperature per station 1950-2014.
## Extracting year-month-day, station number (key) and temperature (value).
station_daily_all = lines.map(lambda x: ((x[1], x[0]), float(x[3])))
## Filtering for period 1950-2014.
station_daily_all = station_daily_all.filter(lambda x: int(x[0][0][0:4]) in range(1950, 2015))
## Aggregating maximum temperature per day and station.
station_daily_max = station_daily_all.reduceByKey(lambda a,b: a if a > b else b)
## Aggregating minimum temperature per day and station.
station_daily_min = station_daily_all.reduceByKey(lambda a,b: a if a < b else b)
## Unioning maximum and minimum daily temperatures per station.
station_daily_minmax = station_daily_max.union(station_daily_min)
## Extracting year-month, station number (key) and daily min and max temperatures (value).
station_monthly_minmax = station_daily_minmax.map(lambda x: ((x[0][0][0:7], x[0][1]), x[1]))
## Aggregating average monthly temperature per station.
station_monthly_avg = station_monthly_minmax.reduceByKey(lambda a,b: (a+b)/2)

# Calculating average temperature over all stations for a specific year and month 1950-2014.
monthly_avg = station_monthly_avg.map(lambda x: (x[0][0], (x[1], 1)))
monthly_avg = monthly_avg.reduceByKey(lambda a,b: a+b)
monthly_avg = monthly_avg.map(lambda x: (x[0], (x[1][0])/x[1][1]))

# Calculating long-term monthly averages in the period of 1950-1980.
## Filtering for period 1950-1980.
monthly_avg_longterm = monthly_avg.filter(lambda x: (int(x[0][0:4]) in range(1950, 1981)))
## Setting month as key and average temperature and counter as value.
monthly_avg_longterm = monthly_avg_longterm.map(lambda x: (x[0][5:7], (x[1], 1)))
## Calculating monthly averages.
monthly_avg_longterm = monthly_avg_longterm.reduceByKey(lambda x,y: x+y)
monthly_avg_longterm = monthly_avg_longterm.map(lambda x: (x[0], (x[1][0])/x[1][1]))

# Adjusting monthly_avg by adding differnces to long-term averages.
## Preparing monthly_avg for join with monthly_avg_longterm.
monthly_avg = monthly_avg.map(lambda x: (x[0][5:7], (x[0], x[1])))
## Joining monthly_avg with monthly_avg_longterm.
monthly_avg = monthly_avg.join(monthly_avg_longterm)
## Remapping monthly_avg to format: year-month, (average, difference to long-term-average).
monthly_avg = monthly_avg.map(lambda x: (x[1][0][0], x[1][0][1], x[1][0][1]-x[1][1]))

# Printing results.
## Long-term monthly averages 1950-1980.
print("Identified long-term monthly averages in the period of 1950-1980:\n")
print(monthly_avg_longterm.collect())
## Monthly averages 1950-2014 compared to long-term monthly averages.
print("\nExtract of identified monthly averages in the period of 1950-2014 with differences to long-term monthly averages.")
print("Format: (year-month, average, difference to long-term average):\n")
print(monthly_avg.take(10))

# Storing results.
monthly_avg.repartition(1).saveAsTextFile("result_assignment6")

# Closing Spark's execution environment.
sc.stop()
