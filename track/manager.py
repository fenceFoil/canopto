from twilio.rest import TwilioRestClient
import datetime
import json
import time
from Canopto import Canopto
from PersonTracker import PersonTracker


class Message:
    def __init__(self):
        self.id = ""
        self.body = ""
        self.phone_from = ""
        self.phone_to = ""

    def __init__(self, id, phone_from, phone_to, body):
        self.id = id
        self.phone_from = phone_from
        self.phone_to = phone_to
        self.body = body

    def __str__(self):
        return (self.id, self.phone_from, self.phone_to, self.body)


def main():
    #Initialize Canopto Display
    display = Canopto(8, 8)
    display.start()

    #Initialize Person Tracker
    tracker = PersonTracker()
    PersonTracker.start(tracker)

    CONFIG_PATH = '/home/aoi/code/canopto_config.json'
    # API KEYS FOUND HERE: https://www.twilio.com/user/account  (NOT  under DEV TOOLS > API KEYS)
    # Read API keys for Twilio from json config file (outside of git repository)
    # Or use environment variables as https://github.com/twilio/twilio-python suggests
    with open(CONFIG_PATH) as json_config:
        config = json.load(json_config)
        ACCOUNT_SID = config['twilio']['account_sid']
        AUTH_TOKEN = config['twilio']['auth_token']
        print("Successfuly read api information from config")

    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

    processedMessages = []
    processedIDs = []
    toProcess = []
    running = True

    while (running):
        for message in client.messages.list():
            if (message.direction == "inbound"):
                #New message from today that hasn't already been processed
                currentMessage = Message(message.sid, message.from_, message.to, message.body)
                if message.sid not in processedIDs and datetime.datetime.today() < message.date_created:
                    display.drawSentence(message.body)

                    processedIDs.append(message.sid)
                    processedMessages.append(currentMessage)
                    #Reposition the tracker
                    #tracker.setTrackingPosition()
                    #toProcess.append(currentMessage)
                else:
                    print("ignoring")
                    print(processedMessages)
                print(message.sid, message.body)
                #print [m.__str__() for m in toProcess]
        time.sleep(3)


if __name__ == "__main__":
    main()
    #time.sleep(1)
    #CANOPTO.drawSentence("Hello")
