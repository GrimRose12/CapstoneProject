import time
import RPi.GPIO as GPIO
import Hydreon as hd
import gpr
import concurrent.futures
import mnv2
import laserSensor as ls
import webcam as wc
import compileCSV as comp
from datetime import datetime
import logging 
import VL53L0X


relayPin = 24
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
GPIO.setup(relayPin, GPIO.OUT)

"""Parameters""" 
rainDetectParam = 0.6
detectDuration = 20 
laserCalib = 0
actuateDuration = 90

directory = 'input/image.jpg'

# water level thresholds
height = 20
safeLevel = 0
threshold1 = 0.6*height # flood alert
threshold2 = 0.8*height # flood warning

#logging
logging.basicConfig(filename="logs/waterpi.log", format='%(asctime)s - %(message)s', level=logging.INFO)


def logger(cycle, waterlevel, intensity, classification, prediction, actuation):
    logging.info(f'Cycle: {cycle} | Water level: {waterlevel} cm | Rainfall Intensity: {intensity} | \
Water Level Classification: {classification} | Predicted Water Level: {prediction} cm | \
Actuation: {actuation}')

def detectRain():
    depthList = hd.rainDepth(detectDuration)
    depthDiff = depthList[-1] - depthList[0]
    if depthDiff >= rainDetectParam:
        rainStatus = 1
        print("Rain detected")
    elif depthDiff < rainDetectParam:
        rainStatus = 0
        print("No rain detected")
    return depthList, rainStatus

def detectLevel():
    #waterlevel = ls.measureDist(detectDuration, laserCalib)
    waterlevel = ls.measureDist(1, laserCalib)
    return waterlevel

def rainIntensity(depth):
    intensity = depth/detectDuration
    return intensity

def compareLevels(waterclass, numlevel):
    numclass = 0
    if numlevel < threshold1:
        numclass = 1
    elif numlevel < threshold2:
        numclass = 2
    elif numlevel > threshold2:
        numclass = 3
    print("numclass is: ", numclass)
    if numclass != waterclass:
        return False
    elif numclass == waterclass:
        return True

def actuate():
    GPIO.output(relayPin, GPIO.LOW)
    time.sleep(actuateDuration)
    GPIO.output(relayPin, GPIO.HIGH)

def start():
    global actuation_log
    rainDepth, rainStatus = detectRain()
    level = detectLevel()
    in_level = level[0]
    lastDepth = rainDepth[-1]
    wc.takePicture(directory, counts)
    classification = mnv2.classify(directory)
    print("Image classification: ", classification)
    isCorrect = compareLevels(classification, in_level)
    if rainStatus == 0 and in_level > threshold1 and isCorrect:
        print("No rain but water level is high, and image classification agrees. Actuating.")
        actuate()
        actuation_log = 1
    return in_level, lastDepth, classification, isCorrect, rainStatus

def activate(level, intensity):
    global actuation_log
    print('Activating GPR function.')
    predLevel = gpr.gpr(level, intensity)
    print(f"Inputs : {level}, {intensity} | Output: {predLevel}")
    if predLevel > threshold1:
        actuate()
        actuation_log = 1
        print('Predicted level is higher than threshold, actuating.')
    return predLevel

counts = 0 # logging
hd.addEvent()


while True:
    init_time = time.time()
    print(f"Cycle: {counts}")
    GPIO.output(relayPin, GPIO.HIGH)
    final_level_log = "GPR not activated"
    actuation_log = 0
    initialLevel, depth, classification, isCorrect, rainStatus= start()
    print(f"Initial Level = {initialLevel}, Depth = {depth}, classification = {classification}, rainStatus = {rainStatus}")
    
    intensity = rainIntensity(depth)
    counts += 1
    if rainStatus == 1:
        print('Rain detected. Activating.')
        if isCorrect == False:
            print('Numerical and classified water level not the same. Moving to next cycle.')
            logger(counts, initialLevel, intensity, classification, final_level_log, actuation_log)
            print("Elapsed time = ", time.time()-init_time, " s")
            continue
        elif isCorrect == True:
            print("Water level matches picture")
            final_level_log = activate(initialLevel, intensity)
            logger(counts, initialLevel, intensity, classification, final_level_log, actuation_log)
            print("Elapsed time = ", time.time()-init_time, " s")
            continue
    elif rainStatus == 0:
        print('No rainfall detected')
        logger(counts, initialLevel, intensity, classification, final_level_log, actuation_log)
        print("Elapsed time = ", time.time()-init_time, " s")
        continue
    print("Elapsed time = ", time.time()-init_time, " s")
