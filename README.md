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
| 100           | 20.46        | 3.90         |
| 200           | 49.59        | 6.28         |
| 300           | 75.47        | 11.45        |
| 400           | 82.77        | 15.62        |
| 500           | 102.14       | 17.43        |
| 600           | 131.92       | 19.30        |



Version1
100: 20.46
200: 49.59
300: 75.47
400: 82.77
500: 102.14
600: 131.92

Version2
100: 3.90
200: 6.28
300: 11.45
400: 15.62
500: 17.43
600:  19.3![image](https://user-images.githubusercontent.com/36546351/143241486-dc7d1330-be03-4106-8a4a-6e09dd45575f.png)


