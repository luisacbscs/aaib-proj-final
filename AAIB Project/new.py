import numpy as np

def load_data():

    data = np.loadtxt('all1.txt')

    classes = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    data_class = []
    for i in classes:
        data_class = data_class + [i] * 30

    return data, data_class
