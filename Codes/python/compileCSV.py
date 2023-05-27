import numpy as np
from datetime import datetime

def createCSV(time, level, depth):
    time.insert(0,'Time')
    level.insert(0, 'Level')
    depth.insert(0, 'Depth')
    title = 'data' + str(datetime.now())
    np.savetxt(f'dataset/{title}.csv', [p for p in zip(time, level, depth)], delimiter=',', fmt='%s')
