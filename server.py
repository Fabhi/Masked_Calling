from Model.interface import performDB
from Model.interface import getNumbers
from flask import Flask, request, jsonify
from twilio.twiml.voice_response import Gather, VoiceResponse
from Data.creds import creds
app = Flask(__name__)

@app.route("/test", methods=['GET', 'POST'])
def index() -> str:
    test = request.form.get('returnMe')
    # transform a dict into an application/json response 
    return jsonify({"message": "It Works", 'value':test})


# Used by Twilio Servers to transfer the call to correct recipient
@app.route('/twilio/call', methods=['GET', 'POST'])
def call():
    caller = request.form.get('From') #Contains the number of the caller
    mask = request.form.get('To') #Contains the twilio number that was called
    if not (caller and mask):
        return jsonify({"responseCode": 900,"response": "Insufficient Parameters! Please refer to documents"})
    '''
    1. Find SID of interface number stored in mask
    2. Update CUSTOMER and DRIVER'''

    (DRIVER,CUSTOMER) = getNumbers({'mask':mask}, creds)
    response = VoiceResponse()
    if caller == CUSTOMER:  # if the customer is calling
        response.say("Please wait while we contact the driver")
        response.dial(DRIVER, mask)
    elif caller == DRIVER:  # if driver is calling
        response.say("Please wait while we contact the customer")
        response.dial(CUSTOMER, mask)
    else: #Every other number
        response.say("This call is invalid. This trip is over. Please contact Rento for any inquiries.", voice="man")
    return str(response)

# Used by App to initialize a session
@app.route('/init_session', methods=['GET', 'POST'])
def initialize():
    SID = request.form.get('SID')
    customer = request.form.get('customer')
    driver = request.form.get('driver')
    if not (SID and customer and driver):
        return jsonify({"responseCode": 900,"response": "Insufficient Parameters! Please refer to documents"})
    '''
    1. Create a new entry in Sessions Table
    2. Select a random TWILIO_NUMBER from numbers Table.
    3. Create a new entry (SID, TWILIO_NUMBER) in used_by Relation
    4. Create a response dictionary and jsonify it
    '''
    response = performDB(request.url_rule.rule[1:],{'SID':SID,'driver':driver,'customer': customer}, creds)
    assert type(response) is dict
    return jsonify(response)

# Used by App to terminate an ongoing session
@app.route('/terminate_session', methods=['GET', 'POST'])
def terminate():
    SID = request.form.get('SID')
    if not (SID):
        return jsonify({"responseCode": 900,"response": "Insufficient Parameters! Please refer to documents"})
    '''
    1. Delete the SID from the Sessions Table
    2. Delete the entry (SID, TWILIO_NUMBER) in used_by Relation
    3. Create a response dictionary and jsonify it
    '''
    response = performDB(request.url_rule.rule[1:], {'SID':SID}, creds)
    assert type(response) is dict
    return jsonify(response)
# Used by App to find the TWILIO_NUMBER associated with a SID
@app.route('/get_number', methods=['GET', 'POST'])
def query():
    SID = request.form.get('SID')
    if not (SID):
        return jsonify({"responseCode": 900,"response": "Insufficient Parameters! Please refer to documents"})
    '''
    1. Query the used_by relation to find the TWILIO_NUMBER used by SID
    2. Create a response dictionary and jsonify it
    '''
    response = performDB(request.url_rule.rule[1:], {'SID':SID}, creds)
    assert type(response) is dict
    return jsonify(response)

def main():
    app.run(host="0.0.0.0")

if __name__ == '__main__':
    main()
