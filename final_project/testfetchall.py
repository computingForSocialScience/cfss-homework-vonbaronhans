import pymysql

dbname="dicegame"
host="localhost"
user="root"
passwd="computers"
db=pymysql.connect(db=dbname, host=host, user=user,passwd=passwd, charset='utf8')

cur = db.cursor()

get_condition = """SELECT cond from dicegame;"""
cur.execute(get_condition)
cond_tupl = cur.fetchall()
cond = []
for i in cond_tupl:
	extract = i[0]
	cond.append(extract)
#print cond
cond.remove(u"'cond'")
print "Count of Gain Salient condition =", cond.count("'Gain Salient'")
print "Count of Gain Computer condition =", cond.count("'Gain Computer'")
print "Count of Loss Salient condition =", cond.count("'Loss Salient'")
print "Count of Gain Computer condition =", cond.count("'Loss Computer'")
print "Total observations =", len(cond)