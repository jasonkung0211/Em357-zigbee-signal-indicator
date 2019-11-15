from gpiozero import Button
from signal import pause
from time import sleep, time

import serial as serial
import threading
import queue
import statistics
from enum import Enum
from lcd import Lcd
from buzzer import Buzzer


class Mode(Enum):
    START_MODE = '@'
    STOP_MODE = '#'
    CHANNEL_MODE = '$'
    IDLE_MODE = '%'
    HOLD_MODE = '^'
    POWER_MODE = '&'


class SerialProcess:
    def in_Waiting(self):
        return self.zigbee_uart.inWaiting()

    def flush_Input(self):
        self.zigbee_uart.flushInput()
        return

    def flush_Output(self):
        self.zigbee_uart.flushOutput()
        return

    def __init__(self):
        self.zigbee_uart = serial.Serial(port='/dev/ttyAMA0',
                                         baudrate=115200,
                                         parity=serial.PARITY_NONE,
                                         stopbits=serial.STOPBITS_ONE,
                                         bytesize=serial.EIGHTBITS,
                                         writeTimeout=5,
                                         rtscts=True,
                                         timeout=5)

        if self.zigbee_uart.is_open:
            input_queue.put('setchannel '+format(channel, 'X'))
            if is_tx():
                input_queue.put('setTxPowMode 1 0')
                input_queue.put('settxpower ' + format(power, 'X'))
                input_queue.put("setTxLength 6")
                input_queue.put("setTxPayload 0 0x1b 0x61 0x98 0x00")
            else:
                input_queue.put("showPayload 1")

        input_queue.put('e')

    def is_open(self):
        return self.zigbee_uart.isOpen()

    def close(self):
        self.zigbee_uart.close()

    def write(self, data):
        print("> " + data)
        data += '\r\n'
        self.zigbee_uart.write(data.encode())

    def read(self):
        data = self.zigbee_uart.readline().strip().decode('utf8')
        return data


def is_tx():
    return not jmp.is_pressed


def set_power():
    global current_mode, power
    if current_mode != Mode.POWER_MODE:
        return

    input_queue.put('settxpower ' + format(power, 'X'))
    current_mode = Mode.HOLD_MODE
    buzzer.prog()
    lcd.setflash()


def power_mode():
    if not is_tx():
        return

    global current_mode, power
    if current_mode == Mode.START_MODE:
        return
    elif current_mode == Mode.HOLD_MODE:
        current_mode = Mode.IDLE_MODE
        return

    current_mode = Mode.POWER_MODE

    power += 1
    if power == 9:
        power = -8

    buzzer.set()
    lcd.setflash()


def set_channels():
    global current_mode, channel
    if current_mode != Mode.CHANNEL_MODE:
        return

    input_queue.put('setchannel ' + format(channel, 'X'))
    current_mode = Mode.HOLD_MODE
    buzzer.prog()
    lcd.setflash()


def channels():
    global current_mode, channel
    if current_mode == Mode.START_MODE:
        return
    elif current_mode == Mode.HOLD_MODE:
        current_mode = Mode.IDLE_MODE
        return

    current_mode = Mode.CHANNEL_MODE

    channel += 1
    if channel == 27:
        channel = 11

    buzzer.set()
    lcd.setflash()


def stop():
    btn_start.when_released = None
    global current_mode
    if current_mode == Mode.START_MODE:
        current_mode = Mode.STOP_MODE
        input_queue.put('e')

    buzzer.set()
    lcd.setflash()
    btn_start.when_released = start


def start():
    btn_start.when_released = None
    global current_mode

    if current_mode == Mode.CHANNEL_MODE:
        input_queue.put('setchannel ' + format(channel, 'X'))
        if is_tx():
            input_queue.put('settxpower ' + format(power, 'X'))

    if current_mode == Mode.POWER_MODE:
        input_queue.put('setchannel ' + format(channel, 'X'))
        if is_tx():
            input_queue.put('settxpower ' + format(power, 'X'))

    if current_mode != Mode.START_MODE:
        current_mode = Mode.START_MODE
        if is_tx():
            input_queue.put('tx 0')
        else:
            input_queue.put('rx')

    buzzer.set()
    lcd.setflash()
    btn_start.when_released = stop


