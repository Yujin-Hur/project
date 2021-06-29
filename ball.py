from colorsys import hsv_to_rgb
import board
from digitalio import DigitalInOut, Direction
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
import random
import time

class Ball():
    def __init__(self):
        self.imgA = Image.open('image/BallA.png')
        self.imgB = Image.open('image/BallB.png')
        self.imgF = Image.open('image/BallF.png')
        self.img = Image.open('image/BallF.png')
        
        self.size = 50
        self.x = random.randrange(40,200)
        self.y = 0
        self.ds = 2

        self.time = time.time()     # create time
        self.score = 0

        self.random_image = random.randrange(1,4)

        if self.random_image == 1 :
            self.img = Image.open('image/BallA.png')
            self.score = 20
        elif self.random_image == 2 :
            self.img = Image.open('image/BallB.png')
            self.score = 10
        else:
            self.img = Image.open('image/BallF.png')
            self.score = -10
        self.img = self.img.resize((self.size,self.size))

    def move(self):
        if self.y < 100:
            self.y += self.ds
            return 1
        else:
            if (time.time() - self.time) > 5:
                return 0

    def check(self, rodx, rody):

        if (abs(self.x - rodx) < self.size-5):
            if(abs(self.y - rody) < self.size):

                return 0
        else:
            return 1
  