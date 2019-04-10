from readwrite import *
from drawer import *
import os
import sys
import numpy as np
import features
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import random
from sklearn.decomposition import PCA


#
#  data object is a dict of terrain types
#  for each terrain type there is a list of walkers with 4 sensor data (lu, ru, ld, rd)
#  so each row is a person's list of sensor data (4 for perfect walk, if sensor missing it is empty list)
#  for example data["ls"][0] will be (4,N,3) shape. 4 sensor each has N data recorded on 3 axes.
#

def organise_data(path, ip):
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
				prefixes = []  # each prefix is a data run

				for data_file in os.listdir(walker_data_filename):
					if terrain in data_file:
						if len(prefixes) > 0:  # if there is a data run is added already to data run list
							flag = True

							for data_run in prefixes:  # loop through data run names
								if str(data_file.strip().split(terrain)[0]) == data_run:  # if you find match, don't add
									flag = False

							if flag:  # if you didn't find any match in list, then this is a new run
								prefixes.append(str(data_file.strip().split(terrain)[0]))

						else:
							prefixes.append(str(data_file.strip().split(terrain)[0]))

				for prefix in prefixes:
					one_person_run_data = []
					filenames = []

					for sensor in list(person.keys()):
						if (person[sensor] != 'x'):
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

	return data, filenames_of_data



def k_fold(data, K, threshold = 0, first_N = 300, window_size = 50, with_pca=False, n_components=20):
	test_split_rate = 1 / K
	accuracies = []

	ds = data['ds']
	us = data['us']
	random.shuffle(ds)
	random.shuffle(us)
	data['ds'] = ds
	data['us'] = us

	total_set = []
	total_label = []

	flag_f1 = False
	flag_f2 = False

	for i in range(1000): #tries to add all data from all classes, if all flags are true, that means all data collected

		try:
			if len(data['ds'][i][1]) > threshold:
				if len(data['ds'][i][3]) > threshold:
					total_set.append([features.run("all", data['ds'][i][1], window_size, first_N),
									  features.run("all", data['ds'][i][3], window_size, first_N)])
					total_label.append(1)
		except:
			flag_f1 = True

		try:
			if len(data['us'][i][1]) > threshold:
				if len(data['us'][i][3]) > threshold:
					total_set.append([features.run("all", data['us'][i][1], window_size, first_N),
									  features.run("all", data['us'][i][3], window_size, first_N)])
					total_label.append(0)
		except:
			flag_f2 = True

		if flag_f1 and flag_f2:
			break



	for i in range(K):

		if i+1 == K: #when i is the last index, test split is not taking from middle, no need for 2 concatenation in train
			train = total_set[:int(i * test_split_rate * len(total_set))]
			train_label = total_label[:int(i * test_split_rate * len(total_set))]

			test = total_set[int(i * test_split_rate * len(total_set)):]
			test_label = total_label[int(i * test_split_rate * len(total_set)):]

		else: #means that test split is taken from middle or from end of the list which creates no problem
			train = total_set[:int(i * test_split_rate * len(total_set))] + \
					total_set[int((i+1) * test_split_rate * len(total_set)):]

			train_label = total_label[:int(i * test_split_rate * len(total_set))] + \
						  total_label[int((i+1) * test_split_rate * len(total_set)):]


			test = total_set[int(i*test_split_rate*len(total_set)):int((i+1)*test_split_rate*len(total_set))]
			test_label = total_label[int(i*test_split_rate*len(total_set)):int((i+1)*test_split_rate*len(total_set))]


		#flattens data automaticcaly for all data point
		train = np.reshape(np.asarray(train), (len(train), len(train[0]) * len(train[0][0]) * len(train[0][0][0])))
		test = np.reshape(np.asarray(test), (len(test), len(test[0]) * len(test[0][0]) * len(test[0][0][0])))


		if with_pca:
			pca = PCA(n_components=n_components, svd_solver= "arpack")
			pca.fit(train)
			train = pca.transform(train)
			test = pca.transform(test)


		print("SVM training started...")
		svm = SVC(kernel='linear')
		svm.fit(np.asarray(train), np.asarray(train_label))

		print("SVM prediction started...")
		predictions = svm.predict(np.asarray(test))
		accuracy = accuracy_score(test_label, predictions)
		accuracies.append(accuracy)


	print("Accuracies: ",end='')
	print(accuracies)
	print("Average accuracy: ", end='')
	print(sum(accuracies)/len(accuracies))
	print("Train split size: " + str(len(train)))
	print("Test split size: " + str(len(test)))

	return accuracies



def single_run(data, split_rate, threshold=0, first_N=300, window_size=50, with_pca=False, n_components=20):

		ds = data['ds']
		us = data['us']
		random.shuffle(ds)
		random.shuffle(us)
		data['ds'] = ds
		data['us'] = us

		total_set = []
		total_label = []

		flag_f1 = False
		flag_f2 = False

		for i in range(1000):

			try:
				if len(data['ds'][i][1]) > threshold:
					if len(data['ds'][i][3]) > threshold:
						total_set.append([features.run("all", data['ds'][i][1], window_size, first_N),
										  features.run("all", data['ds'][i][3], window_size, first_N)])
						total_label.append(1)
			except:
				flag_f1 = True

			try:
				if len(data['us'][i][1]) > threshold:
					if len(data['us'][i][3]) > threshold:
						total_set.append([features.run("all", data['us'][i][1], window_size, first_N),
										  features.run("all", data['us'][i][3], window_size, first_N)])
						total_label.append(0)
			except:
				flag_f2 = True

			if flag_f1 and flag_f2:
				break


		#train and test split
		train = total_set[:int(split_rate * len(total_set))]
		train_label = total_label[:int(split_rate * len(total_set))]
		test = total_set[int(split_rate * len(total_set)):]
		test_label = total_label[int(split_rate * len(total_set)):]

		# flattens data automaticcaly for all data point
		train = np.reshape(np.asarray(train), (len(train), len(train[0]) * len(train[0][0]) * len(train[0][0][0])))
		test = np.reshape(np.asarray(test), (len(test), len(test[0]) * len(test[0][0]) * len(test[0][0][0])))

		if with_pca:
			pca = PCA(n_components=n_components, svd_solver="arpack")
			pca.fit(train)
			train = pca.transform(train)
			test = pca.transform(test)

		print("SVM training started...")
		svm = SVC(kernel='linear')
		svm.fit(np.asarray(train), np.asarray(train_label))

		print("SVM prediction started...")
		predictions = svm.predict(np.asarray(test))
		accuracy = accuracy_score(test_label, predictions)
		print(accuracy)
		print("Train split size: " + str(len(train)))
		print("Test split size: " + str(len(test)))


