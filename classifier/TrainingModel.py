# coding=UTF-8
import numpy as np
import pymysql
import env
from classifier.classification import classifierTraining
from classifier.normalized import *

if __name__ == '__main__':
    connect = pymysql.connect(host=env.host, port=env.port, user=env.user, passwd=env.password, db=env.db)
    cur = connect.cursor()
    cur.execute("SELECT view,download,created,updated,size,subsets FROM " + env.db + '.' + env.tableName)
    data = []
    data = np.array(cur.fetchall())
    cur.close()
    colName = np.array(["view", "download", "created", "updated", "size", "subsets"])
    target = formatTarget(data[:, 1])
    structuredData = formatStructuredData(data[:, [0, 4, 5]])
    timeData = formatTime(data[:, [2, 3]])
    classifierTraining(data, structuredData, timeData, target, colName)
    # data = list(cur.fetchall())
    # data=pd.DataFrame(data)
    # print(data.isnull().sum())
    # cur.execute(" DESC " + env.db + '.' + env.tableName)
    # description = cur.fetchall()
    # print(description)
