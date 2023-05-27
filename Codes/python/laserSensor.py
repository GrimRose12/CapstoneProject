import time
import VL53L0X
import concurrent.futures

def measureDist(t,c=0):
    tof = VL53L0X.VL53L0X()
    tof.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)
    timing = tof.get_timing()
    if (timing < 20000):
        timing = 20000
    level = []
    for _ in range(t):
        x = round(abs(20-(tof.get_distance()/10)+c),3)
        # y = isc.pred(x)
        # level.append(y,3)
        print("Level = ", x, " cm")
        level.append(x)
        #time.sleep(0.5)
    tof.stop_ranging()
    return level
    
#measureDist(3)
