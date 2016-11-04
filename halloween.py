import time
from machine import Pin, PWM
from ESP_PINS import PINS

d1 = PWM(Pin(PINS['D1']))
d2 = PWM(Pin(PINS['D2']))
d3 = PWM(Pin(PINS['D3']))
d4 = PWM(Pin(PINS['D4']))
d5 = PWM(Pin(PINS['D5']))
d6 = PWM(Pin(PINS['D6']))
d7 = PWM(Pin(PINS['D7']))

all_pins = [d1, d2, d3, d4, d5, d6, d7]


def do_something():
    for pin in all_pins:
        pin.duty(0)

    for pin in all_pins:
        pin.duty(1023)
        time.sleep(2)
