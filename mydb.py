import mysql.connector

dataBase = mysql.connector.connect(
  host = 'localhost',
  user = 'root',
  passwd = 'rootaniedi',
  
)

cursorObject = dataBase.cursor()

cursorObject.execute("CREATE DATABASE tandemsql")

print("Database Created!")

# From terminal run $ python.mydb.py
# If you get Database Created then all is well