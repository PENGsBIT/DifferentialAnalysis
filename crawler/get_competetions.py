# -*-coding:utf-8-*-
import requests
import json
import MySQLdb
import conn as conn
import codecs
from bs4 import BeautifulSoup

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Referer': 'http://www.kaggle.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4882.400 QQBrowser/9.7.13059.400'
}

conn = MySQLdb.connect(host=conn.db_host, port=conn.db_port, user=conn.db_user, passwd=conn.db_pwd, db=conn.db_db,
                       charset='utf8')
cur = conn.cursor()

def get_kernels(cid,lastid):
    cur.execute('select id from userdb.kaggle_competitions where team_num >0;')
    competitions = cur.fetchall()
    ccount = 0
    for i in competitions:
        ccount += 1
        last_id = 0
        if i[0]<cid:
            continue
        if i[0]==cid:
            last_id = lastid
        enen(ccount, i[0], last_id)


def enen(ccount, cid, last_id):
    print(ccount, cid, last_id)
    url = 'https://www.kaggle.com/kernels.json?sortBy=scoreDescending&group=everyone&pageSize=20&after=' + str(
        last_id) + '&competitionId=' + str(cid)

    try:
        content = requests.get(url, headers=headers).content
    except:
        print('cannot get kernels of competition : id' + str(cid))
    try:
        if len(content) < 3:
            return
    except:
        get_kernels(cid,last_id)
    js = json.loads(content)

    for i in js:
        kid = i.get('id')
        last_id = kid
        if cur.execute('select * from userdb.kaggle_competitions_kernels where kernel_id =' + str(kid) + ';'):
            continue
        language = i.get('aceLanguageName')
        medal = ""
        medal = i.get('medal')
        best_score = str(i.get('bestPublicScore'))
        title = i.get('title').replace("'", ' ')
        url = i.get('scriptUrl')
        votes = i.get('totalVotes')
        content = ""

        sql = "insert into userdb.kaggle_competitions_kernels values (" \
              "'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                  kid, cid, title, votes, best_score, medal, language, url, content, content)
        try:
            cur.execute(sql)
            conn.commit()
        except:
            print(sql)
            with codecs.open("error.txt",'a','utf-8') as f:
                f.writelines(sql)
                f.write('\n')
    enen(ccount, cid, last_id)


get_kernels(5568,119394)
# get_kernels1()
# get_kernels2()
# def get_content(url):


def get_competition_id():
    for i in range(1, 18):
        url = 'https://www.kaggle.com/competitions.json?sortBy=recentlycreated&pageSize=20&page=' + str(i)
        content = requests.get(url, headers=headers).content
        js = json.loads(content).get('pagedCompetitionGroup').get('competitions')
        for e in js:
            id = e.get('competitionId')
            if cur.execute('select * from userdb.kaggle_competitions where id =' + str(id) + ';'):
                continue
            title = e.get('competitionTitle')
            description = e.get('competitionDescription')
            url = e.get('competitionUrl')
            team_num = e.get('totalTeams')
            kernel_num = e.get('totalKernels')
            reward = e.get('rewardDisplay')
            level = e.get('hostSegment')
            enabledata = e.get('enabledDate')[0:10]
            deadline = e.get('deadline')[0:10]
            datatype = []
            analysis = []
            problemtype = []
            category = []
            em = e.get("evaluationMetric")
            for c in e.get('categories').get('categories'):
                cid = c.get('id')
                cfullpath = c.get('fullPath')
                cname = c.get('name')
                category.append(cname)
                if ('data type' in cfullpath):
                    datatype.append(cfullpath[cfullpath.find('>') + 2:])
                if ('analysis' in cfullpath):
                    analysis.append(cfullpath[cfullpath.find('>') + 2:])
                if ('problem type' in cfullpath):
                    problemtype.append(cfullpath[cfullpath.find('>') + 2:])

            sql = "insert into userdb.kaggle_competitions values (" \
                  "'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                      id, title.replace("'", ' '), reward, level, str(datatype).replace("'", '"'),
                      str(problemtype).replace("'", '"'),
                      str(analysis).replace("'", '"'), str(category).replace("'", '"'), description.replace("'", '"'),
                      url.replace("'", '"'), team_num,
                      kernel_num, enabledata, deadline, em)
            try:
                cur.execute(sql)
                conn.commit()
            except:
                print(sql)
# get_competition_id()
