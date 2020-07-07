from pyspark import SparkContext
from pyspark.sql import SQLContext, Row
from pyspark.sql import functions as F

# Setting up Spark's execution environment.
sc = SparkContext(appName = "BDA2_assignment6")
sqlContext= SQLContext(sc)

# Creating RDD.
temperature_file = sc.textFile("/user/x_lensc/data/temperature-readings.csv")

# Splitting lines.
lines = temperature_file.map(lambda line: line.split(";"))

# Creating DataFrame with columns year-month-day, station number and temperature.
station_daily_all_rdd = lines.map(lambda x: Row(year_month_day = x[1], station_nr = x[0], temperature = float(x[3])))
station_daily_all_df = sqlContext.createDataFrame(station_daily_all_rdd)
station_daily_all_df.registerTempTable("station_daily_all_rdd")

# Calculating monthly average temperature per station 1950-2014.
## Filtering for period 1950-2014.
station_daily_all_df = station_daily_all_df.filter(station_daily_all_df["year_month_day"][0:4] >= 1950)
station_daily_all_df = station_daily_all_df.filter(station_daily_all_df["year_month_day"][0:4] <= 2014)
## Aggregating maximum and minimum temperature per day and station.
station_daily_max_df = station_daily_all_df.groupBy(
    "year_month_day", "station_nr").agg(F.max('temperature').alias("temperature"))
station_daily_min_df = station_daily_all_df.groupBy(
    "year_month_day", "station_nr").agg(F.min('temperature').alias("temperature"))
## Unioning DataFrames.
station_daily_min_max_df = station_daily_max_df.unionAll(station_daily_min_df)
## Aggregating average monthly temperature per station.
station_monthly_avg_df = station_daily_min_max_df.groupBy(
    station_daily_min_max_df["year_month_day"][0:7].alias("year_month"),
    "station_nr").agg(F.avg("temperature").alias("temperature_avg"))

# Calculating average temperature over all stations for a specific year and month 1950-2014
monthly_avg_df = station_monthly_avg_df.groupBy("year_month").agg(F.avg("temperature_avg").alias("temperature_avg"))

# Calculating long-term monthly averages in the period of 1950-1980.
## Filtering for period 1950-1980.
monthly_avg_longterm_df = monthly_avg_df.filter(monthly_avg_df["year_month"][0:4] >= 1950)
monthly_avg_longterm_df = monthly_avg_df.filter(monthly_avg_df["year_month"][0:4] <= 1980)
## Calculating monthly averages.
monthly_avg_longterm_df = monthly_avg_longterm_df.groupBy(
    monthly_avg_longterm_df["year_month"][6:7].alias("month")).agg(F.avg("temperature_avg").alias("temperature_avg_longterm"))

# Adjusting monthly_avg_df by adding long-term averages.
monthly_avg_df = monthly_avg_df.join(monthly_avg_longterm_df,
                                     monthly_avg_df["year_month"][6:7] == monthly_avg_longterm_df["month"])

# Calculating difference and selecting columns year, month, difference.
monthly_avg_df = monthly_avg_df.select(monthly_avg_df["year_month"][0:4].alias("year"),
                                       monthly_avg_df["year_month"][6:7].alias("month"),
                                       (monthly_avg_df["temperature_avg"] - monthly_avg_df["temperature_avg_longterm"]).alias("difference"))

# Ordering dataFrame by year DESC, month DESC.
monthly_avg_df = monthly_avg_df.orderBy(['year', 'month'], ascending=[0,0])

# Printing extract of results.
print(monthly_avg_df.show(10))

# Storing results.
monthly_avg_df.rdd.repartition(1).saveAsTextFile("bda2_result_assignment6")

# Closing Spark's execution environment.
sc.stop()
