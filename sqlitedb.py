import sqlite3
from sqlite3 import Error

def create_database():
	conn = None
	try:
		conn = sqlite3.connect("data.sqlite")
		return conn
	except Error as e:
		print(e)
	return conn

def create_table(conn):
	try:
		cur = conn.cursor()
		table = """CREATE TABLE IF NOT EXISTS data (
			council_reference VARCHAR(20) PRIMARY KEY,
			address TEXT,
			council TEXT,
			description TEXT,
			info_url TEXT,
			date_scraped DATE
			);"""
		cur.execute(table)
		# print("Table created")
	except Error as e:
		print(e)

def store_data(data, conn):
	sql = """   INSERT INTO data(council_reference, address, council, description, info_url, date_scraped)
                VALUES(?, ?, ?, ?, ?, ?)"""
	cur = conn.cursor()
	cur.execute(sql, data)
	conn.commit()