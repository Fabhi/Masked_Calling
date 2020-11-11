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
    mycursor.execute("drop table if exists `Twilio_Numbers`;")
    mycursor.execute("create table `Twilio_Numbers`(`Number` varchar(15) primary key);")

    mycursor.execute("drop table if exists `Session`;")
    mycursor.execute("create table `Session`(`SID` int primary key, `Customer_No` int, `Driver_No` int, `Last_Update` datetime);")

    mycursor.execute("drop table if exists `Used_By`;")
    mycursor.execute("create table `Used_By`(`SID` int, `Number` varchar(15), foreign key(`SID`) references Session(`SID`), foreign key(`Number`) references Twilio_Numbers(`Number`));")

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
