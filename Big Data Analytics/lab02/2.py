from pyspark import SparkContext
from pyspark.sql import SQLContext, Row
from pyspark.sql import functions as F

# Setting up Spark's execution environment.
sc = SparkContext(appName = "BDA2_assignment2")
sqlContext= SQLContext(sc)

# Creating RDD.
temperature_file = sc.textFile("/user/x_lensc/data/temperature-readings.csv")

# Splitting lines.
lines = temperature_file.map(lambda line: line.split(";"))

# Creating DataFrame with columns year-month-day, station number and temperature.
station_daily_all_rdd = lines.map(lambda x: Row(year = x[1][0:4], month = x[1][5:7], station_nr = x[0], temperature = float(x[3])))
station_daily_all_df = sqlContext.createDataFrame(station_daily_all_rdd)
station_daily_all_df.registerTempTable("station_daily_all_rdd")

# Filtering for period 1950-2014 and temperatures larger 10 degrees using SQL-like queries.
station_daily_all_df = sqlContext.sql("SELECT * FROM station_daily_all_rdd WHERE year >= 1950 AND year <= 2014 AND temperature >= 10")

# Using all readings.
## Counting.
year_month_counts_all = station_daily_all_df.groupBy(
    "year", "month").agg(F.count("temperature").alias("count"))
## Ordering by value DESC.
year_month_counts_all = year_month_counts_all.orderBy(["count"], ascending = [0])
## Printing result.
print("\nExtract of results using all readings:\n")
print(year_month_counts_all.show(10))

# Using only distinct readings.
## Keeping one entry per station and month.
station_monthly_distinct_df = station_daily_all_df.select("station_nr", "year", "month").distinct()
## Counting.
station_monthly_distinct_df = station_monthly_distinct_df.groupBy(
    "year", "month").agg(F.count("station_nr").alias("count"))
## Ordering by value DESC.
station_monthly_distinct_df = station_monthly_distinct_df.orderBy(["count"], ascending = [0])
## Printing result.
print("\nExtract of results using distinct readings:\n")
print(station_monthly_distinct_df.show(10))

# Closing Spark's execution environment.
sc.stop()