def io_jobs():
    sp.flush_Input()
    sp.flush_Output()

    rssi = []
    lqi = []
    while sp.is_open():

        if current_mode == Mode.STOP_MODE:
            if is_tx():
                lcd.redraw(channel, 'STOP', 'N/A', 'N/A', power)
            else:
                lcd.redraw(channel, 'STOP', 'N/A', 'N/A')
        elif current_mode == Mode.POWER_MODE:
            if is_tx():
                lcd.redraw(channel, 'POWER', 'N/A', 'N/A', power)
            else:
                lcd.redraw(channel, 'POWER', 'N/A', 'N/A')
        elif current_mode == Mode.CHANNEL_MODE:
            if is_tx():
                lcd.redraw(channel, 'CHANNEL', 'N/A', 'N/A', power)
            else:
                lcd.redraw(channel, 'CHANNEL', 'N/A', 'N/A')
        elif current_mode == Mode.IDLE_MODE:
            if is_tx():
                lcd.redraw(channel, 'IDLE', 'N/A', 'N/A', power)
            else:
                lcd.redraw(channel, 'IDLE', 'N/A', 'N/A')
        elif current_mode == Mode.START_MODE and output_queue.empty():
            if is_tx():
                lcd.redraw(channel, 'Transmit', 'N/A', 'N/A', power)
            else:
                lcd.redraw(channel, 'Receive', 'N/A', 'N/A')
        elif not output_queue.empty():
            if is_tx():
                pass
            else:
                output_queue.get()
                if y >= 250:
                    if int(x) >= -50:
                        lcd.redraw(channel, 'Excellent', str(y), str(x))
                        buzzer.buzz(.1, 2300, 1)
                    elif int(x) >= -70:
                        lcd.redraw(channel, 'Good', str(y), str(x))
                        buzzer.buzz(.1, 2500, 1)
                    else:
                        lcd.redraw(channel, 'Good', str(y), str(x))
                        buzzer.buzz(.1, 2700, 2)
                else:
                    if int(x) <= -89:
                        lcd.redraw(channel, 'Poor', str(y), str(x))
                        buzzer.buzz(.1, 3000, 3)
                    else:
                        lcd.redraw(channel, 'Bad', str(y), str(x))
                        buzzer.buzz(.1, 3200, 4)

        sleep(.1)

        if not input_queue.empty():
            data = input_queue.get()
            # send it to the serial device
            if data == 'e':
                sp.flush_Input()
                sp.flush_Output()
                output_queue.queue.clear()
                input_queue.queue.clear()
            elif data == 'rx':
                sp.flush_Input()
                sp.flush_Output()
                output_queue.queue.clear()
                input_queue.queue.clear()
                # lcd.reflash(channel)

            sp.write(data)
            lcd.setflash()

        if sp.in_Waiting() > 1 and current_mode == Mode.START_MODE:
            data = sp.read()

            if "0x1B 0x61" in data and len(data.split('{')) > 11:
                r = (data.split('{')[8][0:3])
                l = (data.split('{')[7][0:4])
                try:
                    int(r)
                    if 4000 != int(data.split('{')[11][2:6]):
                        continue
                    rssi.append(r)
                    lqi.append(int(l, 16))
                except ValueError:
                    continue

                if len(rssi) > 10:
                    sp.flush_Input()
                    try:
                        x = statistics.mode(rssi)
                        y = statistics.mode(lqi)
                        rssi[:] = []
                        lqi[:] = []
                        output_queue.put(data)
                        print('RSSI:{}, LQI: {}'.format(repr(x), repr(y)))
                        lcd.setflash()
                    except statistics.StatisticsError:
                        continue


if __name__ == '__main__':

    # sudo service pigpiod start
    # sudo service pigpiod stop

    time()
    jmp = Button(21)
    btn_power = Button(26, hold_time=2)
    btn_channel = Button(13, hold_time=2)
    btn_start = Button(6)

    channel = 11
    power = 8
    current_mode = ''

    input_queue = queue.Queue()
    output_queue = queue.Queue()

    sp = SerialProcess()
    lcd = Lcd()
    buzzer = Buzzer()

    buzzer.start()

    if is_tx():
        print("Tx Mode")
    else:
        print("Rx mode")

    while True:
        while not sp.is_open():
            sp = SerialProcess()
            print('port is open')

        try:
            t = threading.Thread(target=io_jobs)
            t.start()
            btn_start.when_released = start
            btn_channel.when_released = channels
            btn_channel.when_held = set_channels
            btn_power.when_released = power_mode
            btn_power.when_held = set_power
            current_mode = Mode.IDLE_MODE
            lcd.setflash()
            pause()
        except Exception:
            sp.close()
            raise
        sp.close()

