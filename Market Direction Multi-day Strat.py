import csv
import queue
import matplotlib.pyplot as plt

leverage = 1.0 #Edit to use leverage

assetStartingValue = -1.0

# --Gathering Data--

# Edit to use data for a different asset
#filenames = ["sp500_2015-2020", "sp500_2014", "sp500_2013", "sp500_2012", "sp500_2011", "sp500_2010"]
filenames = ["sp500_2010", "sp500_2009", "sp500_2008", "sp500_2007", "sp500_2006", "sp500_2005"]
#filenames = ["sp500_2015-2020", "sp500_2014", "sp500_2013", "sp500_2012", "sp500_2011", "sp500_2010", "sp500_2009", "sp500_2008", "sp500_2007", "sp500_2006", "sp500_2005"]
#filenames = ["BTC-USD"]
#filenames = ["AMZN"]

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

days = queue.LifoQueue() #Lifo for old data

for file in filenames:
    with open('data/' + file +'.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        
        firstLine = True
        
        for row in reader:
            if firstLine:
                firstLine = False
                continue
            else:
                if(row[1] == 'null'):
                    continue
                day = Day(row[0], float(row[1].replace(',', '')), float(row[2].replace(',', '')), float(row[3].replace(',', '')), float(row[4].replace(',', '')))
                days.put(day)
                assetStartingValue = day.Close




x = []
y = []

cash = []
noStrategyCash = []
stratNoLeverageCash = []
startingCash = assetStartingValue
currentCash = startingCash
currentNoStrategyCash = currentCash
currentStratNoLeverage = currentCash

sellCounter = 1
streakAndDirection = 0
previousClose = 0.0
firstDay = True
while days.empty() == False:
    day = days.get()

    x.append(day.Date)
    y.append(day.Close)
    if not firstDay:

        #---Strategy---

        if streakAndDirection >= 1:
            #Stay Out
            print("selling (" + str(sellCounter)+")")
            sellCounter+=1
        else:
            #Buy
            currentCash = currentCash * (1+((day.Close/previousClose)-1)*leverage)

        if(day.Close/previousClose) > 1:
            if streakAndDirection <= 0:
                streakAndDirection = 1
            else:
                streakAndDirection += 1
        else:
            if streakAndDirection >= 0:
                streakAndDirection = -1
            else:
                streakAndDirection -= 1

        #Update Null Strategy
        currentNoStrategyCash = currentNoStrategyCash * (1+((day.Close/previousClose)-1)*leverage)
        currentStratNoLeverage = currentStratNoLeverage * (day.Close/previousClose)
        
    else:
        firstDay = False
    cash.append(currentCash)
    noStrategyCash.append(currentNoStrategyCash)
    stratNoLeverageCash.append(currentStratNoLeverage)
    previousClose = day.Close
    

# --Plotting--

#Dark Theme
plt.style.use('dark_background')

plt.plot(x,y, label='Asset Price')
plt.plot(x,cash, label='Portfolio Value')
plt.plot(x,noStrategyCash, label='Null Strategy')
plt.plot(x,stratNoLeverageCash, label='Strategy No Leverage')
marketReturn = ((y[-1]/assetStartingValue)-1)*100.0
yourReturn = ((cash[-1]/startingCash)-1)*100.0
results = "Market return: " + str(marketReturn)[0:7] + "% | Your return: " + str(yourReturn)[0:7] + "% | Δ: " + str(yourReturn-marketReturn)[0:7] + "%"
plt.title(results)
plt.xlabel('')
plt.ylabel('')
print(results)
plt.show()