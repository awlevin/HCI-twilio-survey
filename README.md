# Simple Twilio Survey Collector (for CS 570 at UW-Madison)
## Purpose
This simple Flask server with Twilio integration is designed to help us conduct a daily survey, as part of our cultural probe for our human computer interaction project. The server is hardcoded to send text messages at 9:00AM every day for roughly 7 days, asking users how many times they expect to take the bus each day. The users can respond with a number (0-10) and the server records the users' responses in `data.csv`. If a user enters invalid input, the server will store their response in a separate file `error_logs.txt`. 

### Instructions
Before doing anything, you'll need to download [ngrok](https://ngrok.com/download "Download ngrok") and relocate it to the root of this project's directory.

Next, enter Twilio credentials in the `start.sh` shell script, change permissions on the script file using `chmod <number> start.sh` so that it is executable (if not already). The `<number>` should probably be `700` if you want the script to be private (i.e. only you can read, write, execute) or `755` if you want those same permissions but everyone else will only have read and execute permissions.

Also make sure to update `participants.json` so the Flask server knows to whom it should send the survey!

1. Run `./start.sh` to run the Flask server.
2. In a separate shell, run `./ngrok http <FLASK_PORT>`
3. Copy the last entry that ngrok displays (the 'https' one). Use it to configure your Twilio webhooks for the appropriate outgoing phone number. Make sure to add '/sms' at the end so it matches the route we declared in our simple Flask app!

### Dependencies
Flask, Twilio's Python SDK,  ngrok
