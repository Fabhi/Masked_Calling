import threading
from flask import Flask, request, jsonify, send_file
from twilio.twiml.voice_response import Gather, VoiceResponse
import logging

from model.interface import *
from data.setup import initDB
from data.creds import creds


app = Flask(__name__)
@app.route("/")
def homepage():
    return """
    <h1>JCO Masked Calling Microservice</h1>
    """


# Used for Testing
@app.route("/test", methods=['GET', 'POST'])
def index() -> str:
    test = request.form.get('returnMe')
    # transform a dict into an application/json response
    return jsonify({"message": "It Works", 'value':test})


def writeLog(caller, mask, wasConnected=False, callerType="", connectedTo=""):
    handle = open('calls.log', 'a+')
    strings = ["[CALL EVENT]\n",
                    "\tCALLER : "+caller+"\n",
                    "\tTWILIO NUMBER : "+mask+"\n",
                    "\tVALID CALLER : "+str(wasConnected)+"\n"]
    if(wasConnected):
        strings.append("\tCALLER TYPE : "+callerType+"\n")
        strings.append("\tCONNECTED TO : "+connectedTo+"\n")
    handle.writelines(strings)
    handle.close()


# Used by Twilio Servers to transfer the call to correct recipient
@app.route('/twilio/call', methods=['GET', 'POST'])
def call():
    caller = request.form.get('From') #Contains the number of the caller
    mask = request.form.get('To') #Contains the twilio number that was called
    if not (caller and mask):
        return jsonify({"responseCode": 900,"response": "Insufficient Parameters! Please refer to documents"})

    wasConnected, callerType, connectedTo = True, "", ""

    (DRIVER,CUSTOMER) = getNumbers({'mask':mask}, creds, app.logger)
    # (CUSTOMER,DRIVER) = ("+919611139444", "+918660817513")
    response = VoiceResponse()
    app.logger.error(caller)
    app.logger.error(CUSTOMER)
    app.logger.error(DRIVER)
    if caller == CUSTOMER:  # if the customer is calling
        response.say("Welcome to Rent O. Please wait while we connect you to your driver")
        response.dial(DRIVER, caller_id=mask)
        callerType = "Customer"
        connectedTo = DRIVER
    elif caller == DRIVER:  # if driver is calling
        response.say("Welcome to Rent O. Please wait while we connect you to your customer")
        response.dial(CUSTOMER, caller_id=mask)
        callerType = "Driver"
        connectedTo = CUSTOMER
    else: #Every other number
        response.say("Welcome to Rent O. This call is invalid. This trip is over. Or does not exist. Please contact Rent O for any inquiries.", voice="man")
        wasConnected = False
    threading.Thread(target = writeLog, args = (caller, mask, wasConnected, callerType, connectedTo)).start()
    return str(response)

@app.route('/twilio/<mask>')
def statusCallback(mask):
    return jsonify({"response" : "Obtained"})

# Used by App to initialize a session
@app.route('/init_session', methods=['GET', 'POST'])
def initialize():
    SID = request.form.get('SID')
    customer = request.form.get('customer')
    driver = request.form.get('driver')
    if not (SID and customer and driver):
        return jsonify({"responseCode": 900,"response": "Insufficient Parameters! Please refer to documents"})
    response = performDB(request.url_rule.rule[1:],{'SID':SID,'driver':driver,'customer': customer}, creds)
    assert type(response) is dict
    return jsonify(response)

# Used by App to terminate an ongoing session
@app.route('/terminate_session', methods=['GET', 'POST'])
def terminate():
    SID = request.form.get('SID')
    if not (SID):
        return jsonify({"responseCode": 900,"response": "Insufficient Parameters! Please refer to documents"})
    response = performDB(request.url_rule.rule[1:], {'SID':SID}, creds)
    assert type(response) is dict
    return jsonify(response)

# Used by App to find the TWILIO_NUMBER associated with a SID
@app.route('/get_number', methods=['GET', 'POST'])
def query():
    SID = request.form.get('SID')
    if not (SID):
        return jsonify({"responseCode": 900,"response": "Insufficient Parameters! Please refer to documents"})
    response = performDB(request.url_rule.rule[1:], {'SID':SID}, creds)
    assert type(response) is dict
    return jsonify(response)


# Management Callbacks
@app.route('/initDB', methods=["GET", "POST"])
def initDatabase():
    response = initDB(creds)
    return jsonify({"response": response})

@app.route('/getLogs', methods=["GET", "POST"])
def sendLogs():
    return send_file("calls.log")

if __name__ != '__main__':
    # if we are not running directly, we set the loggers
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

if __name__ == '__main__':
    app.run(host="0.0.0.0")
