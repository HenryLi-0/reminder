from settings import *
import time

# delta = -(7+int(FORMAT_NOW("%d"))-((int(FORMAT_NOW("%d"))-["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"].index(FORMAT_NOW("%A"))))%7)*86400
# print([FORMAT_DELTA("%d", delta+i*86400) for i in range(35)])

# # 17179869184
# print(time.localtime(2**34))

# timestamp = "12/25/1985 @5-00-9 PM" #"8/6/2024 8:50:22"
# print(timestamp)
# offset = 0
# for test in ["am", "AM", "aM", "Am", "pm", "PM", "pM", "Pm"]:
#     if test in timestamp: break
# if test in ["am", "AM", "aM", "Am"]: offset = 0
# if test in ["pm", "PM", "pM", "Pm"]: offset = 43200
# timestamp += " "
# for char in timestamp:
#     if not(str(char) in "0123456789"): timestamp = timestamp.replace(str(char), " ")
# while "  " in timestamp: timestamp = timestamp.replace("  ", " ")
# try: print(int(round(time.mktime(time.strptime(timestamp, "%m %d %Y %I %M %S ")))+offset))
# except: print(int(round(time.mktime(time.strptime(timestamp, "%m %d %Y %I %M ")))+offset))

# thing = str(123456)
# print(thing[1:])

# x = time.time()
# x = time.localtime(x)
# x = x.tm_mday*86400 + x.tm_hour*3600 + x.tm_min*60 + x.tm_sec
# print(x)

# print(time.time())
# (621-self.calendarOffset)*25/(self.calendarScale+0.000001) + 47


# calendarScalePrevious = self.calendarScale
# self.calendarScale = 10**(math.log(self.calendarScale+0.000001,10) + self.mouseScroll/2500)-0.000001
# if abs(self.mouseScroll) > 0:
#     self.calendarOffset -= (self.calendarScale-calendarScalePrevious)*(self.mx-71)/25


# temp = time.localtime(time.time())
# print(temp.tm_mday + (8-temp.tm_wday))

# def idk(id):
#     now = time.localtime()
#     yearNow = now.tm_year
#     monthNow = now.tm_mon
#     firstDayInMonth = time.mktime((yearNow, monthNow, 1, 0, 0, 0, 0, 0, -1))
#     monthDay = 1 + (7*(id//7)) + (id%7-time.localtime(firstDayInMonth).tm_wday)
#     if monthDay < 1: monthDay += 7
#     date = (yearNow, monthNow, monthDay, 0, 0, 0, 0, 0, -1)
#     epochSeconds = time.mktime(date)
#     daysSinceEpoch = epochSeconds // (24 * 3600) - 1
#     return daysSinceEpoch


# print((time.mktime(temp) - time.mktime(time.gmtime(0)))//(86400))
# print(f"Epoch day: {idk(34)}")

# temp = time.mktime(time.localtime())
# print(temp)
# print(time.time())

print(time.time()-11*3600-44*60-30*60)

print(round((3599)/900)*900)

from subsystems.simplefancy import generatePastelLight

a,b,c,d = [0,0,0,0]
for i in range(1000):
    temp = generatePastelLight()
    a+=temp[0]
    b+=temp[1]
    c+=temp[2]
    d+=temp[3]
print([a/1000,b/1000,c/1000,d/1000])