import mysql.connector
from mysql.connector import Error

def getErrorObject(code, error):
    # template = "An exception of type {0} occurred on the server."
    # message = template.format(type(ex).__name__)
    return {"responseCode": code, "response" : message}

def getNumbers(SID):
    try:
        conn = mysql.connector.connect(host="localhost", user="root", password="root", database="mydatabase")
        curr = conn.cursor()
        # SQL query
        conn.commit()
        return (customer, driver)
    except Exception as e:
        return ("0","0")
    finally:
        #closing database connection.
        if(conn.is_connected()):
            mycursor.close()
            conn.close()
            print("connection is closed")

def initSession(SID, driver, customer):
    try:
        conn = mysql.connector.connect(host="localhost", user="root", password="root", database="mydatabase")
        curr = conn.cursor()
        # SQL query
        conn.commit()
        return None
    except Error as e:
        return getErrorObject(e.errno, e.msg)
    finally:
        #closing database connection.
        if(conn.is_connected()):
            mycursor.close()
            conn.close()
            print("connection is closed")
def terminateSession(SID):
    try:
        conn = mysql.connector.connect(host="localhost", user="root", password="root", database="mydatabase")
        curr = conn.cursor()
        # SQL query
        conn.commit()
        return None
    except Error as e:
        return getErrorObject(e.errno,e.msg)
    finally:
        #closing database connection.
        if(conn.is_connected()):
            mycursor.close()
            conn.close()
            print("connection is closed")
def querySession(SID):
    try:
        conn = mysql.connector.connect(host="localhost", user="root", password="root", database="mydatabase")
        curr = conn.cursor()
        # SQL query
        conn.commit()
        return None
    except Error as e:
        return getErrorObject(e.errno,e.msg)
    finally:
        #closing database connection.
        if(conn.is_connected()):
            mycursor.close()
            conn.close()
            print("connection is closed")
