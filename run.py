from flask import Flask, request, session
from twilio.twiml.messaging_response import MessagingResponse
import os, datetime, csv

PORT = os.environ["PORT"]
SECRET_KEY = os.environ["TWILIO_AUTH_TOKEN"]

app = Flask(__name__)
app.config.from_object(__name__)

participants = {
    "+<country_code><phone_number>" : "<name_of_participant>"
}


@app.route("/")
def hello():
    return "Hello World!"

@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    """ RESPOND TO USER TEXT MESSAGES TO THE TWILIO NUMBER"""
    counter = session.get('counter', 0)
    counter = counter + 1
    
    body = request.values.get('Body', None)
    
    date = datetime.datetime.now().isoformat()

    # save new counter value in the session
    #session['counter'] = counter
    
    from_number = request.values.get('From')
    if from_number in participants:
        name = participants[from_number]
    else:
        name = "Unknown"

    resp = MessagingResponse()
    
    if body.isdigit():
        if (int(body) > 5 or int(body) < 0):
            resp.message("Please enter a valid number between 0-5!")
        else:
            resp.message("Thank you!")
            save_data(name, int(body), date)
    else:
        resp.message("Please enter a valid number!")

    """
    # build the response
    message = '{} has messaged {} {} times.' \
        .format(name, request.values.get('To'), counter)
    """

    print(date)

    return str(resp)

def save_data(name, value, timestamp):
    with open('data.csv', 'a') as csvfile:
        wr = csv.writer(csvfile, dialect='excel')
        wr.writerow([name, value, timestamp])

if __name__ == "__main__":
    app.run(debug=True, port=int(PORT))
    
