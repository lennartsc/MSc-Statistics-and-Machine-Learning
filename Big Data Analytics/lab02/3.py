from pyspark import SparkContext
from pyspark.sql import SQLContext, Row
from pyspark.sql import functions as F

# Setting up Spark's execution environment.
sc = SparkContext(appName = "BDA2_assignment3")
sqlContext= SQLContext(sc)

# Creating RDD.
temperature_file = sc.textFile("/user/x_lensc/data/temperature-readings.csv")

# Splitting lines.
lines = temperature_file.map(lambda line: line.split(";"))

# Creating DataFrame with columns date, station number and temperature.
station_daily_all_rdd = lines.map(lambda x: Row(year = x[1][0:4], month = x[1][5:7], day = x[1][8:10], station_nr = x[0], temperature = float(x[3])))
station_daily_all_df = sqlContext.createDataFrame(station_daily_all_rdd)
station_daily_all_df.registerTempTable("station_daily_all_rdd")

# Filtering for period 1960-2014.
station_daily_all_df = station_daily_all_df.filter(station_daily_all_df["year"] >= 1960)
station_daily_all_df = station_daily_all_df.filter(station_daily_all_df["year"] <= 2014)

# Aggregating maximum temperature per day and station.
station_daily_max_df = station_daily_all_df.groupBy("station_nr", "year", "month", "day").agg(
    F.max("temperature").alias("temperature"))

# Aggregating minimum temperature per day and station.
station_daily_min_df = station_daily_all_df.groupBy("station_nr", "year", "month", "day").agg(
    F.min("temperature").alias("temperature"))

# Unioning maximum and minimum daily temperatures per station.
station_daily_minmax_df = station_daily_max_df.unionAll(station_daily_min_df)

# Aggregating average monthly temperature per station.
station_monthly_avg_df = station_daily_minmax_df.groupBy("station_nr", "year", "month").agg(
    F.avg("temperature").alias("temperature_avg"))

# Ordering dataFrame by avgMonthlyTemperature DESC
station_monthly_avg_df = station_monthly_avg_df.orderBy(["temperature_avg"], ascending=[0])

# Printing extract of results.
print(station_monthly_avg_df.show(10))

# Closing Spark's execution environment.
sc.stop()
