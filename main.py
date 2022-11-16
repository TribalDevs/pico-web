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
from machine import Pin,ADC,PWM
from sensores import playsong, bequiet, evalColor


# SET UP BUZZER AND RGB LED
buzzerPIN=16
buzzer=PWM(Pin(buzzerPIN))

xAxis = ADC(Pin(27))
yAxis = ADC(Pin(26))
SW = Pin(22,Pin.IN, Pin.PULL_UP)
readDelay = 0.1

red = Pin(13, Pin.OUT)
green = Pin(14, Pin.OUT)
blue = Pin(15, Pin.OUT)

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

# Function to load in html page
def get_html(html_name, **kwargs):
    toPlay = False
    with open(html_name, 'r') as file:
        html = file.read()
    if bool(kwargs.get('playSong')):
        html = html.replace('class="fas fa-volume-off"', 'class="fas fa-volume-on"')
        toPlay = True
    else:
        toPlay=False
        bequiet(buzzer)
    
    html = html.replace('id="led" style="color: #333"', f'id="led" style="color: {kwargs.get("color")}"')
    html = html.replace('id="joystick"></i>', f'id="joystick">x: {kwargs.get("x_stick")}, y: {kwargs.get("y_stick")}</i>')
    return html, toPlay

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

# Listen for connections
while True:	
    try:
        x_stick = xAxis.read_u16()
        y_stick = yAxis.read_u16()
        print('x: %s y: %s' % (x_stick, y_stick))
        
        isButtonPushed= SW.value()
        print('Button: %s' % isButtonPushed)
        playSong = False
        color = 'blue'
        cl, addr = s.accept()
        print('Client connected from', addr)
        r = cl.recv(1024)
        print(r)
        r = str(r)
        sensor = r.find('/sensor/')
        if sensor == 6:
            if isButtonPushed == 0:
                playsong = True
            color = evalColor(x_stick, y_stick)
            print('Color: %s' % color)
            

        
            
        response, song = get_html('index.html', color=color, playSong=playSong, x_stick=x_stick, y_stick=y_stick)
        if song:
            playsong(buzzer)
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()
        
    except OSError as e:
        cl.close()
        print('Connection closed')



