import psycopg2

DB_HOST = "localhost"
DB_USER = "postgres"
DB_PASS = "root"
DB_NAME = "postgres"

conn = psycopg2.connect(host="DB_HOST", user="DB_USER", password="DB_PASS", database="DB_NAME")

conn.close()
