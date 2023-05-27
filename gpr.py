from joblib import load
import numpy as np

def gpr(x1,x2):
    min1 = 0 # based on gprData.csv
    max1 = 0
    min2 = 0
    max2 = 0
    #ymin = 0
    #ymax = 0

    # Normalize
    # in1 = (x1-min1)/(max1-min1)
    # in2 = (x2-min2)/(max2-min2)
    gp = load('gpr.joblib')
    nptest = np.array([[x1],[x2]])
    nptest2 = nptest.reshape(1,2)
    #y = gp.predict(nptest2)
    #y_pred = y*(ymax-ymin)+ymin
    y_pred = gp.predict(nptest2)
    return y_pred
