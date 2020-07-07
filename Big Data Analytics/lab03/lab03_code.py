from __future__ import division
from math import radians, cos, sin, asin, sqrt, exp
from datetime import datetime, timedelta
from pyspark import SparkContext
from collections import OrderedDict

# Defining haversine-function to calculate great circle distance between two points on earth.
def haversine(lon1, lat1, lon2, lat2):
    # Converting decimal degrees to radians.
    lon1, lati1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # Calculating distance in km using haversine formula.
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    km = 6367 * c
    # Returning distance in km.
    return km

# Setting up Spark's execution environment.
sc = SparkContext(appName="BDA3")

# Setting up input parameters.
h_distance = 100
h_date = 3
h_time = 2
lat_given = 58.4274
lon_given = 14.826
given_date = "2015-07-04"
start = datetime.strptime("04:00:00","%H:%M:%S")
given_time = [start + timedelta(hours=2*x) for x in range(0, 11)]

# Reading stations data and broadcasting it.
## Reading data.
stations = sc.textFile("/user/x_lensc/data/stations.csv")
stations = stations.map(lambda line: line.split(";"))
## Extracting station number (key) and longitude, latitude (value).
stations = stations.map(lambda x: (x[0], (x[3], x[4])))
## Broadcasting stations data to each node (accessable over attribute 'value').
stations = stations.collectAsMap()
stations = sc.broadcast(stations)

# Reading temperature data.
## Reading data.
temps = sc.textFile("/user/x_lensc/data/temperature-readings.csv")
temps = temps.map(lambda line: line.split(";"))
## Extracting station number (key) and date, time, temperature (value).
temps = temps.map(lambda x: (x[0], (x[1], x[2], float(x[3]))))

# Filtering temperature data related to given date
# (keep onlydata prior to date. Posterior data should not be considererd for the prediction.)
## Filtering data with date <= given date.
temps = temps.filter(lambda x: x[1][0] <= given_date)

# Adding longitute, latitude of stations to temperature data.
temps = temps.map(lambda x: (x[0], (stations.value.get(x[0], "-"), x[1])))
temps = temps.map(lambda x: (x[0], (x[1][0][0], x[1][0][1], x[1][1][0],
x[1][1][1], x[1][1][2])))

# Caching data.
temps = temps.cache()

# Implementing kernel function.
def gaussian_kernel(diff, h):
    return exp(-(diff / h) ** 2)
# Creating an emtpy dictionary

# Creating empty dictionaries to store predictions.
# Results for addition and multiplication of kernels will be stored.
predAddition = OrderedDict()
predMultiplication = OrderedDict()

for i in range(len(given_time)):

    # Remapping temperature data including distances for location, day and hour to
    # given location, given date and to each given time.
    # New format: station_nr, distance in km, distance in days, distance in hours, temperature.
    temp = temps.map(lambda x: (x[0], (haversine(lon_given,
    lat_given,float(x[1][1]), float(x[1][0])),
    (datetime.strptime(x[1][2], '%Y-%m-%d') -
    datetime.strptime(given_date,'%Y-%m-%d')).days,
    (datetime.strptime(x[1][3], '%H:%M:%S') -
    given_time[i]).seconds / 3600,
    x[1][4])))

    # Remapping using kernel function.
    # Key will be set to 0 for later aggregation.
    # New format: 0, kernel value for distance in km, kernel value for distance in days,
    # kernel value for distance in hours, temperature.
    # Storing new value in temp instead of temps because we need to use temps again.
    temp = temp.map(lambda x: (0, (gaussian_kernel(x[1][0],
    h_distance), gaussian_kernel(x[1][1], h_date),
    gaussian_kernel(x[1][2], h_time), x[1][3])))

    # Addition of kernels.

    ## Remapping.
    ## New format:
    ## (0, (distance kernel * temp + day kernel * temp + hour kernel * temp, sum of kernels))
    tempAdd = temp.map(lambda x: (x[0], (x[1][0] * x[1][3] + x[1][1]
    * x[1][3] + x[1][2] * x[1][3],
    x[1][0] + x[1][1] + x[1][2])))

    ## Aggregating by key (we implemented same key for every observation,
    ## so aggreagating over all observations.
    ## New format: (0, (sum of kernel values * temps, sum of kernel values))
    tempAdd = tempAdd.reduceByKey(lambda x, y: (x[0] + y[0], x[1] + y[1]))

    ## Remapping to extract result:
    ## Prediction = (sum of kernel values * temps) / sum of kernel values
    tempAdd = tempAdd.map(lambda x: x[1][0] / x[1][1])

    ## Storing predicted values.
    predAddition[given_time[i].strftime("%H:%M:%S")] = tempAdd.take(1)

    # Multiplication of kernels.

    ## Remapping.
    ## New format:
    ## (0, (distance kernel * day kernel * hour kernel * temp, product of kernels))
    tempMult = temp.map(lambda x: (x[0], (x[1][0] * x[1][1] * x[1][2] * x[1][3],
    x[1][0] * x[1][1] * x[1][2])))

    ## Aggregating by key (we implemented same key for every observation,
    ## so aggreagating over all observations.
    ## New format: (0, (sum of kernel values * temps, sum of kernel values))
    tempMult = tempMult.reduceByKey(lambda x, y: (x[0] + y[0], x[1] + y[1]))

    ## Remapping to extract result:
    ## Prediction = (sum of kernel values * temps) / sum of kernel values
    tempMult = tempMult.map(lambda x: x[1][0] / x[1][1])

    ## Storing predicted values.
    predMultiplication[given_time[i].strftime("%H:%M:%S")] = tempMult.take(1)


# Printing results.
print("Results for addition of kernels:\n")
print("Time | Predicted Temperature")
print("----------------------------------")
for key,value in predAddition.items() :
    print(key,' | ',round(value[0],2))

print("Results for multiplication of kernels:\n")
print("Time | Predicted Temperature")
print("----------------------------------")
for key,value in predMultiplication.items() :
    print(key,' | ',round(value[0],2))

# Closing spark enviorenment.
sc.stop()
