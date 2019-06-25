# -*- coding: UTF-8 -*-
from impala.dbapi import connect
import numpy as np
from different import differInterval
from different.isolation import *
from different.localOutlierFactor import *
from log import log
from recommendcolumn import keyColumn_RandomForest

if __name__ == '__main__':
    log("Project start")
    args = ["10.141.212.155", 10010, "", "", "bigbench_100g", "websales_home_myshop"]
    # conn = hive.Connection(host="10.141.212.155", port=10010, database='bigbench_100g')
    conn = connect(host="10.141.212.155", port=10010, database='bigbench_100g', auth_mechanism='PLAIN')
    log("connect hive ")
    assign_columns = []
    cur = conn.cursor()
    cur.execute('SELECT * FROM  websales_home_myshop  LIMIT 1')
    des = cur.description
    para = ""
    for i in des:
        colnames = i[0].split(".")
        if ('1' in colnames[1]):
            continue
        else:
            assign_columns.append(colnames[1])
    for i in assign_columns:
        para += i + ","
    para = para[0:-1]
    cur.execute("SELECT " + para + " FROM " + args[5])
    log("get data from hive")
    data = np.array(map(list, cur.fetchall()))
    cur.close()
    conn.close()
    log("connect close")
    log("recommend columns")
    feat_labels, importance = keyColumn_RandomForest.keyColumn_RandomForest(data, para)
    log("compute differtial interval")
    differInterval(data)

