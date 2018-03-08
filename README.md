# Simple Twilio Survey Collector (for CS 570 at UW-Madison)
To run the program, enter Twilio credentials in the `start.sh` shell script, change permissions on the script file using `chmod <number> start.sh` if necessary. `<number>` should probably be `700` if you want the script to be private (i.e. only you can read, write, execute) or `755` if you want those same permissions but everyone else will only have read and execute permissions.

### Instructions
Before doing anything, you'll need to download [ngrok](https://ngrok.com/download "Download ngrok") and relocate it to the root of this project's directory.

1. Run `./start.sh` to run the Flask server.
2. In a separate shell, run `./ngrok http <FLASK_PORT>`
3. Copy the last entry that ngrok displays (the 'https' one). Use it to configure your Twilio webhooks for the appropriate outgoing phone number. Make sure to add '/sms' at the end so it matches the route we declared in our simple Flask app!

### Dependencies
Flask, Twilio's Python SDK,  ngrok


