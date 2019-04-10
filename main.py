from data_organization import *

path = "/home/darg2/Desktop/117E747"
ip = "192.168.4."

threshold = 0
first_N = 300
window_size = 50
split_rate = 0.80
K = 5

data, filenames_of_data = organise_data(path, ip)

#single_run(data, split_rate, threshold, first_N, window_size)
k_fold(data, K, threshold, first_N, window_size)







