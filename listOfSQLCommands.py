#CREATE TABLE
#cur.execute("CREATE TABLE student (id SERIAL PRIMARY KEY, name VARCHAR);")

#INSERT
# cur.execute("INSERT INTO student (name) VALUES (%s)", ("Armand",)) # %s comme en C

#SELECT ALL
# cur.execute("SELECT * FROM student;")
# print(cur.fetchall())

#SELECT ONE
# cur.execute("SELECT * FROM student WHERE id = %s;", (1,))
# print(cur.fetchone()) affiche [1, 'Armand']
# print(cur.fetchone()['name']) ==>Affiche Armand