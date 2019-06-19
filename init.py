import numpy as np

if __name__ == '__main__':
    setStatisticalData = []
    structuredData = formatStructuredData(setStatisticalData[:, 0: 3])
    timeData = formatTime(setStatisticalData[:, [3, 4]])
    formatData = np.concatenate((structuredData, timeData), axis=1)
    #classifier(formatData, 'dt')

