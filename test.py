import scipy
import pandas as pd
import numpy as np

dictionary = {"message": 1}
a = "message"
if dictionary.get(a, " ") == " ":
    dictionary[a] = 1
else:
    dictionary[a] += 1
print(dictionary.get(a))
