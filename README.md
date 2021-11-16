# Backtesting

Status as of 11.11.2021 - version 1.0

This is a simple backtesting script written in python. This is in no way optimized for speed (see notes below).
Current performance on my Lenovo T450s: Going through 1800 stocks over a 5 years of daily data takes ~8 minutes.


Upcoming changes in rough order of priority

Improve
1) Improve speed - at first by implementing vectorization in the main function
2) Implement commission and slippage - simulate realistic trading
3) Improve the measure of volatility - currently the script uses average of entire testperiod thus "looking ahead"
4) Expand strategy evaluation - add Sharp/Sortino ratio etc, different levels of risk exposure 
 


