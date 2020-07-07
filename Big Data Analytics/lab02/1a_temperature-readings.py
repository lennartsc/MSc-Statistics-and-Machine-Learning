from pyspark import SparkContext
from pyspark.sql import SQLContext, Row
from pyspark.sql import functions as F

# Setting up Spark's execution environment.
sc = SparkContext(appName = "BDA2_assignment1a_temperature-readings")
sqlContext= SQLContext(sc)

# Creating RDD.
temperature_file = sc.textFile("/user/x_lensc/data/temperature-readings.csv")

# Splitting lines.
lines = temperature_file.map(lambda line: line.split(";"))

# Creating DataFrame with columns year, station number and temperature.
station_daily_all_rdd = lines.map(lambda x: Row(year = x[1][0:4], station_nr = x[0], temperature = float(x[3])))
station_daily_all_df = sqlContext.createDataFrame(station_daily_all_rdd)
station_daily_all_df.registerTempTable("station_daily_all_rdd")

# Filtering for period 1950-2014.
station_daily_all_df = station_daily_all_df.filter(station_daily_all_df["year"] >= 1950)
station_daily_all_df = station_daily_all_df.filter(station_daily_all_df["year"] <= 2014)

# Identifying minimum temperature per year in descending order with respect to maximum temperature.
station_daily_min_df = station_daily_all_df.groupBy("year").agg(F.min(station_daily_all_df["temperature"]).alias("temperature"))
## Adding station_nr to station_daily_min_df.
station_daily_min_df = station_daily_min_df.join(station_daily_all_df, ["year", "temperature"])
## Ordering dataFrame by minValue DESC.
station_daily_min_df = station_daily_min_df.orderBy(["temperature"], ascending=[0])

# Identifying maximum temperature per year in descending order with respect to maximum temperature.
station_daily_max_df = station_daily_all_df.groupBy("year").agg(F.max(station_daily_all_df["temperature"]).alias("temperature"))
## Adding station_nr to station_daily_min_df.
station_daily_max_df = station_daily_max_df.join(station_daily_all_df, ["year", "temperature"])
## Ordering dataFrame by minValue DESC.
station_daily_max_df = station_daily_max_df.orderBy(["temperature"], ascending=[0])

# Printing results.
print("Extrat of results for data:" + "temperature-readings.csv:")
print("\nMaximum temperature per year:\n")
print(station_daily_max_df.show(10))

print("\Minimum temperature per year:\n")
print(station_daily_min_df.show(10))

sc.stop()
