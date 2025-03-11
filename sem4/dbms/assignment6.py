import pymysql

host = "localhost"
user = "root"
password = "root"
database = "assignment6"

connection = pymysql.connect(host=host, user=user, password=password,database=database)

cursor = connection.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS faculty (name VARCHAR(20) NOT NULL, id INT PRIMARY KEY)")
cursor.execute("CREATE TABLE IF NOT EXISTS student (name VARCHAR(20) NOT NULL, prn INT PRIMARY KEY)")
cursor.execute("CREATE TABLE IF NOT EXISTS course (name VARCHAR(20) NOT NULL, id VARCHAR(20) PRIMARY KEY)")

cursor.execute("INSERT INTO faculty VALUES ('John', 16)")
cursor.execute("INSERT INTO student VALUES ('Jane', 102342)")
cursor.execute("INSERT INTO course VALUES ('Computer Networks', 'CN1')")

cursor.execute("SELECT * FROM faculty")
results = cursor.fetchall()
for row in results:
    print(row)

cursor.close()
connection.close()
