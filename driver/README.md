Adafruit ST7735R Library
=======================

Python library to control an [Adafruit 1.44" Color TFT LCD Display with MicroSD Card breakout - ST7735R](https://www.adafruit.com/product/2088)
This library was adapted from cskau/Python_ST7735 which had already been adapted from
adafruit/Adafruit_Python_ILI9341. Despite having dimensions of 128x128, the Adafruit display
requires a 132x132 image to be written to the frame memory. This fork resolves issues users
were having with multiple dead pixel rows by including an image buffer that fills in this extra
space.

Designed specifically to work with the Adafruit display listed above.

No SD card functionality has been built in to this library.

For all platforms (Raspberry Pi and Beaglebone Black) make sure you have the following dependencies:

````
sudo apt-get update
sudo apt-get install build-essential python-dev python-smbus python-pip python-imaging python-numpy
````

For a Raspberry Pi make sure you have the RPi.GPIO and Adafruit GPIO libraries by executing:

````
sudo pip install RPi.GPIO
sudo pip install Adafruit_GPIO
````

For a BeagleBone Black make sure you have the Adafruit_BBIO library by executing:

````
sudo pip install Adafruit_BBIO
````

Install the library by downloading with the download link on the right, unzipping the archive, navigating inside the library's directory and executing:

````
sudo python setup.py install
````

See example of usage in the examples folder.

Adafruit invests time and resources providing this open source code, please support Adafruit and open-source hardware by purchasing products from Adafruit!

Modified from 'Adafruit Python ILI9341' written by Tony DiCola for Adafruit Industries.
Modified in turn from 'Python ST7735' written by cskau.

MIT license, all text above must be included in any redistribution
