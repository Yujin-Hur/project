from colorsys import hsv_to_rgb
import board
from digitalio import DigitalInOut, Direction
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
import time

fnt0 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15)
fnt1 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
fnt2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)

button_A = DigitalInOut(board.D5)
button_A.direction = Direction.INPUT
button_B = DigitalInOut(board.D6)
button_B.direction = Direction.INPUT

class Game():

    def __init__(self, draw, image, disp):

        self.draw = draw
        self.image = image
        self.disp = disp

        self.score = 0
        self.limit_score = 60
        self.start_time = time.time()
        self.time = time.time() - self.start_time
        self.ball_time = time.time()
        self.limit_time = 35

    def start(self):
        
        self.draw.text((5, 100), "Get Your Score!", font=fnt2, fill="#00FF00")
        self.draw.text((45, 140), "Press #5 to Start", font=fnt1, fill="#00FF00")
        self.disp.image(self.image)

        while (button_A.value):      
            time.sleep(0.1)

        self.draw.rectangle((0, 0, 240, 180), outline=0, fill=0)
        self.draw.text((50, 100), "S T A R T !", font=fnt2, fill="#00FF00")
        self.draw.text((50, 140), "Get 60 in 35sec", font=fnt1, fill="#00FF00")

        self.disp.image(self.image)
        time.sleep(1)


    def fail(self, message):
        self.draw.rectangle((0, 0, 240, 240), outline=0, fill=0)
        self.draw.text((5, 100), message, font=fnt2, fill="#00FF00")
        self.draw.text((45, 220), "THX to Professor Kim ", font=fnt0, fill="#00FF00")
        self.draw.text((45, 140), "Press #6 to Reset ", font=fnt1, fill="#00FF00")
       
        
    def success(self):
        self.draw.rectangle((0, 0, 240, 240), outline=0, fill=0)
        self.draw.text((5, 100), "S U C E S S!", font=fnt2, fill="#00FF00")
        self.draw.text((45, 220), "THX to Professor Kim ", font=fnt0, fill="#00FF00")
        self.draw.text((45, 140), "Press #6 to Reset ", font=fnt1, fill="#00FF00")
     
    
    def reset(self, Professor, Rod):    
        while (button_B.value):      
            time.sleep(0.1)
        del Professor
        del Rod
            

    def control(self, theta):
        self.time = time.time() - self.start_time
    
        if self.time > self.limit_time:  
            self.fail("Time Out")
            return 0

        if theta > 0.9 or theta < -0.9:
            self.fail("Game Over")
            return 0

        if self.score >= self.limit_score:
            self.success()
            return 0

        else:
            return 1