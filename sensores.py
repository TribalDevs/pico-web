from machine import Pin,ADC,PWM
import utime

buzzerPIN=16
BuzzerObj=PWM(Pin(buzzerPIN))

xAxis = ADC(Pin(27))
yAxis = ADC(Pin(26))
SW = Pin(22,Pin.IN, Pin.PULL_UP)
readDelay = 0.1

red = Pin(13, Pin.OUT)
green = Pin(14, Pin.OUT)
blue = Pin(15, Pin.OUT)
 
def buzzer(buzzerPinObject,frequency,sound_duration,silence_duration):

    buzzerPinObject.duty_u16(int(65536*0.2))
    buzzerPinObject.freq(frequency)
    utime.sleep(sound_duration)
    buzzerPinObject.duty_u16(int(65536*0))
    utime.sleep(silence_duration) 
 
 
while True:
    xRef = xAxis.read_u16()
    yRef = yAxis.read_u16()
    
    SWPushed= SW.value()
    
    
    print("X: " + str(xRef) +", Y: " + str(yRef) + ", SW: " + str(SWPushed))
    utime.sleep(readDelay)
    
    if(SWPushed == 0):
        buzzer(BuzzerObj,523,0.5,0.1) #C (DO)

        buzzer(BuzzerObj,587,0.5,0.1) #D (RE)

        buzzer(BuzzerObj,659,0.5,0.1) #E (MI)
        buzzer(BuzzerObj,698,0.5,0.1) #F (FA)

        buzzer(BuzzerObj,784,0.5,0.1) #G (SOL)
        buzzer(BuzzerObj,880,0.5,0.1) #A (LA)
        buzzer(BuzzerObj,987,0.5,0.1) #B (SI)
    
    if(xRef < 300):
        red.value(1)
        utime.sleep(1)
    elif(yRef < 300):
        green.value(1)
        utime.sleep(1)
    else:
        red.value(0)
        green.value(0)
        blue.value(0)
    
    
    BuzzerObj.deinit()
