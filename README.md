# Backtesting

## About this repository

This is a simple backtesting script written in python. It is in no way optimized for speed (see notes below).
Current performance on my Lenovo T450s: Going through 1800 stocks over 5 years of daily data takes ~8 minutes.


## Status as of 11.11.2021 - version 1.0



## Upcoming changes in rough order of priority

- [x] 1) Improve speed - at first by implementing vectorization in the main function (version 2.0)
- [ ] 2) Implement commission and slippage - simulate realistic trading
- [ ] 3) Add a stop loss condition (static or dynamic) to limit downside, esp. important for small cap short positions 
- [ ] 4) Add functionality to test long trades (currently only short positions) 
- [ ] 5) Improve the measure of volatility - currently the script uses the average of entire testperiod thus "looking ahead"
- [ ] 6) Expand strategy evaluation - add Sharp/Sortino ratio etc, different levels of risk exposure 
- [ ] 7) Add dynamic position sizing based on the historic volatility of each stock

## Version 2 versus version 1

The table of individual simulated trades 'resultsdataframe' and the eponymous 'Logdataframe' have the same structure as in version 1.
The basic plotting and logging is also kept exactly as in version 1.

The easy solution here would have been to make it quite different, but setting it up in this way makes for easy comparison.

The different lies in the main function which leads to...

### Performance comparison

Boosting performance (speed) was the main priority in version 2.0 so it is interesting to see the actual difference.

#### Method
This test was done by using datetime.now() which is sometimes considered bad practice.
The time to run throught the script is of such a magnitude than small inaccuracies don't affect the conclusions significantly.

Cons:
* It is not very exact

Pros:
* It shows an actual usecase


#### Results

* Version 2 is much faster - due to vectorization of the main function
* There is a monotonic increase in time for both versions
* The time margin varies for both versions
  This is because different sections of the list of stocks have different numbers of trading signals


| Stocks tested | Version 1    | Version 2    |
| :------------ |:------------:| ------------:|
| 100           | 20.46        | 3.90         |
| 200           | 49.59        | 6.28         |
| 300           | 75.47        | 11.45        |
| 400           | 82.77        | 15.62        |
| 500           | 102.14       | 17.43        |
| 600           | 131.92       | 19.30        |



![Comparison chart](https://i.ibb.co/pr4h6xX/SR-Backtesting-speed-comparison.png)

