import csv
import queue
import matplotlib.pyplot as plt

filename = "sp500" # Edit to use data for a different asset

# --Gathering Data--

class Day:
    Date = ""
    Open = 0.0
    High = 0.0
    Low = 0.0
    Close = 0.0

    def __init__(self, date, open, high, low, close):
        self.Date = date
        self.Open = open
        self.High = high
        self.Low = low
        self.Close = close

days = queue.LifoQueue()

with open('data/' + filename +'.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    firstLine = True
    for row in reader:
        if firstLine:
            firstLine = False
            continue
        else:
            day = Day(row[0], float(row[1].replace(',', '')), float(row[2].replace(',', '')), float(row[3].replace(',', '')), float(row[4].replace(',', '')))
            days.put(day)

x = []
y = []

dateFrequency = 10
dateFrequencyCounter = 0

while days.empty() == False:
    day = days.get()
    x.append(day.Date)
    y.append(day.Close)
    
# --Plotting--

#Dark Theme
plt.style.use('dark_background')

plt.plot(x,y, label='Asset Price')
plt.title('Market')
plt.xlabel('')
plt.ylabel('')
plt.show()