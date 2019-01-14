import os



######################################
#
# This method reads and returns the sensor data
# selection_type indicates how much or which type of data you want
# "one" = returns only indicated specific data
# TODO: Other types of selections, like only uphill, only 1 person, whole data ... etc

def get_data(path, selection_type="one"):
    if selection_type == "one":
        file_handler = open(path, "r")

        data = []

        for line in file_handler:
            values = line.strip().split(" ")
            data.append([int(values[1]), int(values[2]), int(values[3])])

        return data