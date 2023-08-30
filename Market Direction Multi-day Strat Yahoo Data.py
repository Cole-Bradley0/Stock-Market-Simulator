import csv
import queue
import matplotlib.pyplot as plt

leverage = 1.0 #Edit to use leverage

assetStartingValue = -1.0

# --Gathering Data--

# Edit to use data for a different asset
#filenames = ["BTC-USD"]
filenames = ["SPY"]
#filenames = ["SPY_afterBubblePop"]
#filenames = ["VOO_corona"]
#filenames = ["GOLD"]
#filenames = ["UVXY-1yr"]
#filenames = ["Japan"]
#filenames = ["AAT"]
#filenames = ["PG"]
#filenames = ["U"]
#filenames = ["KO"]
#filenames = ["SPY-90s"]

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

days = queue.Queue()

for file in filenames:
    with open('yahooData/' + file +'.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        
        firstLine = True
        secondLine = True

        for row in reader:
            if firstLine:
                firstLine = False
                continue
            else:
                if(row[1] == 'null'):
                    continue
                day = Day(row[0], float(row[1].replace(',', '')), float(row[2].replace(',', '')), float(row[3].replace(',', '')), float(row[4].replace(',', '')))
                days.put(day)
                if(secondLine):
                    assetStartingValue = day.Close
                    secondLine = False

x = []
y = []

cash = []
noStrategyCash = []
stratNoLeverageCash = []
startingCash = assetStartingValue
currentCash = startingCash
currentNoStrategyCash = currentCash
currentStratNoLeverage = currentCash

strategyDelta = []
delta = 1000.00

sellCounter = 1

streakAndDirection = 0

previousClose = 0.0
firstDay = True
chartResolutionDivisor = 12
chartResolutionCounter = chartResolutionDivisor
while days.empty() == False:
    day = days.get()

    if not firstDay:
        #---Strategy---
        if streakAndDirection >= 5:
            # Stay Out
            #print("selling (" + str(sellCounter)+")")
            #sellCounter+=1
            #delta = delta - (((day.Close/previousClose)*1000)-1000)

            # Buy inverse
            currentCash = currentCash * (1+((day.Close/previousClose)-1)*-leverage)
            print("selling and inversing (" + str(sellCounter)+")")
            sellCounter+=1

            # Only stay out of the days; stay in at night.
            #currentCash = currentCash * (1+((day.Open/previousClose)-1)*leverage)
            #Only stay out of the nights; stay in during days
            #currentCash = currentCash * (1+( ((day.Close/previousClose)-1) - ((day.Open/previousClose)-1)  )*leverage)
        else:
            #Buy
            currentCash = currentCash * (1+((day.Close/previousClose)-1)*leverage)

        # Keep track of streak as determined by entire previous day
        #if(day.Close/previousClose) > 1:
        #    if streakAndDirection <= 0:
        #        streakAndDirection = 1
        #    else:
        #        streakAndDirection += 1
        #else:
        #    if streakAndDirection >= 0:
        #        streakAndDirection = -1
        #    else:
        #        streakAndDirection -= 1
    
        # Keep track of streak as determined by previous night
        #if(day.Open/previousClose) > 1:
        #    if streakAndDirection <= 0:
        #        streakAndDirection = 1
        #    else:
        #        streakAndDirection += 1
        #else:
        #    if streakAndDirection >= 0:
        #        streakAndDirection = -1
        #    else:
        #        streakAndDirection -= 1

        # Keep track of streak as determined by previous day (no night)
        if((day.Close/previousClose) - ((day.Open/previousClose)-1)) > 1:
            if streakAndDirection <= 0:
                streakAndDirection = 1
            else:
                streakAndDirection += 1
        else:
            if streakAndDirection >= 0:
                streakAndDirection = -1
            else:
                streakAndDirection -= 1

        # Update Null Strategy
        currentNoStrategyCash = currentNoStrategyCash * (1+((day.Close/previousClose)-1)*leverage)
        currentStratNoLeverage = currentStratNoLeverage * (day.Close/previousClose)
        
    else:
        firstDay = False

    if(chartResolutionCounter == chartResolutionDivisor):
        x.append(day.Date)
        y.append(day.Close)
        cash.append(currentCash)
        noStrategyCash.append(currentNoStrategyCash)
        stratNoLeverageCash.append(currentStratNoLeverage)
        strategyDelta.append(delta)

    if chartResolutionCounter == 1:
        chartResolutionCounter = chartResolutionDivisor
    else:
        chartResolutionCounter-=1
    
    previousClose = day.Close


# --Plotting--
    
# Dark Theme
plt.style.use('dark_background')

plt.plot(x,y, label='Asset Price')
plt.plot(x,cash, label='Portfolio Value')
plt.plot(x,noStrategyCash, label='Null Strategy')
plt.plot(x,stratNoLeverageCash, label='Strategy No Leverage')
plt.plot(x,strategyDelta, label='Strategy Delta')
marketReturn = ((y[-1]/assetStartingValue)-1)*100.0
leveragedMarketReturn = ((noStrategyCash[-1]/assetStartingValue)-1)*100.0
yourReturn = ((cash[-1]/startingCash)-1)*100.0
results = "Market return: " + str(marketReturn)[0:7] + "% | Your return: " + str(yourReturn)[0:7] + "% | Δ: " + str(yourReturn-marketReturn)[0:7] + "%"
leveragedResults = "Leveraged (" + str(leverage) + "x) return: " + str(leveragedMarketReturn)[0:7] + "% | Your return: " + str(yourReturn)[0:7] + "% | Δ: " + str(yourReturn-leveragedMarketReturn)[0:7] + "%"
plt.title(leveragedResults)
plt.xlabel('')
plt.ylabel('')
print(results)
print(leveragedResults)
plt.show()
