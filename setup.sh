sudo apt-get update

# fix boot 
sudo systemctl disable apt-daily.service


# install py3
sudo apt-get install -y vim git
sudo apt-get install -y python3-gpiozero python3-serial python3-pip libatlas-base-dev pigpio python-pigpio python3-pigpio

# get source code
git clone https://github.com/rewrite404/Zigbee-signal-indicator.git

# install lcd driver
cd ~/Zigbee-signal-indicator/driver
sudo apt-get install -y build-essential python3-dev python3-smbus python3-pip python3-pil python3-numpy
sudo pip3 install RPi.GPIO
sudo pip3 install Adafruit_GPIO
sudo pip3 install Adafruit_BBIO
sudo python3 setup.py install

# Created symlink /etc/systemd/system/multi-user.target.wants/pigpiod.service → /lib/systemd/system/pigpiod.service.
sudo systemctl enable pigpiod 

# install font
cd ~/Zigbee-signal-indicator
sudo apt-get install -y fontconfig
sudo cp HelveticaBlkIt.ttf /usr/share/fonts/truetype

# define /etc/rc.local to run py script
>> sudo python3 /home/pi/Zigbee-signal-indicator/ZSI.py &

sudo apt-get clean
sudo apt-get autoremove --purge
