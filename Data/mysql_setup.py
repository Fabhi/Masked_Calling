import os
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
import logging

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
try:
    mydb = mysql.connector.connect(host="localhost",
                                   user="root",
                                   password="root",
                                   database="mydatabase")

    mycursor = mydb.cursor()
    mycursor.execute("create table if not exists`Twilio_Numbers`(`Number` varchar(15) primary key);")

    mycursor.execute("create table if not exists`Session`(`SID` int primary key, `Customer_No` int NOT NULL, `Driver_No` int NOT NULL, `Last_Update` datetime NOT NULL);")

    mycursor.execute("create table if not exists `Used_By`(`SID` int NOT NULL, `Number` varchar(15) NOT NULL, foreign key(`SID`) references Session(`SID`), foreign key(`Number`) references Twilio_Numbers(`Number`));")


    mydb.commit()

except mysql.connector.Error as error :
    print("Failed to update record to database rollback: {}".format(error))
    #reverting changes because of exception
    mydb.rollback()
finally:
    #closing database connection.
    if(mydb.is_connected()):
        mycursor.close()
        mydb.close()
        print("connection is closed")
