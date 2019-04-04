import numpy as np
import pandas as pd
import math
import sys

def slicer(data, T, first_N):
	new_data = []

	offset = 0
	for i in range(math.ceil(first_N/T)):
		partition = []
		c = 0

		while c != T:
			index = offset + c
			partition.append(data[index])
			c += 1

		new_data.append(partition)

		offset += T #not sliciding but rolling
		#offset += T//2 #sliding with half


	return new_data


def integrate(data):
	integrated = []

	for i in range(len(data)):
		slice = []

		for j in range(len(data[i])):
			slice.append(list(map(np.sum, data[i][0:j])))

		integrated.append(slice)

	return integrated


def mean(data, T, first_N):
	sliced_data = slicer(data, T, first_N)
	return list(map(np.mean, sliced_data))


def variance(data, T, first_N):
	sliced_data = slicer(data, T, first_N)
	return list(map(np.var, sliced_data))


def median(data, T, first_N):
	sliced_data = slicer(data, T, first_N)
	return list(map(np.median, sliced_data))


def averaged_velocity(data, T, first_N):
	sliced_data = slicer(data, T, first_N)
	velocity = integrate(sliced_data)

	return list(map(np.average, velocity))


def averaged_distance(data, T, first_N):
	velocity = averaged_velocity(data, T, first_N)
	distance = integrate(velocity)

	return list(map(np.average, distance))


def zero_crossing_rate(data, T, first_N):
	sliced_data = slicer(data, T, first_N)

	zcr = []

	for i in range(len(sliced_data)):
		counter = 0
		state = -1
		for j in range(len(sliced_data[i])):
			if state == -1:
				if sliced_data[i][j] >= 0:
					state == 1
					counter += 1

			else:
				if sliced_data[i][j] <= 0:
					state = -1
					counter += 1

		zcr.append(counter)

	return zcr


def pairwise_correlation(data, T, first_N): #xy, xz, yz
	d = pd.DataFrame(data)
	return [d.corr().get_values()[0][1], d.corr().get_values()[0][2], d.corr().get_values()[1][2]]


def MI(data): #movement intensity
	mi = []

	for i in range(len(data)):
		mi.append(math.sqrt(data[i][0]**2 + data[i][1]**2 + data[i][2]**2))

	return mi


def AI(data, T, first_N): #averaged movement intensity
	mi = MI(data)
	sliced_mi = slicer(mi, T, first_N)

	return list(map(np.mean, sliced_mi))


def VI(data, T, first_N): #var of movement intensity
	mi = MI(data)
	sliced_mi = slicer(mi, T, first_N)

	return list(map(np.var, sliced_mi))



def run(func, data, T, first_N):
	result = []

	if func != pairwise_correlation and func != AI and func != VI:
		result.append(func(list(np.asarray(data)[:,0]), T, first_N))
		result.append(func(list(np.asarray(data)[:,1]), T, first_N))
		result.append(func(list(np.asarray(data)[:,2]), T, first_N))
		return result

	else:
		return func(data, T, first_N)




