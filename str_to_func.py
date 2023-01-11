import re
import numpy as np
import matplotlib.pyplot as plt

def str_to_func(string):

    replacements = {
        'sin' : 'np.sin',
        'cos' : 'np.cos',
        'exp': 'np.exp',
        'sqrt': 'np.sqrt',
        '^': '**',
    }

    allowed_words = [
        'x',
        'sin',
        'cos',
        'sqrt',
        'exp',
    ]
    
    for old, new in replacements.items():
        string = string.replace(old, new)
        
    alg = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    for char in range(len(string)):
        if string[char] == 'x':
            if string[char-1] in alg:
                string = string[:char]+'*'+string[char:]

    def func(x):
        return eval(string)

    return func
