import pymysql
import env
import numpy as np
import pandas as pd
from classifier.classification import classifier

from classifier.normalized import *

if __name__ == '__main__':
    data = []
    structuredData = formatStructuredData(data[:, 0: 3])
    timeData = formatTime(data[:, [3, 4]])
    formatData = np.concatenate((structuredData, timeData), axis=1)
    classifier(formatData, 'dt')
    print()
