import os


######################################
#
# This method reads and returns the sensor data
# selection_type indicates how much or which type of data you want
# "one" = returns only indicated specific data

def get_data(path):
	try:
		file_handler = open(path, "r")
	except:
		return 0

	data = []

	for line in file_handler:
		values = line.strip().split(" ")
		data.append([int(values[1]), int(values[2]), int(values[3])])

	return data


def sensortxt_parser(path):
	order = ['lu', 'ru', 'lu', 'ru']
	order2 = ['ld', 'rd', 'ld', 'rd']
	dict1 = {}  # walker1
	dict2 = {}  # walker2

	with open(path, 'r') as f:
		c = 0
		for line in f:
			if c == 2:
				sensors = []
				for elem in line.strip().split("\t"):
					if elem == ' ':
						sensors.append("x")
					else:
						sensors.append(int(elem))

				if len(line.strip().split("\t")) == 3:
					sensors.append("x")

				for i in range(len(sensors)):
					if i > 1:
						dict2[order[i]] = sensors[i]
					else:
						dict1[order[i]] = sensors[i]

			if c == 3:
				sensors = []
				for elem in line.strip().split("\t"):
					if elem == ' ':
						sensors.append("x")
					else:
						sensors.append(int(elem))

				if len(line.strip().split("\t")) == 3:
					sensors.append("x")

				for i in range(len(sensors)):
					if i > 1:
						dict2[order2[i]] = sensors[i]
					else:
						dict1[order2[i]] = sensors[i]

			c += 1

	return dict1, dict2
