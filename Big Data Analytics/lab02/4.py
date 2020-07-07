from pyspark import SparkContext
from pyspark.sql import SQLContext, Row
from pyspark.sql import functions as F

# Setting up Spark's execution environment.
sc = SparkContext(appName = "BDA2_assignment4")
sqlContext= SQLContext(sc)

# Identifying maximum temperature per station.
## Creating RDD.
temperature_file = sc.textFile("/user/x_lensc/data/temperature-readings.csv")
## Splitting lines.
lines = temperature_file.map(lambda line: line.split(";"))
## Creating DataFrame with columns station_nr and temperature.
temp_station_all_rdd = lines.map(lambda x: Row(station_nr = x[0], temperature = float(x[3])))
temp_station_all_df = sqlContext.createDataFrame(temp_station_all_rdd)
temp_station_all_df.registerTempTable("temp_station_all_rdd")
## Aggregating maximum temperature per station.
temp_station_max_df = temp_station_all_df.groupBy("station_nr").agg(
    F.max("temperature").alias("temperature_max"))

# Identifying maximum daily precipitation per station.
## Creating RDD.
precipitation_file = sc.textFile("/user/x_lensc/data/precipitation-readings.csv")
## Splitting lines.
lines = precipitation_file.map(lambda line: line.split(";"))
## Creating DataFrame with columns station_nr and precipitation.
precip_station_all_rdd = lines.map(lambda x: Row(precip_station_nr = x[0], precipitation = float(x[3])))
precip_station_all_df = sqlContext.createDataFrame(precip_station_all_rdd)
precip_station_all_df.registerTempTable("precip_station_all_rdd")
## Aggregating maximum daily precipitation per station.
precip_station_max_df = precip_station_all_df.groupBy("precip_station_nr").agg(
    F.max("precipitation").alias("precipitation_max"))

# Joining maximum temperature and maximum daily precipitation per station.
temp_precip_station_max_df = temp_station_max_df.join(precip_station_max_df,
                                                     temp_station_max_df["station_nr"] ==
                                                      precip_station_max_df["precip_station_nr"]).select(
    "station_nr", "temperature_max","precipitation_max")

# Filtering stations related to maximum temperature and maximum precipitation.
temp_precip_station_max_df = temp_precip_station_max_df.filter(temp_precip_station_max_df["temperature_max"] >= 25)
temp_precip_station_max_df = temp_precip_station_max_df.filter(temp_precip_station_max_df["temperature_max"] <= 25)
temp_precip_station_max_df = temp_precip_station_max_df.filter(temp_precip_station_max_df["precipitation_max"] >= 100)
temp_precip_station_max_df = temp_precip_station_max_df.filter(temp_precip_station_max_df["precipitation_max"] <= 200)

# Printing result.
print("Extract of the result:\n")
print(temp_precip_station_max_df.show(10))

# Closing Spark's execution environment.
sc.stop()
