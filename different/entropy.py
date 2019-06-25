import numpy as np
from scipy.stats import entropy
from collections import Counter
import math

'''
***Example**
exception = [3, 2, 1, 3, 2, 4]
exception = np.array(exception)
p_data = list(Counter(exception).values())
entropy = entropy(p_data)  # get entropy from counts
print entropy
'''


def paritionEntropy(data, exception, des):
    # x = exception
    # y = exception
    # px = x / np.sum(x)
    # py = y / np.sum(y)
    # KL = 0.0
    # for i in range(10):
    #     KL += px[i] * np.log(px[i] / py[i])
    # return entropy
    price = list(Counter(data[:, 1]).values())
    item=list(Counter(data[:, 0]).values())
    entropy(price)

