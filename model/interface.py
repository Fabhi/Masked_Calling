import mysql.connector
from mysql.connector import Error

queries = {"init_session":("INSERT INTO Session(SID, Customer_No, Driver_No, Last_Update) VALUES (%(SID)s, %(customer)s, %(driver)s, NOW());"
                              "SELECT Number into @numb from Twilio_Numbers where used <> 1 order by RAND() limit 1;"
                              "UPDATE Twilio_Numbers SET used = 1 where Number=@numb;"
                              "INSERT INTO Used_By(SID, Number) VALUES (%(SID)s, @numb);"),
           "terminate_session":("delete from Session where SID=%(SID)s;"
                                  "Select Number into @numb from Used_By where SID=%(SID)s;"
                                  "UPDATE Twilio_Numbers SET used = 0 where Number=@numb;"
                                  "delete from Used_By where SID=%(SID)s;"),
           "get_number":("Select Number from Used_By where SID = %(SID)s;")}


def getErrorObject(code, message,):
    # template = "An exception of type {0} occurred on the server."
    # message = template.format(type(ex).__name__)
    return {"responseCode": str(code), "response" : str(message)}



def getNumbers(params, creds, logger):
    try:
        conn = mysql.connector.connect(**creds)
        curr = conn.cursor()
        query = ("Select Customer_No, Driver_No from Session where SID=(select SID from Used_By where Number=%(mask)s);")
        curr.execute(query,params)
        rows = curr.fetchall()
        if not rows:
            return ("0","0")
        return rows[0]
    except:
        logger.error(e)
    finally:
        #closing database connection.
        if(conn.is_connected()):
            curr.close()
            conn.close()
            print("connection is closed")

def performDB(operation, params, creds):
    try:
        conn = mysql.connector.connect(**creds)
        curr = conn.cursor()
        print(params)
        query = queries[operation]
        for _ in curr.execute(query,params, multi=True): 
                result = curr.fetchone()
        conn.commit()
        if(operation!='get_number'):
            return {'reponseCode':100,'response':operation+" successful"+" for SID:"+params['SID']}
        else:
            if not result:
                return {'responseCode':900, 'response':'No number associated with SID'}
            return {'responseCode':200,'response':result}
            
    except Error as e:
        return getErrorObject(e.errno, e.msg)
    finally:
        #closing database connection.
        try:
            if(conn.is_connected()):
                curr.close()
                conn.close()
                print("connection is closed")
        except NameError as e:
            pass