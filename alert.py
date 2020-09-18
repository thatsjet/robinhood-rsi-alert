import yaml
import pync
import robin_stocks as r
import numpy as np
import talib as ti
import pandas as pd
import schedule
import time


''' NOTE
   -  IF RSI is not matching with RobinHood, then try either increasing the timeperiod
   value or the data frequency, but not sure I can do that.
'''


# READ CONFIG FOR USER, PASS, STOCK
print("Reading configuration data\n")
with open("config.yml", 'r') as stream:
    try:
        config = yaml.safe_load(stream)
        robin_user = config["robinhood"]["user"]
        robin_pass = config["robinhood"]["pass"]
        rsiPeriod = config["rsi"]["period"]
        rsiCeiling = config["rsi"]["ceiling"]
        rsiFloor = config["rsi"]["floor"]
    except yaml.YAMLError as exc:
        print(exc)

# LOGIN TO ROBINHOOD
print("Logging you in...\n")
r.login(robin_user,robin_pass)


# GET HISTORICALS
def run():
    global rsiPeriod
    global config

    close_prices = []
    currentIndex = 0

    historical_quotes = r.get_stock_historicals(config['symbol'],interval='5minute',span='day')
    df = pd.DataFrame(historical_quotes)

    df['close_price'] = df['close_price'].astype(float)

    DATA = np.array(df['close_price'])

    # If it's early in the day there won't be enough records so just
    # use the length of the dataframe isntead
    if(len(DATA) < rsiPeriod):
        rsiPeriod = len(DATA)
        print("rsiPeriod is larger than DATA length, indicator may not be accurate")

    # TODO if DATA.len is < rsiPeriod then rsiPeriod = DATA.len
    rsi = ti.RSI(DATA, timeperiod=rsiPeriod)


    if(rsi[-1] < rsiFloor):
        print('RSI below ' + str(rsiFloor))
        pync.notify('RSI ' + str(rsi[-1]) + ' is below ' + str(rsiFloor) , title="Gold Target")
    elif(rsi[-1] > rsiCeiling):
        print('RSI above ' + str(rsiCeiling))
        pync.notify('RSI ' + str(rsi[-1]) + ' is above ' + str(rsiCeiling) , title="Gold Target")
    else:
        print("RSI of " + str(rsi[-1]) + " is not in window\n")
        pass


# DO one run, then schedule to run every 5 minutes
run()

schedule.every(5).minutes.do(run)
while True:
    schedule.run_pending()
    time.sleep(1)

exit()