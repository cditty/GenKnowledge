#!/usr/lib/python

import mysql.connector

HOST = ""
PORT = 3306
USER = ""
PASSWORD = ""
DB = ""

cnx = mysql.connector.connect(user=USER, password=PASSWORD,
                              host=HOST, port=PORT,
                              database=DB)
cursor = cnx.cursor()

query = ("SELECT * from table")

cursor.execute(query)

for (msgID, msgMessage, msgURL) in cursor:
  print("Message ID: {}\nMessage: {}\nURL: {}".format(1, 2, 3))
  myID = msgID
  myMessage = msgMessage
  myURL = msgURL

print myMessage

cursor.close()
cnx.close()