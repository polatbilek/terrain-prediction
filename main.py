from readwrite import *
import pandas as pd
import matplotlib.pyplot as plt
from drawer import *
import os
import sys
import numpy as np

#
#  data object is a dict of terrain types
#  for each terrain type there is a list of walkers with 4 sensor data (lu, ru, ld, rd)
#  so each row is a person's list of sensor data (4 for perfect walk, if sensor missing it is empty list)
#  for example data["ls"][0] will be (4,N,3) shape. 4 sensor each has N data recorded on 3 axes.
#

path = "/home/darg2/Desktop/117E747"
ip = "192.168.4."

ls = []  # level-surface
ds = []  # downstairs
dh = []  # downhill
us = []  # upstairs
uh = []  # uphill

data = {"ls": ls, "ds": ds, "dh": dh, "us": us, "uh": uh}

file_ls = []  # level-surface
file_ds = []  # downstairs
file_dh = []  # downhill
file_us = []  # upstairs
file_uh = []  # uphill

filenames_of_data = {"ls": file_ls, "ds": file_ds, "dh": file_dh, "us": file_us, "uh": file_uh}

for walker in os.listdir(path):
	walker_data_filename = os.path.join(path, walker)

	sensor_walker1, sensor_walker2 = sensortxt_parser(os.path.join(walker_data_filename, "sensors.txt"))

	for person in [sensor_walker1, sensor_walker2]:
		for terrain in list(data.keys()):
			prefixes = [] #each prefix is a data run

			for data_file in os.listdir(walker_data_filename):
				if terrain in data_file:
					if len(prefixes) > 0: #if there is a data run is added already to data run list
						flag = True

						for data_run in prefixes: #loop through data run names
							if str(data_file.strip().split(terrain)[0]) == data_run: # if you find match, don't add
								flag = False

						if flag: #if you didn't find any match in list, then this is a new run
							prefixes.append(str(data_file.strip().split(terrain)[0]))

					else:
						prefixes.append(str(data_file.strip().split(terrain)[0]))

			for prefix in prefixes:
				one_person_run_data = []
				filenames = []

				for sensor in list(person.keys()):
					if(person[sensor] != 'x'):
						data_filename = prefix + terrain + "." + ip + str(40 + person[sensor]) + ".dat"

						absolute_path = os.path.join(walker_data_filename, data_filename)

						one_person_one_sensor_data = get_data(absolute_path)

						if one_person_one_sensor_data != 0:
							one_person_run_data.append(one_person_one_sensor_data)
							filenames.append(data_filename)
						else:
							one_person_run_data.append([])
							filenames.append("")

					else:
						one_person_run_data.append([])
						filenames.append("")

				temp = data[terrain]
				temp.append(one_person_run_data)
				data[terrain] = temp

				temp = filenames_of_data[terrain]
				temp.append(filenames)
				filenames_of_data[terrain] = temp


for i in range(8):
	#for j in range(4):
	if len(data["ls"][i][0]) != 0 and len(data["ls"][i][1]) != 0:
		#s = np.std(data["ls"][i][j])
		#m = np.mean(data["ls"][i][j])
		#print("User: " + str(i) + ", Sensor: " + str(j) + "\nmean: " + str(m) + ", std: " + str(s))
		pd_data = pd.DataFrame(data["ls"][i][0])

		plt.title(filenames_of_data["ls"][i][0] + " Walker: " + str(i) + ", Sensor: " + str(0))
		plt.plot(pd_data[1])
		plt.show()

		pd_data = pd.DataFrame(data["ls"][i][1])

		plt.title(filenames_of_data["ls"][i][0] + " Walker: " + str(i) + ", Sensor: " + str(1))
		plt.plot(pd_data[1])
		plt.show()

