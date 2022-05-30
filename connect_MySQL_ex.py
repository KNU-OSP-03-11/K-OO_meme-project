import pymysql

# --------- edit data (insert, update, delete) example -----------
def insert(self, vo):
# 1. connect
#conn = pymysql.connect(host='localhost', user='root', password='password', db='encore', charset='utf8')
    self.conn = pymysql.connect(host='localhost', user='root', password='bumsu1208', db='encore', charset='utf8')

# 2. create cursor
#cur = conn.cursor()
    cur = self.conn.cursor()

# 3. insert data
#sql = 'insert into departments values(280, "depth test", null, 1700)'
#sur.execute(sql)

# insert using format
#sql = "insert into members values(%s, %s, %s, %s)"
#vals = (id, pwd, name, email)
    fals = (vo.id, vo.pwd, vo.name, vo.email)
    cur.execute(sql, vals)

# 4. save data
#conn.commit()
    self.conn.commit()
# 5. finish connect
#conn.close()
    self.conn.close()

# --------------- read data(select) -------------------
# 1. connect
conn = pymysql.connect(host='localhost', user='root', password='password', db='encore', charset='utf8')

# 2. create cursor
cur = conn.cursor()

# 4. read data
sql = 'select * from departments where department_id=%d'
vals = (department_id,)
cur.execute(sql, vals)

# 5. fetch result at cursor
# print lines
for row in cur:
    print(row[0], row[1], row[2], row[3])

# print a line
row = cur.fetchone()
if row == None:
    print('NO result')
else:
    print(row[0], row[1], row[2], row[3])