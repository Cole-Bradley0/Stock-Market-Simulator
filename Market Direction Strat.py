import csv
import queue
import matplotlib.pyplot as plt

leverage = 1.0 #Edit to use leverage

assetStartingValue = -1.0

# --Gathering Data--

filename = "sp500" # Edit to use data for a different asset

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
            assetStartingValue = day.Close




x = []
y = []

cash = []
startingCash = 3294.61
currentCash = startingCash

todayIsUp = False

previousClose = 0.0
firstDay = True
while days.empty() == False:
    day = days.get()
    x.append(day.Date)
    y.append(day.Close)
    if not firstDay:

        #---Strategy---
        
        if not todayIsUp:
            #Buy
            currentCash = currentCash * (1+((day.Close/previousClose)-1)*leverage)
        else:
            #Sell
            print("selling")

        if(day.Close/previousClose) > 1:
            todayIsUp = True
        else:
            todayIsUp = False
        
    else:
        firstDay = False
    cash.append(currentCash)
    previousClose = day.Close


# --Plotting--
    
#Dark Theme
plt.style.use('dark_background')

plt.plot(x,y, label='Asset Price')
plt.plot(x,cash, label='Portfolio Value')
marketReturn = ((y[-1]/assetStartingValue)-1)*100.0
yourReturn = ((cash[-1]/startingCash)-1.0)*100.0
plt.title("Market return: " + str(marketReturn)[0:7] + "% | Your return: " + str(yourReturn)[0:7] + "% | Δ: " + str(yourReturn-marketReturn)[0:7] + "%")
plt.xlabel('')
plt.ylabel('')
plt.show()