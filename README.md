# Backtesting



## Status as of 11.11.2021 - version 1.0

This is a simple backtesting script written in python. This is in no way optimized for speed (see notes below).
Current performance on my Lenovo T450s: Going through 1800 stocks over 5 years of daily data takes ~8 minutes.


## Upcoming changes in rough order of priority

1) Improve speed - at first by implementing vectorization in the main function (version 2.0)
2) Implement commission and slippage - simulate realistic trading
3) Add a stop loss condition (static or dynamic) to limit downside, esp. important for small cap short positions
4) Improve the measure of volatility - currently the script uses the average of entire testperiod thus "looking ahead"
5) Expand strategy evaluation - add Sharp/Sortino ratio etc, different levels of risk exposure 
 

## Version 2 versus 1
V-E-C-T-O-R-I-Z-A-T-I-O-N

#Performance comparison

As booting performance (speed) was the main priority in version 2.0 it is interesting to see at the actual difference.

Method
This test was done by using datetime.now() which is considered nooby'

Pros:
*It shows an actual usecase

Results

Stocks tested | Version 1 | Version 2
-------------   ---------   ---------
100
200
300
400
500
600


| Stocks tested | Version 1    | Version 2    |
| :------------ |:------------:| ------------:|
| 100           | 10.20        | 12.21        |
| 200           | 12.12        | 12.12        |
| 300           | 34.34        | 12.12        |




