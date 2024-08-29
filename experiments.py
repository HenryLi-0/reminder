from settings import *
import time

delta = -(7+int(FORMAT_NOW("%d"))-((int(FORMAT_NOW("%d"))-["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"].index(FORMAT_NOW("%A"))))%7)*86400
print([FORMAT_DELTA("%d", delta+i*86400) for i in range(35)])

# 17179869184
print(time.localtime(2**34))