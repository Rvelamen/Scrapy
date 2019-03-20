import pymysql

class DBHelper:
    def __init__(self,host='localhost',
    port=3306,
    user='root',
    passwd='12345678',
    db='0',
    charset='utf8'):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.db = db
        self.charset = charset
        self.conn = None
        self.cur = None

    def connectDatabase(self):
        try:
            self.conn =pymysql.connect(host=self.host,port=self.port,user=self.user,passwd=self.passwd,db=self.db,charset=self.charset)
            print("Database connected Success!!!")
        except:
            print("数据库连接错误！！！")
            return False
        self.cur = self.conn.cursor()
        return True

    def close(self):
        if self.conn and self.cur:
            self.cur.close()
            self.conn.close()
        return True



if __name__ == '__main__':
    db = DBHelper()
    db.connectDatabase()
    sql = "INSERT INTO problem (pid,url) VALUES ('%d','%s')"
    db.cur.execute(sql % (1,"123"))
    db.conn.commit()
    db.close()
