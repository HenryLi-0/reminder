from settings import *
import time

# delta = -(7+int(FORMAT_NOW("%d"))-((int(FORMAT_NOW("%d"))-["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"].index(FORMAT_NOW("%A"))))%7)*86400
# print([FORMAT_DELTA("%d", delta+i*86400) for i in range(35)])

# # 17179869184
# print(time.localtime(2**34))

timestamp = "12/25/1985 @5-00-9 PM" #"8/6/2024 8:50:22"
print(timestamp)
offset = 0
for test in ["am", "AM", "aM", "Am", "pm", "PM", "pM", "Pm"]:
    if test in timestamp: break
if test in ["am", "AM", "aM", "Am"]: offset = 0
if test in ["pm", "PM", "pM", "Pm"]: offset = 43200
timestamp += " "
for char in timestamp:
    if not(str(char) in "0123456789"): timestamp = timestamp.replace(str(char), " ")
while "  " in timestamp: timestamp = timestamp.replace("  ", " ")
try: print(int(round(time.mktime(time.strptime(timestamp, "%m %d %Y %I %M %S ")))+offset))
except: print(int(round(time.mktime(time.strptime(timestamp, "%m %d %Y %I %M ")))+offset))