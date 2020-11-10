from flask import Flask, request
from twilio.twiml.voice_response import Gather, VoiceResponse

app = Flask(__name__)

# Used by Twilio Servers to transfer the call to correct recipient
@app.route('/twilio/call', methods=['GET', 'POST'])
def call():
    caller = request.form['From'] #Contains the number of the caller
    mask = request.form['To']  #Contains the twilio number that was called

    '''TODO:
    1. Find SID of interface number stored in mask
    2. TODO: Update CUSTOMER and DRIVER'''
    (DRIVER,CUSTOMER) = getNumbers()
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
    SID = request.form['SID']

    '''TODO:
    1. Create a new entry in Sessions Table
    2. Select a random TWILIO_NUMBER from numbers Table.
    3. Create a new entry (SID, TWILIO_NUMBER) in used_by Relation
    4. Create a response dictionary and jsonify it
    '''
    return initSession(SID)


# Used by App to terminate an ongoing session
@app.route('/terminate_session', methods=['GET', 'POST'])
def terminate():
    SID = request.form['SID']

    '''TODO:
    1. Delete the SID from the Sessions Table
    2. Delete the entry (SID, TWILIO_NUMBER) in used_by Relation
    3. Create a response dictionary and jsonify it
    '''
    return terminateSession(SID)

# Used by App to find the TWILIO_NUMBER associated with a SID
@app.route('/mask_number', methods=['GET', 'POST'])
def query():
    SID = request.form['SID']

    '''TODO:
    1. Query the used_by relation to find the TWILIO_NUMBER used by SID
    2. Create a response dictionary and jsonify it
    '''
    return querySession(SID)

def main():
    app.run()

if __name__ == '__main__':
    main()
