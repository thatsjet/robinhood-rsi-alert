import yaml
import pync
import robin_stocks as r
import numpy as np
import talib as ti
import pandas as pd
import schedule
from datetime import datetime
import time

'''
TODO
- Start on a 5 minute mark
- Print a timestamp at the beginning of the message line

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

    # if DATA.len is < rsiPeriod then rsiPeriod = DATA.len
    rsi = ti.RSI(DATA, timeperiod=rsiPeriod)

    if(rsi[-1] < rsiFloor):
        message = 'RSI ' + str(rsi[-1]) + ' is below ' + str(rsiFloor)
        print(message)
        pync.notify(message , title="Target floor reached")
    elif(rsi[-1] > rsiCeiling):
        message = 'RSI ' + str(rsi[-1]) + ' is above ' + str(rsiCeiling)
        print(message)
        pync.notify(message , title="Target ceiling reached")
    else:
        print("RSI of " + str(rsi[-1]) + " is not in window\n")
        pass

# Calculate current time, subtract from 5, wait that amount of time


print("Running RSI monitor on multiple's of 5 for best accuracy")
# DO one run, then schedule to run every 5 minutes
while True:
    now = datetime.now()
    if (now.minute % 10 == 5) or (now.minute % 10 == 0):
        time.sleep(5)
        run()
        break
    else:
        time.sleep(1)

schedule.every(5).minutes.do(run)
while True:
    schedule.run_pending()
    time.sleep(1)

exit()