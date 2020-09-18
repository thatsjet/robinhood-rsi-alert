# robinhood-gold-alert

Runs continuously and will send an alert (MacOS) when the RSI hits your defined cieling or floor.

If you're not on a Mac, you'll want to comment out the `pync` calls and use some other method to alert or just watch the terminal I suppose.

## Installation

Clone repository
```
$ git clone git@github.com:thatsjet/robinhood-gold-alert.git
```

Setup virtual environment (optional)
```
$ python3 -m venv .
```
Install dependencies
```
$ pip install -r requirements.txt
```
Rename and edit config file with your details
```nano
$ mv config_example.yml config.yml

$ vi config.yml
```
```
robinhood:
  user: "yourname@somewhere.com"
  pass: "Password123"

symbol: "SPY"

rsi:
  ceiling: 70
  floor: 30
  period: 10
```

Run the script and you should see output similar to below
```
$ python3 alert.py

Reading configuration data

Logging you in...

RSI of 69.54420633505075 is not in window


```