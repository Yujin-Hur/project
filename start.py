from colorsys import hsv_to_rgb
import board
from digitalio import DigitalInOut, Direction
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
import time
import math
import random

from professor import Prof
from rod import Rod
from ball import Ball
from game import Game

# Create the display
cs_pin = DigitalInOut(board.CE0)
dc_pin = DigitalInOut(board.D25)
reset_pin = DigitalInOut(board.D24)
BAUDRATE = 24000000

spi = board.SPI()
disp = st7789.ST7789(
    spi,
    height=240,
    y_offset=80,
    rotation=180,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
)

button_L = DigitalInOut(board.D27)
button_L.direction = Direction.INPUT

button_R = DigitalInOut(board.D23)
button_R.direction = Direction.INPUT

button_A = DigitalInOut(board.D5)
button_A.direction = Direction.INPUT

button_B = DigitalInOut(board.D6)
button_B.direction = Direction.INPUT

# Turn on the Backlight
backlight = DigitalInOut(board.D26)
backlight.switch_to_output()
backlight.value = True

# Create blank image for drawing. (240, 240)
width = disp.width
height = disp.height

image = Image.new("RGB", (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Clear display.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image)

# Font
fnt0 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15)
fnt1 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
fnt2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)

# Math
D2R = math.pi/180
R2D = 180/math.pi
g = 9.806
dt = 0.5

while True:
    
    game = Game(draw, image, disp)
    prof = Prof()
    rod = Rod(prof.x,prof.y)
    balls = []

    draw.rectangle((0, 0, 240, 240), outline=0, fill=0)
    image.paste(prof.img,(prof.x,prof.y))
    game.start()
    

    while game.control(rod.theta):
        
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        draw.text((5, 20), str(game.score), font=fnt1, fill="#00FF00")
        draw.text((5, 50), str(round(game.time,1)), font=fnt1, fill="#00FF00")

        # Prof, Rod
        rod.move(prof.x,prof.y) 

        if not button_R.value:  # right pressed    
            prof.right()
            rod.right()
    
        if not button_L.value:  # left pressed    
            prof.left()
            rod.left()


        # Ball
        if (time.time() - game.ball_time) > 3:
            ball = Ball()
            balls.append(ball)
            game.ball_time = time.time()

                
        for ball in balls:

            if( ball.check(rod.rodx, rod.rody)== 0):
                game.score += ball.score
                del balls[0]

            elif(ball.move() == 0):
                del balls[0]
                
            image.paste(ball.img,(ball.x,ball.y))


        draw.line(rod.line, rod.color, rod.width)
        draw.ellipse((rod.rodx-6,rod.rody-6 , rod.rodx+6, rod.rody+6),fill='#FF0000')
        image.paste(prof.img,(prof.x,prof.y))

        # Display image.
        disp.image(image)
        time.sleep(0.001)

    disp.image(image)
    game.reset(prof, rod)