from pyspark import SparkContext

# Setting up Spark's execution environment.
sc = SparkContext(appName = "bda1_assignment5")

# Extracting Ostergotland stations and broadcasting RDD to all nodes.
## Creating RDD.
stations_file = sc.textFile("/user/x_lensc/data/stations-Ostergotland.csv")
## Splitting lines.
stations_file = stations_file.map(lambda line: line.split(";"))
## Extracting station number (key) and temperature (value).
stations = stations_file.map(lambda x: (x[0]))
## Broadcasting stations data to each node (accessable over attribute 'value').
stations = stations.collect()
stations = sc.broadcast(stations)

# Filtering precipitation data only for Ostergotland stations.
## Creating RDD.
precip_file = sc.textFile("/user/x_lensc/data/precipitation-readings.csv")
## Splitting lines.
precip_file = precip_file.map(lambda line: line.split(";"))
## Filering data for Ostergotland stations.
stations_precip = precip_file.filter(lambda x: x[0] in stations.value)

# Calculating average monthly precipitation over all stations.
## Extracting total monthly precipitation for each station.
stations_monthly_precip = stations_precip.map(lambda x: ((x[0], x[1][0:7]), float(x[3])))
stations_monthly_precip = stations_monthly_precip.reduceByKey(lambda a,b: a+b)

# Extracting average monthly precipitation over all stations.
avg_monthly_precip = stations_monthly_precip.map(lambda x: (x[0][1], (x[1], 1)))
avg_monthly_precip = avg_monthly_precip.reduceByKey(lambda a,b: a+b)
avg_monthly_precip = avg_monthly_precip.map(lambda x: (x[0], (x[1][0])/x[1][1]))

# Printing result.
print("Extract of result shown as follows: year-month, average precipitation\n")
print(stations_monthly_precip.take(10))

# Closing Spark's execution environment.
sc.stop()
