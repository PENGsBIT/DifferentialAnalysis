# -*-coding:utf-8-*-
import requests
import json
import pymysql
import env
from datetime import datetime

# import jsonpath
# from bs4 import BeautifulSoup

connect = pymysql.connect(host=env.host, port=env.port, user=env.user, passwd=env.password, db=env.db)
cur = connect.cursor()
tablename = 'kaggle_datasets'

urlpre = 'https://www.kaggle.com/datasets_v2.json?sortBy=votes&group=public&pageSize=200&page='
urlpost = '&size=all&filetype=all&license=all'
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Referer': 'http://www.kaggle.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4882.400 QQBrowser/9.7.13059.400'
}


def getdatasetid():
    for i in range(830):
        url = urlpre + str(i + 1) + urlpost
        response = requests.get(url, headers=headers)
        pageJSON = json.loads(response.content)
        # html = response.text.encode('unicode-escape').decode('string_escape').lower()
        # jsons = json.loads(html)['banner']
        dataset_list = pageJSON.get('datasetListItems')

        for j in range(20):
            # 获得数据集概要信息
            Info = dataset_list[j]
            datasetUrl = Info.get('datasetUrl')
            title = Info.get('title')
            kaggleSetId = Info.get('datasetId')
            viewCount = Info.get('viewCount')
            downloadCount = Info.get('downloadCount')
            created = datetime.strptime(Info.get('dateCreated').split('T')[0], '%Y-%m-%d')
            updated = datetime.strptime(Info.get('dateUpdated').split('T')[0], '%Y-%m-%d')
            size = Info.get('datasetSize')
            # kernel_num = Info.get('scriptCount')
            description = Info.get('overview')
            tags = []
            tags = getTags(Info.get('categories').get('categories'), tags)
            tags = ','.join(tags)
            subsets = computeFileNumber(Info.get('commonFileTypes'))
            # dataset = {
            #     'title': dataset_title,
            #     'id': kaggleSetId,
            #     'kernel_num': kernel_num,
            #     'category': category,
            #     'description': dataset_description
            # }
            # if cur.execute('select * from userdb.kaggle_datasets where id = ' + str(kaggleSetId)):
            #     continue

            insertValue = '("' + title + '","' + str(kaggleSetId) + '","' + str(viewCount) + '","' + str(
                downloadCount) + '","' + str(created) + '","' \
                          + str(updated) + '","' + str(size) + '","' + str(
                subsets) + '","' + tags + '","' + description + '");'
            # print("insertValue" + insertValue)

            # sql = "insert into kaggle.kaggle_datasets (title, kaggleSetId, view, download, created, updated, size, subsets, tags,description) values ('{}','{}','{}','{}','{}','{}','{}','{}','{}');"\
            #     .format(title, kaggleSetId, viewCount, downloadCount, created, updated, size, subsets, tags,description)
            sql = 'insert into kaggle.kaggle_datasets (title, kaggleSetId, view, download, created, updated, size, subsets, tags,description)values ' + insertValue
            try:
                cur.execute(sql)
                env.commit()
                print("insert Page No.%d ,setID %d,Set %s" % (i, j, title))
            except Exception as e:
                print(e)
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print("Error！Page No.%d ,setID %d,Set %s" % (i, j, title))
    cur.close()


def getTags(categories, tags):
    for item in categories:
        tags.append(item.get('name'))
    return tags


def computeFileNumber(commonFileTypes):
    subset = 0
    for item in commonFileTypes:
        subset += item.get('count')
    return subset


if __name__ == '__main__':
    getdatasetid()
