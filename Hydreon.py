import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from time import sleep
#from datetime import datetime
#import threading

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # 23 is the pin number of RPi
count = 0


def button_callback(channel) -> None:
        global count
        count += 1

def addEvent(): # call this function in your main code
    GPIO.add_event_detect(23, GPIO.FALLING, callback=button_callback)


def rainDepth(t): # t duration of sensing, also the number of rainfall depth in the returned list
    bucketSize = 0.2 # Sensitivity of your Hydreon
    def get_RG11() -> float: 
        return round(count*bucketSize, 5)

    def reset_RG11() -> None:
        global count
        count = 0
        # logging.info("[{}] Reset RG11".format(datetime.now()))

    try:
        rain = []
        for _ in range(t):
            
            x = get_RG11()  # return variable if you want singular values
            print("Rainfall: ", x, "mm")
            rain.append(x) 
            sleep(1)
        reset_RG11()

    except:
        GPIO.cleanup()
    #print(rain)
    return(rain) # returns a list of rainfall depth
