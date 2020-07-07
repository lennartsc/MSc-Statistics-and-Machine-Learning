from pyspark import SparkContext
from pyspark.sql import SQLContext, Row
from pyspark.sql import functions as F

# Setting up Spark's execution environment.
sc = SparkContext(appName = "BDA2_assignment5")
sqlContext= SQLContext(sc)

# Extracting Ostergotland stations.
## Creating RDD.
stations_rdd = sc.textFile("/user/x_lensc/data/stations-Ostergotland.csv")
## Splitting lines.
stations_rdd = stations_rdd.map(lambda line: line.split(";"))
## Creating DataFrame with column station_nr.
stations_rdd = stations_rdd.map(lambda x: Row(ostergotland_station_nr = x[0]))
stations_df = sqlContext.createDataFrame(stations_rdd)

# Filtering precipitation data only for Ostergotland stations.
## Creating RDD.
precip_rdd = sc.textFile("/user/x_lensc/data/precipitation-readings.csv")
## Splitting lines.
precip_rdd = precip_rdd.map(lambda line: line.split(";"))
## Creating DataFrame with column station_nr.
precip_rdd = precip_rdd.map(lambda x: Row(station_nr = x[0], year = int(x[1][0:4]), month = x[1][5:7], precip = float(x[3])))
precip_df = sqlContext.createDataFrame(precip_rdd)
## Filtering for period 1993-2016.
precip_df = precip_df.filter(precip_df["year"] >= 1993)
precip_df = precip_df.filter(precip_df["year"] <= 2016)
## Joining precipitation data with stations_df to keep only data for Ostergotland stations.
precip_df = precip_df.join(stations_df,
                           precip_df["station_nr"] == stations_df["ostergotland_station_nr"]).select(
    "station_nr", "year", "month", "precip")

# Extracting average monthly precipitation over all stations.
## Extracting total monthly precipitation for each station.
precip_df = precip_df.groupBy(
    "year", "month", "station_nr").agg(F.sum('precip').alias("precipitation_sum"))
# Extracting average monthly precipitation over all stations.
precip_df = precip_df.groupBy(
    "year", "month").agg(F.avg('precipitation_sum').alias("precipitation_avg"))

# Ordering df BY year DESC, month DESC.
precip_df = precip_df.orderBy(['year', 'month'], ascending=[0,0])

# Printing result.
print("Extract of result shown as follows: year-month, average precipitation\n")
print(precip_df.show(10))

# Closing Spark's execution environment.
sc.stop()
