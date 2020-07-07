from pyspark import SparkContext

# Setting up Spark's execution environment.
sc = SparkContext(appName = "assignment4")

# Identifying maximum temperature per station.
## Creating RDD.
temperature_file = sc.textFile("/user/x_lensc/data/temperature-readings.csv")
## Splitting lines.
lines = temperature_file.map(lambda line: line.split(";"))
## Extracting station number (key) and temperature (value).
station_temp_all = lines.map(lambda x: (x[0], float(x[3])))
## Aggregating maximum temperature per station.
station_temp_max = station_temp_all.reduceByKey(lambda a,b: a if a > b else b)

# Identifying maximum daily precipitation per station.
## Creating RDD.
precipitation_file = sc.textFile("/user/x_lensc/data/precipitation-readings.csv")
## Splitting lines.
lines = precipitation_file.map(lambda line: line.split(";"))
## Extracting station number (key) and precipitation (value).
station_precip_all = lines.map(lambda x: (x[0], float(x[3])))
## Aggregating maximum daily precipitation per station.
station_precip_max = station_precip_all.reduceByKey(lambda a,b: a if a > b else b)

# Joining maximum temperature and maximum daily precipitation per station.
station_temp_precip_max = station_temp_max.join(station_precip_max)

# Filtering stations related to maximum temperature and maximum precipitation.
station_temp_precip_max = station_temp_precip_max.filter(lambda x: x[1][0] >= 25 and x[1][0] <= 30)
station_temp_precip_max = station_temp_precip_max.filter(lambda x: x[1][1] >= 100 and x[1][1] <= 200)

# Printing result.
print("Result shown as follows: station number, (maximum temperature, maximum daily precipitation)\n")
print(station_temp_precip_max.collect())

# Closing Spark's execution environment.
sc.stop()
