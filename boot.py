# Hecho por: @IsaacRFx - Edwin Isaac Rodriguez Flores
# Programa para iniciar un web server y manipular LED de pico desde éste

import rp2
import network
import ubinascii
import machine
import urequests as requests
import time
from secrets import secrets
import socket
import os

t = time.localtime()
time_parsed = f'{t[2]}-{t[1]}-{t[0]} {t[3]}:{t[4]}:{t[5]}'
# Set country to avoid possible errors
rp2.country('MX')

wlan = network.WLAN(network.STA_IF)

wlan.active(True)
print(wlan.scan())
# If you need to disable powersaving mode
# wlan.config(pm = 0xa11140)

# See the MAC address in the wireless chip OTP
mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
print('mac = ' + mac)

# Load login data from different file for safety reasons
ssid = secrets['ssid']
pw = secrets['pw']

wlan.connect(ssid, pw)

# Wait for connection with 10 second timeout
timeout = 10
while timeout > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    timeout -= 1
    print('Waiting for connection...')
    time.sleep(1)

# Define blinking function for onboard LED to indicate error codes    
def blink_onboard_led(num_blinks):
    led = machine.Pin('LED', machine.Pin.OUT)
    for i in range(num_blinks):
        led.on()
        time.sleep(.2)
        led.off()
        time.sleep(.2)
    
# Handle connection error
# Error meanings
# 0  Link Down
# 1  Link Join
# 2  Link NoIp
# 3  Link Up
# -1 Link Fail
# -2 Link NoNet
# -3 Link BadAuth

wlan_status = wlan.status()
blink_onboard_led(wlan_status)

if wlan_status != 3:
    raise RuntimeError('Wi-Fi connection failed')
else:
    print('Connected')
    status = wlan.ifconfig()
    print('ip = ' + status[0])
    
# HTTP server with socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

