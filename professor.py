from colorsys import hsv_to_rgb
import board
from digitalio import DigitalInOut, Direction
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789


class Prof():

    def __init__(self):
        self.img = Image.open('image/prof2.png')
        self.size = 60
        self.x = 100
        self.y = 200
        self.ds = 10   
        self.img = self.img.resize((self.size, self.size))

    def left(self):
        if self.x > -self.size/2:
            self.x -= self.ds
    
    def right(self):
        if self.x < 240 - self.size/2:
            self.x += self.ds