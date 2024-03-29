import numpy as np
import math

file = "testdata.txt"

if __name__ == "__main__":
    with open(file, "r") as my_file:
        data = my_file.read()

    new_data = data.replace('\n', ' ').replace('\t', ' ')
    list_data = new_data.split(" ")

    # max_idx = len(list_data)
    # print(max_idx)

    arr_data = np.array(list_data, dtype=np.float32)
    print(np.max(arr_data), np.min(arr_data))