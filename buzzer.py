import pigpio
from time import sleep


class Buzzer:
    """docstring for Buzzer"""

    PWM_LED_PIN = 12

    Short_Duration = .05
    Long_Duration = .2
    Low_Pitch = 2200
    mid_Pitch = 2500
    High_Pitch = 2800

    def __init__(self):
        self.pi = pigpio.pi()
        self.pi.set_mode(self.PWM_LED_PIN, pigpio.OUTPUT)

    def __del__(self):
        self.pi.set_mode(self.PWM_LED_PIN, pigpio.INPUT)
        self.pi.stop()

    def buzz(self, duration, freq, n=1):
        for x in range(n):
            self.pi.hardware_PWM(self.PWM_LED_PIN, freq, 50 * 10000)
            sleep(duration)
            self.pi.hardware_PWM(self.PWM_LED_PIN, freq, 0)
            sleep(.1)

    def start(self):
        self.buzz(self.Short_Duration, self.Low_Pitch)
        self.buzz(self.Short_Duration * 2, self.mid_Pitch)
        self.buzz(self.Long_Duration, self.High_Pitch)

    def error(self):
        self.buzz(self.Short_Duration, self.High_Pitch, 3)

    def set(self):
        self.buzz(self.Short_Duration, self.mid_Pitch)

    def prog(self):
        self.buzz(self.Long_Duration, self.High_Pitch)
        self.buzz(self.Short_Duration, self.mid_Pitch)
        self.buzz(self.Long_Duration, self.High_Pitch)
        self.buzz(self.Short_Duration, self.mid_Pitch)
