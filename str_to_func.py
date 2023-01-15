import re
import numpy as np
import matplotlib.pyplot as plt

def str_to_func(string):
    
    replacements = {
        'sin' : 'np.sin',
        'cos' : 'np.cos',
        'tan' : 'np.tan',
        'π' : 'np.pi',
        'exp': 'np.exp',
        '√': 'np.sqrt',
        '^': '**',
    }

    allowed_words = [
        'x',
        'sin',
        'cos',
        'tan',
        'pi',
        '√',
        'exp',
    ]

    for old, new in replacements.items():
        string = string.replace(old, new)

    alg = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    for i in range(len(string)):
        if string[i] == 'x':
            if string[i-1] in alg:
                string = string[:i]+'*'+string[i:]

    def func(x):
        return eval(string)

    return func
