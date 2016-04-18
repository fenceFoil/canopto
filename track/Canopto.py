import threading
from random import randint
import blinkstick.blinkstick as blinkstick
import numpy
import pygame
from PersonTracker import PersonTracker

class Canopto(threading.Thread):
    'The Matrix of LEDs that make up the display'
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    def __init__(self, width=8, height=8, previewEnabled=True, useGamma=False, backgroundColor=(0, 0, 0), fontColor = (255, 255, 255), tracker = None):
        threading.Thread.__init__(self)
        self.width = width
        self.height = height
        self.previewEnabled = previewEnabled
        self.useGamma = useGamma
        self.matrix = numpy.zeros((self.height, self.width), dtype=(float, 3))
        self.conversionMatrix = [
            [12, 15, 31, 30, 46, 47, 62, 63],
            [13, 14, 28, 29, 45, 44, 61, 60],
            [8, 11, 26, 27, 42, 43, 58, 59],
            [9, 10, 24, 25, 41, 40, 57, 56],
            [4, 7, 23, 22, 38, 39, 54, 55],
            [5, 6, 21, 20, 37, 36, 53, 52],
            [0, 3, 18, 19, 34, 35, 50, 51],
            [1, 2, 17, 16, 33, 32, 49, 48],
        ]
        self.gamma = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1,
                      1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 4,
                      4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 9, 9, 9,
                      10, 10, 10, 11, 11, 11, 12, 12, 13, 13, 13, 14, 14, 15, 15, 16, 16,
                      17, 17, 18, 18, 19, 19, 20, 20, 21, 21, 22, 22, 23, 24, 24, 25, 25,
                      26, 27, 27, 28, 29, 29, 30, 31, 32, 32, 33, 34, 35, 35, 36, 37, 38,
                      39, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 50, 51, 52, 54,
                      55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 66, 67, 68, 69, 70, 72, 73,
                      74, 75, 77, 78, 79, 81, 82, 83, 85, 86, 87, 89, 90, 92, 93, 95, 96,
                      98, 99, 101, 102, 104, 105, 107, 109, 110, 112, 114, 115, 117, 119,
                      120, 122, 124, 126, 127, 129, 131, 133, 135, 137, 138, 140, 142,
                      144, 146, 148, 150, 152, 154, 156, 158, 160, 162, 164, 167, 169,
                      171, 173, 175, 177, 180, 182, 184, 186, 189, 191, 193, 196, 198,
                      200, 203, 205, 208, 210, 213, 215, 218, 220, 223, 225, 228, 231,
                      233, 236, 239, 241, 244, 247, 249, 252, 255]

        # Colors
        self.backgroundColor = self.toGamma(backgroundColor)
        self.fontColor = self.toGamma(fontColor)
        self.defaultBackgroundColor = self.toGamma(backgroundColor)
        self.defaultFontColor = self.toGamma(fontColor)

        self.crazyColorMode = False

        # Only works for 8 columns
        if (self.width > 8):
            print("!!!!WARNING: UNSUPPORTED NUMBER OF COLUMNS!!!")

        # Blinkstick init
        self.bs = blinkstick.BlinkStickPro(width * height, 0, 0, 0.002, 255)
        self.bs.connect()

        self.mode = "text"
        #self.mode = "track"

        # PyGame is used for drawing
        self.running = True
        pygame.init()
        self.clock = pygame.time.Clock()
        if self.previewEnabled:
            # Pygame init
            self.SCREEN = pygame.display.set_mode((400, 400), 0, 32)
            self.characterSpriteSheet = pygame.image.load('res/7x5fontHD44780.png').convert_alpha()
            # self.characterSpriteSheet = pygame.image.load('res/8x8CGACodePage.png').convert(8)
            # self.characterSpriteSheet = pygame.image.load('res/7x4fonttrans.png').convert(8)
            # self.characterArray = surfarray.array3d(self.characterSpriteSheet)


    def makeSentence(self, sentence, charWidth=5, charHeight=8):
        resultImage = pygame.Surface((len(sentence) * (charWidth + 1), charHeight))
        count = 0;
        for c in sentence:
            resultImage.blit(self.getChar(c, charWidth, charHeight), (count * (charWidth + 1), 0),
                             (0, 0, charWidth, charHeight))
            count += 1
        return resultImage


    def getChar(self, char, charWidth=5, charHeight=7):
        charValue = ord(char)

        col = int(charValue % 32)
        row = int(charValue / 32)

        # col = int(charValue % 97) % 10
        # row = int(int(charValue % 97) / 10)
        #print("ascii:", charValue, "  char:", char, "   loc:", (col, row), "loc:", (col * charWidth, row * charHeight))
        charImage = pygame.Surface((charWidth, charHeight))

        # set the background color
        charImage.fill(self.backgroundColor)

        # Crop character from spritesheet
        charImage.blit(self.characterSpriteSheet, (0, 0), (col * charWidth, row * charHeight, charWidth, charHeight))

        # set the font color
        charImage = self.colorReplace(charImage, (255, 255, 255), self.fontColor)

        return charImage


    def updatePreview(self):
        # draw pixels onto pygame window
        if self.previewEnabled:
            # reset pygame window
            self.SCREEN.fill(self.BLACK)

            for y in range(0, self.height):
                for x in range(0, self.width):
                    # Draw circular pixels
                    pygame.draw.circle(self.SCREEN, self.matrix[y][x], (x * 20 + 100, y * 20 + 100), 9)

                    # Draw pixel boundaries
                    borderRect = pygame.Rect((x * 20 + 90, y * 20 + 90), (20, 20))
                    pygame.draw.rect(self.SCREEN, ([75] * 3), borderRect, 1)
            self.updateScreen()


    def softToHardPixel(self, x, y):
        'Convert a software pixel (x, y) to the hardware pixel index'
        # 16 or width*height*(x//2) selects a 2-can-wide xumn of lights
        # (((height-1)-y)//4) selects a cell of 4 cans
        # (y%2) adds one if the y is odd
        # (x%2) is true for the second xumn of cans in a cell
        # (1+((y+1)%2)) adds 1 for the lower right can in a cell, and adds one more for the upper right can in a cell
        # return (self.width * self.height) * (x // 2) + (((self.height - 1) - y) // 2) * 4 + (y % 2) + (x % 2) * (
        # 3 - 2 * ((y) % 2))
        # print(x, y, self.conversionMatrix[y][x])
        return self.conversionMatrix[y][x]


    def setPixel(self, x, y, color=(255, 255, 255)):
        self.matrix[y][x] = color
        curved_color = self.toGamma(color)
        self.bs.set_color(0, self.softToHardPixel(x, y), *curved_color)
        self.bs.send_data(0)



    def toGamma(self, color):
        if self.useGamma:
            return (self.gamma[int(color[0])], self.gamma[int(color[1])], self.gamma[int(color[2])])
        return color


    def getPixel(self, x, y):
        return self.matrix[y][x]


    def drawSurface(self, surface):
        if (surface.get_width() < self.width): return
        for x in range(0, self.width):
            for y in range(0, self.height):
                color = surface.get_at((x, y))
                self.matrix[y][x] = (color.r, color.g, color.b)
                curved_color = color
                if self.useGamma:
                    curved_color = (self.gamma[int(color[0])], self.gamma[int(color[1])], self.gamma[int(color[2])])
                self.bs.set_color(0, self.softToHardPixel(x, y), *curved_color)
        self.bs.send_data(0)

    def randomColor(self):
        return self.toGamma((randint(0, 255), randint(0, 255), randint(0, 255)))

    # http://stackoverflow.com/questions/5891808/how-to-invert-colors-of-an-image-in-pygames
    def invertImage(self, img):
        inv = pygame.Surface(img.get_rect().size, pygame.SRCALPHA)
        inv.fill((255, 255, 255, 255))
        inv.blit(img, (0, 0), None, pygame.BLEND_RGB_SUB)
        return inv

    # http://stackoverflow.com/questions/15076133/pygame-edit-colours-of-an-image-makes-white-red-at-255-0-0-without-numerical
    def colorReplace(self, surface, find_color, replace_color):
        for x in range(surface.get_size()[0]):
            for y in range(surface.get_size()[1]):
                if surface.get_at([x, y]) == find_color:
                    surface.set_at([x, y], replace_color)
        return surface

    def resetColors(self):
        self.backgroundColor = self.defaultBackgroundColor
        self.fontColor = self.defaultFontColor

    def drawSentence(self, string):
        self.sentenceBuffer = "  " + str(string)

    def clear(self):
        self.sentence = " "
        self.sentenceBuffer = "  "
        self.matrix = numpy.zeros((self.height, self.width), dtype=(float, 3))
        #self.SCREEN.fill(self.BLACK)
        self.updateScreen()
        self.updatePreview()

    def run(self):
        print "Running Canopto"
        self.clear()

        #Initialize Person Tracker
        self.tracker = PersonTracker()
        PersonTracker.start(self.tracker)

        self.fps = 16
        defaultTextSpeed = 16
        defaultTrackSpeed = 60
        self.sentenceBuffer = ""
        self.sentence = ""
        deltaChars = 1
        self.crazyColorMode = False
        self.sentenceSurface = self.makeSentence(self.sentence)
        loopCount = 0

        while self.running:
            for event in pygame.event.get():
                if hasattr(event, 'key') and event.key == 27:
                    self.running = False
                    break

            if self.mode == "text":
                if self.fps is not defaultTextSpeed: self.fps = defaultTextSpeed
                self.drawSurface(self.sentenceSurface)
                self.sentenceSurface.scroll(dx=-deltaChars)
                loopCount += 1
                # If a char just passed by
                if (loopCount % 6 == 0):
                    if self.crazyColorMode:
                        self.backgroundColor = self.randomColor() #Uncomment to make every character have a different background color
                    self.sentence = self.sentence + self.sentenceBuffer
                    self.sentence = self.sentence[deltaChars:]
                    self.sentenceBuffer = ""
                    self.sentenceSurface = self.makeSentence(self.sentence)
            elif self.mode == "track" and self.tracker is not None:
                #if not self.tracker.resetToMotion: self.tracker.resetToMotion = True
                if self.fps is not defaultTrackSpeed:
                    self.fps = defaultTrackSpeed
                    self.tracker.resetToMotion = True
                #print "Person Location:", self.tracker.personLocation
                x, y = self.tracker.personLocation
                #self.clear()
                self.matrix = numpy.zeros((self.height, self.width), dtype=(float, 3))
                #x varies from 0 to 255 so make bins of ~30 by dividing 255 by the width of the display(8 cans)
                self.setPixel(numpy.clip(int((x) / (255/self.width+2)), 0, 7), 5)
                self.setPixel(numpy.clip(int((x) / (255/self.width+2)), 0, 7), 6)
                self.setPixel(numpy.clip(int((x) / (255/self.width+2)), 0, 7), 7)



            self.updatePreview()
            self.updateScreen()
            self.clock.tick(self.fps)
        self.clear()

    def updateScreen(self):
        # update the screen!
        pygame.display.update()  # Main




if __name__ == "__main__":
    CANOPTO = Canopto(8, 8, previewEnabled=True, useGamma=True)
    CANOPTO.start()
    #time.sleep(1)
    #CANOPTO.drawSentence("Hello")
