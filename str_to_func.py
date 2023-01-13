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
        'sqrt': 'np.sqrt',
        '^': '**',
    }

    allowed_words = [
        'x',
        'sin',
        'cos',
        'tan',
        'pi',
        'sqrt',
        'exp',
    ]

    for old, new in replacements.items():
        string = string.replace(old, new)

    def func(x):
        return eval(string)

    return func
