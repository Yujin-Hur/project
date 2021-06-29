from colorsys import hsv_to_rgb
import board
from digitalio import DigitalInOut, Direction
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
import math

# MATH
D2R = math.pi/180
R2D = 180/math.pi
g = 9.806
dt = 0.5

class Rod():

    def __init__(self, x, y):

        self.length = 100  
        self.width = 12
        self.color = '#d6d6d6'
        self.theta = 10 * D2R    
        self.dt = 0.5
        self.crodx = x + 30
        self.crody = y + 30
        self.rodx = self.crodx + self.length * math.sin(self.theta)
        self.rody = self.crody - self.length * math.cos(self.theta)
        self.line = [(self.rodx, self.rody), (self.crodx, self.crody)]
             
    def move(self, x, y):           # rod's gravity move

        self.crodx = x + 30
        self.crody = y + 30
        ds = g * math.tan(self.theta)*dt*dt*5
        self.rodx = self.rodx + ds
        self.theta = math.asin((self.rodx-self.crodx)/self.length)
        self.rody = self.crody - self.length*math.cos(self.theta)
        self.line = [(self.rodx, self.rody), (self.crodx, self.crody)]

    def left(self):

        da = 2.5 * math.tan(self.theta)*dt*dt
        self.rodx += da
        self.theta = math.asin((self.rodx-self.crodx)/self.length)
        self.rody = self.crody - self.length*math.cos(self.theta)
        self.line = [(self.rodx, self.rody), (self.crodx, self.crody)]

    def right(self):

        da = 2.5 * math.tan(self.theta)*dt*dt
        self.rodx -= da
        self.theta = math.asin((self.rodx-self.crodx)/self.length)
        self.rody = self.crody - self.length*math.cos(self.theta)
        self.line = [(self.rodx, self.rody), (self.crodx, self.crody)]