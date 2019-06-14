import MySQLdb
import math

db_host = 'localhost'
db_port = 3306
db_user = 'root'
db_pwd = 'root'
db_db = 'kaggle'

if __name__ == '__main__':

    print(math.log(0.1, 5))
    conn = MySQLdb.connect(host=db_host, port=db_port, user=db_user, passwd=db_pwd, db=db_db,
                           charset='utf8')
    cur = conn.cursor()
    # if cur.execute('select max(dataset_id),count(*) from userdb.kaggle_kernel;'):
    #     print cur.fetchall()
