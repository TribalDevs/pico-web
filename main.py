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

# Listen for connections
while True:
    try:
        reading = sensor_temp.read_u16() * conversion_factor
        temperature = 27 - (reading - 0.706)/0.001721
        isLedOn = 'OFF'
        cl, addr = s.accept()
        print('Client connected from', addr)
        r = cl.recv(1024)
        
        
        # print(r)
        requestLog = False
        r = str(r)
        led_on = r.find('/led/on')
        led_off = r.find('/led/off')
        logs = r.find('/logs')
        print(logs)
        if led_on == 6:
            isLedOn = 'ON'
            print(f'LED ON - ON: {led_on} OFF: {led_off}')
            led.value(1)
            
        if led_off == 6:
            isLedOn = 'OFF'
            print(f'LED OFF - ON: {led_on} OFF: {led_off}')
            led.value(0)
            
        if logs == 6:
            requestLog = True
            
        response = get_html('index.html', logs=requestLog) % (isLedOn, temperature)
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()
        
    except OSError as e:
        cl.close()
        print('Connection closed')

