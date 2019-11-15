import ST7735 as TFT
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
from time import sleep, time

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


class Lcd:
    def __init__(self):
        self.WIDTH = 128
        self.HEIGHT = 160
        self.display = TFT.ST7735(24, rst=25, spi=SPI.SpiDev(0, 0, max_speed_hz=4000000))
        self.font1 = ImageFont.truetype('HelveticaBlkIt.ttf', 24)
        self.label_font = ImageFont.truetype('HelveticaBlkIt.ttf', 12)

        self.display.begin()
        self.signal_state = ''
        self.flash = False
        # Load an image.
        image = Image.open('/home/pi/Zigbee-signal-indicator/logo.jpg').rotate(0).resize((self.WIDTH, self.HEIGHT))
        self.display.display(image)
        self.draw = self.display.draw()

    @staticmethod
    def draw_rotated_text(image, text, position, angle, font, fill=(255, 255, 255)):
        # Get rendered font width and height.
        draw = ImageDraw.Draw(image)
        width, height = draw.textsize(text, font=font)
        # Create a new image with transparent background to store the text.
        textimage = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        # Render the text.
        textdraw = ImageDraw.Draw(textimage)
        textdraw.text((0, 0), text, font=font, fill=fill)
        # Rotate the text image.
        rotated = textimage.rotate(angle, expand=1)
        # Paste the text into the image, using it as a mask for transparency.
        image.paste(rotated, position, rotated)

    def redraw(self, channel, state='N/A', lqi='N/A', rssi='N/A', power=None):
        if self.flash:
            return
        print("redraw")
        self.display.clear()
        self.draw_rotated_text(self.display.buffer, state, (10, 10), 0, self.font1, fill=(0, 0, 255))
        if state == 'Poor':
            self.draw.rectangle((8, 40, 50, 60), outline=(0, 0, 255), fill=(0, 0, 255))
        elif state == 'Bad':
            self.draw.rectangle((8, 40, 50, 60), outline=(0, 0, 255), fill=(0, 0, 255))
            self.draw.rectangle((50, 40, 70, 60), outline=(0, 110, 255), fill=(0, 110, 255))
        elif state == 'Good':
            self.draw.rectangle((8, 40, 50, 60), outline=(0, 0, 255), fill=(0, 0, 255))
            self.draw.rectangle((50, 40, 70, 60), outline=(0, 110, 255), fill=(0, 110, 255))
            self.draw.rectangle((70, 40, 90, 60), outline=(0, 245, 255), fill=(0, 245, 255))
        else:
            self.draw.rectangle((8, 40, 50, 60), outline=(0, 0, 255), fill=(0, 0, 255))
            self.draw.rectangle((50, 40, 70, 60), outline=(0, 110, 255), fill=(0, 110, 255))
            self.draw.rectangle((70, 40, 90, 60), outline=(0, 245, 255), fill=(0, 245, 255))
            self.draw.rectangle((90, 40, 118, 60), outline=(0, 255, 0), fill=(0, 255, 0))
        self.signal_state = state

        if not (power is None):
            self.draw_rotated_text(self.display.buffer, 'POWER', (10, 75), 0, self.label_font, fill=(0, 255, 0))
            if power > 0:
                self.draw_rotated_text(self.display.buffer, "+" + str(power), (75, 65), 0, self.font1, fill=(255, 255, 255))
            else:
                self.draw_rotated_text(self.display.buffer, str(power), (75, 65), 0, self.font1, fill=(255, 255, 255))

        self.draw_rotated_text(self.display.buffer, 'CHANNEL', (10, 100), 0, self.label_font, fill=(0, 255, 0))
        self.draw_rotated_text(self.display.buffer, str(channel), (75, 90), 0, self.font1, fill=(255, 255, 255))
        self.draw_rotated_text(self.display.buffer, 'LQI', (10, 120), 0, self.label_font, fill=(0, 255, 0))
        self.draw_rotated_text(self.display.buffer, lqi, (10, 130), 0, self.font1, fill=(255, 255, 255))
        self.draw_rotated_text(self.display.buffer, 'RSSI', (70, 120), 0, self.label_font, fill=(0, 255, 0))
        self.draw_rotated_text(self.display.buffer, rssi, (70, 130), 0, self.font1, fill=(255, 255, 255))
        self.display.display()
        self.flash = True

    def setflash(self, ref=False):
        self.flash = ref
