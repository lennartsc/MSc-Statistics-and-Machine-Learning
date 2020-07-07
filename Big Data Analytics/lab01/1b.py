import time
import operator
import sys

# Storing starting time.
start = time.time()

# Initializing empty dictionaries.
res_max = {}
res_min = {}

# Extracting file path from user-specified input.
if sys.argv[1] == "temperature-readings.csv":
    file_path = "../../hadoop_examples/shared_data/temperature-readings.csv"
elif sys.argv[1] == "temperatures-big.csv":
    file_path = "../../hadoop_examples/shared_data/temperatures-big.csv"
else:
    print("SPECIFIED FILE DOES NOT EXIST.")

# Filling dictionaries.
with open(file_path) as file:

    for line in file:

        # Splitting line.
        line_splitted = line.split(";")

        # Skipping line if year not in desired period.
        if not float(line_splitted[1][0:4]) in range(1950, 2015):
            continue

        # Updating res_max.
        ## Initializing value (temperature, station_nr) for year if year entry does not exist yet.
        if not line_splitted[1][0:4] in res_max:
            res_max[line_splitted[1][0:4]] = [float(line_splitted[3]), line_splitted[0]]
        ## Updating value (temperature, station_nr) for year if year entry already exists.
        elif float(line_splitted[3]) > res_max[line_splitted[1][0:4]][0]:
            res_max[line_splitted[1][0:4]][0] = float(line_splitted[3])

        # Updating res_min.
        ## Initializing value (temperature, station_nr) for year if year entry does not exist yet.
        if not line_splitted[1][0:4] in res_min:
            res_min[line_splitted[1][0:4]] = [float(line_splitted[3]), line_splitted[0]]
        ## Updating value (temperature, station_nr) for year if year entry already exists.
        elif float(line_splitted[3]) < res_min[line_splitted[1][0:4]][0]:
            res_min[line_splitted[1][0:4]][0] = float(line_splitted[3])

# Sorting results.
## Sorting res_max.
res_max = sorted(res_max.items(), key = operator.itemgetter(1))
res_max.reverse()
## Sorting res_min.
res_min = sorted(res_min.items(), key = operator.itemgetter(1))
res_min.reverse()

# Printing results.
print("Extract of results for data:" + sys.argv[1])
## Printing res_max.
print("\nMaximum temperature per year (including station number) in descending order with respect to maximum temperature:\n")
print(res_max[0:11])
## Printing res_min.
print("\nMinimum temperature per year (including station number) in descending order with respect to maximum temperature:\n")
print(res_min[0:11])

# Calculating running time..
end = time.time()
print("Running time: " + str(end - start))
