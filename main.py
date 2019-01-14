from readwrite import get_data
import pandas as pd
import matplotlib.pyplot as plt

path_to_file_1 = "C:\\Users\\polat\\Desktop\\117E747\\2018.11.8-BC_GO\\0_27_4_ls.192.168.4.41.dat"
path_to_file_2 = "C:\\Users\\polat\\Desktop\\117E747\\2018.11.8-BC_GO\\1_5_0_ls.192.168.4.41.dat"
path_to_file_3 = "C:\\Users\\polat\\Desktop\\117E747\\2018.11.8-BC_GO\\0_43_44_uh.192.168.4.41.dat"
path_to_file_4 = "C:\\Users\\polat\\Desktop\\117E747\\2018.11.8-BC_GO\\0_53_15_dh.192.168.4.41.dat"

data = get_data(path_to_file_1, selection_type="one")
pd_data = pd.DataFrame(data)
pd_data_ls1 = pd_data

plt.title("column 0 file 1")
plt.plot(pd_data[0])
plt.show()

plt.title("column 1 file 1")
plt.plot(pd_data[1])
plt.show()

plt.title("column 2 file 1")
plt.plot(pd_data[2])
plt.show()

data = get_data(path_to_file_2, selection_type="one")
pd_data = pd.DataFrame(data)
pd_data_ls2 = pd_data

plt.title("column 0 file 2")
plt.plot(pd_data[0])
plt.show()

plt.title("column 1 file 2")
plt.plot(pd_data[1])
plt.show()

plt.title("column 2 file 2")
plt.plot(pd_data[2])
plt.show()

data = get_data(path_to_file_3, selection_type="one")
pd_data = pd.DataFrame(data)

plt.title("column 0 file 3")
plt.plot(pd_data[0])
plt.show()

plt.title("column 1 file 3")
plt.plot(pd_data[1])
plt.show()

plt.title("column 2 file 3")
plt.plot(pd_data[2])
plt.show()

data = get_data(path_to_file_4, selection_type="one")
pd_data = pd.DataFrame(data)

plt.title("column 0 file 4")
plt.plot(pd_data[0])
plt.show()

plt.title("column 1 file 4")
plt.plot(pd_data[1])
plt.show()

plt.title("column 2 file 4")
plt.plot(pd_data[2])
plt.show()


plt.title("Boxplot column 0")
plt.boxplot([pd_data_ls1[0], pd_data_ls2[0]], labels=['1', '2'])
plt.show()

plt.title("Boxplot column 1")
plt.boxplot([pd_data_ls1[1], pd_data_ls2[1]], labels=['1', '2'])
plt.show()

plt.title("Boxplot column 2")
plt.boxplot([pd_data_ls1[2], pd_data_ls2[2]], labels=['1', '2'])
plt.show()