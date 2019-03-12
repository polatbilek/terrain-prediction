from readwrite import get_data
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
import numpy as np

def scatter(path, name):
	data = get_data(path)
	pd_data = pd.DataFrame(data)

	plt.title("column 0 " + name)
	plt.plot(pd_data[0])
	plt.show()

	plt.title("column 1 " + name)
	plt.plot(pd_data[1])
	plt.show()

	plt.title("column 2 " + name)
	plt.plot(pd_data[2])
	plt.show()

	return pd_data


def boxplot(datas, names):
	column0 = []
	column1 = []
	column2 = []
	labels = []

	for i in range(len(datas)):
		column0.append(datas[i][0])
		column1.append(datas[i][1])
		column2.append(datas[i][2])
		labels.append(names[i])

	plt.title("Boxplot column 0")
	plt.boxplot(column0, labels=labels)
	plt.show()

	plt.title("Boxplot column 1")
	plt.boxplot(column1, labels=labels)
	plt.show()

	plt.title("Boxplot column 2")
	plt.boxplot(column2, labels=labels)
	plt.show()

def draw_gaussian(datas):
	pdf_ticks = np.linspace(0, 10000, 100000, endpoint=False)

	density = gaussian_kde(datas)
	plt.plot(pdf_ticks, density(pdf_ticks), color='r')
	plt.show()
