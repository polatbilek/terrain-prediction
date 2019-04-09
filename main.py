from readwrite import *
import pandas as pd
import matplotlib.pyplot as plt
from drawer import *
import os
import sys
import numpy as np
import features
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.decomposition import PCA

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



train = []
test = []
train_label = [] #ds 1    us 0  total 17
test_label = []

for i in range(10):

	if len(data['ds'][i][1]) != 0:
		if len(data['ds'][i][3]) != 0:
			train.append([features.run("all", data['ds'][i][1], 50, 300), features.run("all", data['ds'][i][3], 50, 300)])
			train_label.append(1)

	if len(data['us'][i][1]) != 0:
		if len(data['us'][i][3]) != 0:
			train.append([features.run("all", data['us'][i][1], 50, 300), features.run("all", data['us'][i][3], 50, 300)])
			train_label.append(0)


for j in range(7):
	i = 10+j

	if len(data['ds'][i][1]) != 0:
		if len(data['ds'][i][3]) != 0:
			test.append([features.run("all", data['ds'][i][1], 50, 300), features.run("all", data['ds'][i][3], 50, 300)])
			test_label.append(1)

	if len(data['us'][i][1]) != 0:
		if len(data['us'][i][3]) != 0:
			test.append([features.run("all", data['us'][i][1], 50, 300), features.run("all", data['us'][i][3], 50, 300)])
			test_label.append(0)





'''
pca = PCA(n_components=100)
pca.fit(train)
train = pca.transform(train)
test = pca.transform(test)
'''


train = np.reshape(np.asarray(train), (len(train), 21*6*2))
test = np.reshape(np.asarray(test), (len(test), 21*6*2))

print("SVM training started...")
svm = SVC(kernel='linear')
svm.fit(np.asarray(train), np.asarray(train_label))

print("SVM prediction started...")
predictions = svm.predict(np.asarray(test))
accuracy = accuracy_score(test_label, predictions)
print(accuracy)
#feature_vector = features.run("all", data['ls'][0][0], 50, 10000)


'''
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
'''
