#IMPORTS AND SIMILAR
from scipy.stats.mstats import gmean
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import sqlite3
import pandas as pd
import sqlalchemy
import numpy as np
timemeasure = datetime.datetime.now()
pd.set_option('display.max_columns', None)


#-------------- Set up test universe - loaded from local SQLite database ----------------------

#connect to SQLite database
connect = sqlite3.connect("SRUSListedVersion2.db")

#create a cursor
c = connect.cursor()

#add all symbols in the database to 'stocklist'
stocklist = [] #stockbuffer

c.execute('''select * FROM sqlite_master WHERE type="table"''')
storagelist = c.fetchall()

for x in range(len(storagelist)):
    stocklist.append(storagelist[x][1])



#-------------------- Parameters for the backtest---------------------
# 0=off, 1=on
startdate = "'2016-01-01'"
enddate = "'2021-09-09'"
direction = "short" #"short"/"long"

RVOLfilter = 0
RVOLsetting = 2

DollarVolfilter = 1
DollarVolsetting = 10000

PriceChangeFilter = 1
PriceChangeSetting = 8

RangePercentileFilter = 0
RangePercentileSetting = 50

SharePriceFilter = 1
SharePriceSetting = 1


#------------------- Actual testing section----------------------------------

#Lists for data storage - to build 'results dataframe' from
dates = []
stocknames = []
pricechangespct = []
pricechangesrelative = []
overnightreturns = []
day1returns = []
day2returns = []
entryprices = []
RVOL10D = []
FailureList = []

#Definition of Tradefunction
def TradeFunction(x,stock):
    Tradesignal = 1

    if PriceChangeFilter == 1:
        pricechangepct = df.loc[x,"close"]/df.loc[x,"open"]
        pricechangerelative = (df.loc[x,"close"]-df.loc[x,"open"]) / df["range"].mean()
        if pricechangerelative < PriceChangeSetting: #OBS gennemgå denne linje
            Tradesignal = 0

    if RVOLfilter == 1:
       if df.loc[x,"volume"] > RVOLsetting*df.loc[x,"avgvolume10D"]:
            Tradesignal = 0

    if DollarVolfilter == 1:
        if df.loc[x, "$volume"] < DollarVolsetting:
            Tradesignal = 0

    if RangePercentileFilter == 1:
        if df.loc[x,"percentileclose"] < RangePercentileSetting:
            Tradesignal = 0

    if SharePriceFilter == 1:
        if df.loc[x,"close"] < SharePriceSetting:
            Tradesignal = 0


    #log trade
    if Tradesignal == 1:

        try:
            dates.append(df["date"][x])
            entryprices.append(df["close"][x])
            stocknames.append(stock)
            pricechangespct.append(pricechangepct)
            pricechangesrelative.append(pricechangerelative)
            RVOL10D.append(df.loc[x,"volume"] / df.loc[x,"avgvolume10D"])#df.loc[x,"volume"]/df.loc[x, "avgvolume10D"])

        except:
            print("Failed to log one of: date,entryprice,stockname,pricechange,RVOL")

        if direction == "long":
            try:
                day1returns.append(((df.loc[x + 1, "close"] - df.loc[x, "close"]) / df.loc[x, "close"]) + 1)
                day2returns.append(((df.loc[x + 2, "close"] - df.loc[x + 1, "close"]) / df.loc[x + 1, "close"]) + 1)
                overnightreturns.append((((df.loc[x + 1, "open"] - df.loc[x, "close"]) / df.loc[x, "close"]) + 1))
                df.loc[x, "signal"] = 1
            except:
                print("Failed to log results for a long trade in stock: %s" %stock)

        elif direction == "short":

            try:
                day1returns.append(((df.loc[x, "close"] - df.loc[x + 1, "close"]) / df.loc[x, "close"]) + 1)
                day2returns.append(((df.loc[x + 1, "close"] - df.loc[x + 2, "close"]) / df.loc[x + 1, "close"]) + 1)
                overnightreturns.append((((df.loc[x, "close"] - df.loc[x + 1, "open"]) / df.loc[x, "close"]) + 1))

            except:
                print("Failed to log results for a short trade in stock: %s" % stock)

        else:
            print("Direction for trade needs a parameter setting")


#------------------------- Initiate the backtest ------------------------
for stock in stocklist:
    try:
        # Load data from SQLite and set up the dataframe
        df = (pd.read_sql("SELECT * FROM %s WHERE DATE(date) BETWEEN %s AND %s" %(stock,startdate,enddate), connect))
        pd.set_option("display.max_rows", 300, "display.min_rows", 200, "display.max_columns", None, "display.width", None)

        #Run function with itertuples
        for row in df.iloc[:-2].itertuples():
            TradeFunction(row.Index, stock)


    except:
        print("Error with stock: %s" % stock)
        FailureList.append(stock)



#-------- Check DataFrame---------------------
#pd.DataFrame.to_csv(df,r'C:\Users\LENOVO\Desktop\testfil.csv')

#print("Print of all rows with nan values: \n")
#print(df[df.isna().any(axis=1)])
#print("længde af dataframe før dropna:",len(df))
#df = df.dropna()  # Remove all rows in df with NA/NAN values
#print("længde af dataframe efter dropna:",len(df))


