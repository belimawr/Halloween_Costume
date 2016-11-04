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

def all_off():
    for pin in all_pins:
        pin.duty(0)

def all_on(delay):
    for pin in all_pins:
        pin.duty(0)

    for pin in all_pins:
        pin.duty(1023)
        time.sleep(delay)

def blink(times=2):
    for i in range(times):
        for pin in all_pins:
            pin.duty(0)
        time.sleep(1)

        for pin in all_pins:
            pin.duty(1023)
        time.sleep(1)

def fade_in(delay=0.1, step=10, pins=None):
    if not pins:
        pins = pins_names
    for i in range(0, 1024, step):
        for p in pins:
            try:
                getattr(locals()['halloween'], p).duty(i)
            except Exception:
                pass
        time.sleep(delay)

def fade_out(delay=0.1, step=10, pins=None):
    all_on(0)
    if not pins:
        pins = pins_names
    for i in range(1024, 0, -step):
        for p in pins:
            try:
                getattr(locals()['halloween'], p).duty(i)
            except Exception:
                pass
        time.sleep(delay)
    all_off()

def fade_blink(delay=0.1, step=10, pins=None):
    if not pins:
        pins = pins_names
    for i in range(0, 1024, step):
        for p in pins:
            try:
                getattr(locals()['halloween'], p).duty(i)
            except Exception:
                pass
        time.sleep(delay)

    for i in range(1024, 0, -step):
        for p in pins:
            try:
                getattr(locals()['halloween'], p).duty(i)
            except Exception:
                pass
        time.sleep(delay)
    all_off()

def fade_blink_one(delay=0.1, step=10, pins=None):
    pins = all_pins
    all_off()

    for p in pins:
        for i in range(0, 1024, step):
            p.duty(i)
            time.sleep(delay)
        p.duty(1023)
    for p in pins:
        for i in range(1024, 0, -step):
            p.duty(i)
            time.sleep(delay)
        p.duty(0)
