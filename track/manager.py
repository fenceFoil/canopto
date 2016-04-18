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
    display.clear()

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

    startTime = datetime.datetime.now() + datetime.timedelta(hours=4)

    while (display.running): #display.tracker.running):
        #if tracker.frameCounter == 10:
            #tracker.resetToMotion = True
            #print "reset to motion"

        #Because of a conflict between timezones used to represent dates cannot limit by day since messages sent after
        #~10pm will, according to server, be sent tomorrow thereby not having them show up as new messages if limited by today
        #date_sent=datetime.datetime.today()
        messages = client.messages.list()
        for message in messages:
            if (message.direction == "inbound"):
                #New message from now onward that hasn't already been processed
                if message.sid not in processedIDs and message.date_created > startTime:
                    currentMessage = Message(message.sid, message.from_, message.to, message.body)
                    print "New Text Message:", currentMessage

                    #print(len(message.body))
                    #if len(message.body) > 70:         #Large text messages get split up, also blocks the display
                    #    continue

                    if (message.body.lower() == "reset" or message.body.lower() == "r") and display.mode == "text":
                        display.tracker.resetTrackingPosition()
                        display.drawSentence(str(display.tracker.reportPosition()) + "  ")
                        client.messages.create(to=message.from_, from_=message.to, body=str(display.tracker.reportPosition()))
                        #pass
                    elif (message.body.lower() == "print" or message.body.lower() == "p") and display.mode == "text":
                        display.drawSentence(str(display.tracker.reportPosition()) + "  ")
                        client.messages.create(to=message.from_, from_=message.to, body=str(display.tracker.reportPosition()))
                        #pass
                    elif (message.body.lower() == "clear"):
                        display.clear()
                    elif message.body.lower() == "crazy" and display.mode == "text":
                        display.crazyColorMode = not display.crazyColorMode     #Toggle Crazy Color Mode
                        if not display.crazyColorMode:
                            #reset colors to normal
                            display.resetColors()
                        client.messages.create(to=message.from_, from_=message.to, body="Crazy Mode: " + str(display.crazyColorMode))
                    elif message.body.lower() == "nocrazy":
                        display.crazyColorMode = False
                        client.messages.create(to=message.from_, from_=message.to, body="Crazy Mode: " + str(display.crazyColorMode))
                    elif message.body.lower()[0:5] == "speed" and len(message.body) > 6:
                        display.fps = int(message.body.split(' ')[1])
                        if display.mode == "text":
                            display.drawSentence("fps:" + str(display.fps))
                        client.messages.create(to=message.from_, from_=message.to, body="fps:" + str(display.fps))
                    elif message.body.lower() == "track":
                        display.mode = "track"
                        client.messages.create(to=message.from_, from_=message.to, body="Display Mode = track" )
                    elif message.body.lower() == "text":
                        display.mode = "text"
                        client.messages.create(to=message.from_, from_=message.to, body="Display Mode = text" )
                    elif (message.body[0] == "0"):
                        x, y = [int(x) for x in message.body[1:].split(',')]
                        display.tracker.setTrackingPosition(x,y,30,30)

                        display.drawSentence(str(display.tracker.reportPosition()) + "  ")
                    elif message.body.lower() == "reset to motion":
                        display.mode = "track"
                        client.messages.create(to=message.from_, from_=message.to, body="Refocusing to motion" )
                    elif message.body.lower() == "refocus":
                        display.mode = "track"
                        display.tracker.resetToMotion = True
                        client.messages.create(to=message.from_, from_=message.to, body="Refocusing to motion" )
                    elif message.body.lower()[0:6] == "bcolor":
                        rgb = [int(i) for i in message.body.lower().split(' ')[1].split(',')]
                        print "New background color:", rgb
                        display.backgroundColor = display.toGamma(rgb)
                        client.messages.create(to=message.from_, from_=message.to, body="Background color is now " + str(display.backgroundColor) )
                    elif message.body.lower()[0:6] == "fcolor":
                        rgb = [int(i) for i in message.body.lower().split(' ')[1].split(',')]
                        print "New font color:", rgb
                        display.fontColor = display.toGamma(rgb)
                        client.messages.create(to=message.from_, from_=message.to, body="Font color is now " + str(display.fontColor) )
                    elif message.body.lower()[0] == "w" and display.mode == "text":
                        display.drawSentence(message.body[1:] + " ")
                        client.messages.create(to=message.from_, from_=message.to, body="Writing: " + str(message.body[1:]) )
                    elif message.body.lower() == "resetbs":
                        display.tracker.resetBS = True
                        client.messages.create(to=message.from_, from_=message.to, body="Resetting background subtractor" )
                    elif message.body.lower() == "options" or message.body.lower() == "help":
                        client.messages.create(to=message.from_, from_=message.to, body="""if (message.body.lower() == "reset" or message.body.lower() == "r") and display.mode == "text":
                        elif (message.body.lower() == "print" or message.body.lower() == "p") and display.mode == "text":
                        elif (message.body.lower() == "clear"):
                        elif message.body.lower() == "crazy" and display.mode == "text":
                        elif message.body.lower() == "nocrazy":
                        elif message.body.lower()[0:5] == "speed" and len(message.body) > 6:
                        elif message.body.lower() == "track":
                        elif message.body.lower() == "text":
                        elif (message.body[0] == "0"): display.tracker.setTrackingPosition(x,y,30,30)
                        elif message.body.lower() == "reset to motion":
                        elif message.body.lower() == "refocus":
                        elif message.body.lower()[0:6] == "bcolor":
                        elif message.body.lower()[0:6] == "fcolor":
                        elif message.body.lower()[0] == "w" and display.mode == "text":
                        elif message.body.lower() == "resetbs":""")

                    processedIDs.append(message.sid)
                    processedMessages.append(currentMessage)
        time.sleep(1)

    #Close down the main loops of the threads
    #tracker.running = False
    display.clear()
    display.running = False


if __name__ == "__main__":
    main()
