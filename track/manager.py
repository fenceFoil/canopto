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
        return str((self.id, self.phone_from, self.phone_to, self.body))


def main():
    #Initialize Canopto Display
    display = Canopto(8, 8)
    Canopto.start(display)

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


    while (display.tracker.running and display.running):
        #if tracker.frameCounter == 10:
            #tracker.resetToMotion = True
            #print "reset to motion"
        messages = client.messages.list(date_sent=datetime.datetime.today())
        for message in messages:
            if (message.direction == "inbound"):
                #New message from now onward that hasn't already been processed
                if message.sid not in processedIDs and datetime.datetime.now() <= message.date_created:
                    currentMessage = Message(message.sid, message.from_, message.to, message.body)
                    print "New Text Message:", currentMessage

                    #print(len(message.body))
                    #if len(message.body) > 70:         #Large text messages get split up, also blocks the display
                    #    continue
                    if (message.body.lower() == "reset" or message.body.lower() == "r") and display.mode == "text":
                        display.tracker.resetTrackingPosition()
                        display.drawSentence(str(display.tracker.reportPosition()) + "  ")
                        #pass
                    elif (message.body.lower() == "print" or message.body.lower() == "p") and display.mode == "text":
                        display.drawSentence(str(display.tracker.reportPosition()) + "  ")
                        #pass
                    elif (message.body.lower() == "clear"):
                        display.clear()
                    elif message.body.lower() == "crazy" and display.mode == "text":
                        display.crazyColorMode = not display.crazyColorMode     #Toggle Crazy Color Mode
                    elif message.body.lower()[0:5] == "speed" and len(message.body) > 6:
                        display.fps = int(message.body.split(' ')[1])
                        if display.mode == "text":
                            display.drawSentence("fps:" + str(display.fps))

                    #elif message.body.lower() == "speed down":
                    #    display.fps -= 1
                    elif message.body.lower() == "track":
                        display.mode = "track"
                    elif message.body.lower() == "text":
                        display.mode = "text"
                    elif (message.body[0] == "0"):
                        x, y = [int(x) for x in message.body[1:].split(',')]
                        display.tracker.setTrackingPosition(x,y,30,30)
                        display.drawSentence(str(display.tracker.reportPosition()) + "  ")
                    elif message.body.lower() == "reset to motion":
                        display.mode = "track"
                        #display.tracker.resetToMotion = True
                    elif message.body.lower()[0] == "w" and display.mode == "text":
                        display.drawSentence(message.body[1:] + " ")

                    processedIDs.append(message.sid)
                    processedMessages.append(currentMessage)
        time.sleep(1)

    #Close down the main loops of the threads
    #tracker.running = False
    display.running = False


if __name__ == "__main__":
    main()
