import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
def initDB(creds):
    try:
        mydb = mysql.connector.connect(**creds)
        mycursor = mydb.cursor()
        mycursor.execute("CREATE DATABASE if not exists `JCO`")
        mycursor.execute("create table if not exists `Twilio_Numbers`(`Number` varchar(15) primary key, `used` int DEFAULt 0);")
        mycursor.execute("create table if not exists `Session`(`SID` int primary key, `Customer_No` varchar(15) NOT NULL, `Driver_No` varchar(15) NOT NULL, `Last_Update` datetime NOT NULL);")
        mycursor.execute("create table if not exists `Used_By`(`SID` int NOT NULL, `Number` varchar(15) NOT NULL);")
        mydb.commit()

    except mysql.connector.Error as error :
        print("Failed to update record to database rollback: {}".format(error))
        #reverting changes because of exception
        mydb.rollback()
    finally:
        #closing database connection.
        try:
            if(mydb.is_connected()):
                mycursor.close()
                mydb.close()
                return "Success"
        except NameError as e:
            return "Error Occured in Refreshing DB"

if __name__ == "__main__":
    print(initDB())
