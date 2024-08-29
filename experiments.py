from settings import *
import time

delta = -(7+int(FORMATING_NOW("%d"))-((int(FORMATING_NOW("%d"))-["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"].index(FORMATING_NOW("%A"))))%7)*86400
print([FORMATING_DELTA("%d", delta+i*86400) for i in range(35)])