'''
print("længde for dates:", len(dates))
print("længde for stockname:", len(stocknames))
print("længde for entry price:", len(entryprices))
print("længde for overnightreturn:", len(overnightreturns))
print("længde for day1:", len(day1returns))
print("længde for day2:", len(day2returns))
'''



#-----------------------------------Set up resultsdataframe --------------------------------------


resultsDataFrame = pd.DataFrame({"Date": dates,
                                 "Stockname": stocknames,
                                 "Pricechangepct": pricechangespct,
                                 "Pricechangerelative": pricechangesrelative,
                                 "RVOL10D": RVOL10D,
                                 "Entry price": entryprices,
                                 "overnightreturn": overnightreturns,
                                 "day1return": day1returns,
                                 "day2return": day2returns,
                                 #"RVOL20D": RVOL20D,
                                 #"RVOL30D": RVOL30D
                                 })

resultsDataFrame["overnightreturnscumulative"] = resultsDataFrame["overnightreturn"].cumprod()
resultsDataFrame["day1returnscumulative"] = resultsDataFrame["day1return"].cumprod()
resultsDataFrame["day2returnscumulative"] = resultsDataFrame["day2return"].cumprod()
resultsDataFrame["day2return10PctRisk"] = ((resultsDataFrame["day2return"]-1)/10)+1
resultsDataFrame["day2returnRiskcumulative"] = resultsDataFrame["day2return10PctRisk"].cumprod()

print("resultsDataFrame:")
print(resultsDataFrame)


#--------------------- Preparing data for presentation ----------------------------------------------------------------
#Variables for analysis of results
try:
    NumberTradingDays = len(df) #wrong if last stock tested doesn't have date for entire backtest period
    NumberTradingDaysXTickers = len(stocklist*NumberTradingDays)
    NumberTradeSignals = len(day1returns)
    SignalFrequency = "1 / %s"%(NumberTradingDaysXTickers/NumberTradeSignals)

    GeoMeanOvernight = gmean(overnightreturns)
    GeoMeanDay1 = gmean(day1returns)
    GeoMeanDay2 = gmean(day2returns)
except:
    print("Der var problemer med at logge resultater")


try:
    Logdataframe0 = pd.DataFrame({
        "Antal aktier testet": [len(stocklist)],
        "Antal handelsdage": [NumberTradingDays],
        "Handelsdage X tickers": [NumberTradingDaysXTickers],
        "# Handelssignaler": [NumberTradeSignals],
        "Signal frekvens": [SignalFrequency]})
except:
    print("Der var et problem med Logdataframe0")

try:
    Logdataframe = pd.DataFrame(
        {"Date": datetime.date.today(),
         "RVOL setting": [RVOLsetting],
         "Price change setting": [PriceChangeSetting],
         "Range percentile setting": [RangePercentileSetting],
         "Antal handelssignaler": [NumberTradeSignals],
         "Geo mean overnight": [GeoMeanOvernight],
         "Geo mean day 1": [GeoMeanDay1],
         "Geo mean day 2": [GeoMeanDay2]},
        columns=["Date", "RVOL setting", "Price change setting", "Range percentile setting",
                 "Antal handelssignaler","Geo mean overnight", "Geo mean day 1", "Geo mean day 2"])

except:
    "Errow with 'Logdataframe'"


#--------------------- Presentation of data ----------------------------------------------------------------------------

try:
    print("\n",Logdataframe0.to_string(index=False))
    print("\n",Logdataframe.to_string(index=False),"\n")
except:
    print("Error when presenting results")


print("Time to run script: ",datetime.datetime.now()-timemeasure)


print("Failure list's length now:")
print(len(FailureList))
print(FailureList)

FailureListStorage = open('FailureList.txt','w')
FailureListStorage.write(str(FailureList))
FailureListStorage.close()


#-------------------------------------- Plotting charts --------------------------------------------------

#resultsDataFrame["overnightreturnscumulative"].plot(legend="overnight return",title="Results")
#resultsDataFrame["day1returnscumulative"].plot(legend="day1return",color="black")
#resultsDataFrame["day2returnscumulative"].plot(legend="day2return")

resultsDataFrame["day2returnRiskcumulative"].plot(legend="day2returnRiskControlCumulative")

#plt.ion()
plt.show()
plt.pause(0.001)

resultsDataFrame.plot(x="RVOL10D",y="day1return", legend= "trade return", style="o")
plt.show()


#--------------------- Logging results to CSV ---------------------------------------------------------------------------
try:
    pd.DataFrame.to_csv(Logdataframe,r"C:\Users\LENOVO\desktop\testfilmarts2.csv",mode="a",header=True,index=False)
    #Logdataframe.to_excel(r"C:\Users\LENOVO\desktop\11martsBacktesting2.xlsx",index=False, header=False,mode="a")

except:
    print("Der var problemer med at eksportere resultaterne til CSV")





#--------------------------- Scrap code --------------------------------------------------------
'''
print("\nAntal aktier testet: ",len(stocklist))
    print("Antal handelsdage: ", NumberTradingDays)
    print("Antal handelsdage x tickers: ", NumberTradingDaysXTickers)
    print("Antal handelssignaler: ", NumberTradeSignals)
    print("Signal Frekvens: ", SignalFrequency)


#Run function with for loop - outdated
        
        for x in range(len(df) - 2):
            TradeFunction(x,stock)
        

'''

