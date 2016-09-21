#!/usr/bin/python
# This is a singleton module to call the stock object methods
# and to perform the All share index calulation.
# This is being used as in python is a cleaner method than trying to restrict a class.
# A test method has been included to demonstrate the functionality.
from __future__ import division
from Stock import Stock
import time

# Initialise the dictionary to hold the stock objects
stockDic = {}

def initialise():
    # Create Stock Objects
    # ToDo - Accept stock from other inputs ie files
    stockDic ['TEA'] = Stock("TEA", "Common", 0, None, 100)
    stockDic ['POP'] = Stock("POP", "Common", 8, None, 100)
    stockDic ['ALE'] = Stock("ALE", "Common", 23, None, 60)
    stockDic ['GIN'] = Stock("GIN", "Preferred", 8, 2, 100)
    stockDic ['JOE'] = Stock("JOE", "Common", 13, None, 250)
    print("Stock intialsed")

    
def getStockYeild(stockSymbol, tickerPrice):
    # Get the Yeild values for the stock
    if testKnownType(stockSymbol):
        yeild = stockDic[stockSymbol].getDivYeild (tickerPrice)
        return yeild
    else:
        return "Unknown Stock Symbol"

        
def getPERatio(stockSymbol, tickerPrice):
    # Get the PE Ratio for the stock
    if testKnownType(stockSymbol):
        pe = stockDic[stockSymbol].getPERatio (tickerPrice)
        return pe
    else:
        return "Unknown Stock Symbol"


def getStockPrice(stockSymbol):
    # Get the stock volume weighted price (last 15mins) 
    if testKnownType(stockSymbol):
        price = stockDic[stockSymbol].getVolWeightedPrice()
        return price
    else:
        return "Unknown Stock Symbol"


def putTransaction(stockSymbol, timestamp,quantity, buySell, price):
    # Call the add transaction function of the stock object
    if testKnownType(stockSymbol):
        stockDic[stockSymbol].addTransaction(timestamp, quantity, buySell, price)
    else:
        return "Unknown Stock Symbol"

        
def getAllShare():
    # Get the All share index
    try:
        # Initialise the variables to track the accumulated stock and count values
        allSharePrice = 1
        noTx = 1

        for stockType in stockDic.values():
            #for each stock type
            price = 1
            txCount = 0
            # The stock prices are multiplied in the stock object
            print("StockType {}".format(stockType.getMeanParams()))     # Debug
            price, txCount = stockType.getMeanParams()
            allSharePrice *= price
            noTx += txCount
            print("AllShare {}, Count {}".format(allSharePrice, noTx))  # Debug

        return allSharePrice**(1/noTx)
    
    except Exception as e:
        print("All Share error".format(e))

        
def testKnownType(stockSymbol):
    # Simple test to ensure that a valid stock object will be found
    if stockDic.has_key(stockSymbol):
        return True


def testStockControl():
    # Test function to exercise all the different functions
    # These tests are not exhaustive, further tests are needed to exercise
    # the functions more fully.
    try:
        # List of symbols - include invalid symbol
        testList = ["TEA", "POP", "ALE", "GIN", "JOE","JON"]

        # Loop through the symbols list
        for loop_no, symbol in enumerate(testList):
            # Get epoch for now
            epoch_time = int(time.time())
            # Increment the loop counter to avoid 0
            this_loop = loop_no + 1
            # Test Yeild
            print("{} yeild {}".format(symbol, getStockYeild(symbol, 200)))
            # Test PE
            print("{} pe {}".format(symbol, getPERatio(symbol, 200)))
            putTransaction(symbol, epoch_time, 100, "Buy", 1.60 * this_loop)
            putTransaction(symbol, epoch_time, 100, "Buy", 1.40 * this_loop)
            putTransaction(symbol, epoch_time, 100, "Buy", 1.20 * this_loop)
            putTransaction(symbol, epoch_time, 100, "Buy", 1.00 * this_loop)
            # Test that the stock has loaded
            print("{} price {}".format(symbol, getStockPrice(symbol)))

            # Add further stock outside the calulation window by taking seconds fromt he epoch
            putTransaction(symbol, epoch_time - 1000, 100, "Buy", 1.20 * this_loop)
            # Test that the price has not changed
            print("{} price {}".format(symbol, getStockPrice(symbol)))

        # Calculate all share index
        print("All share - {}".format(getAllShare()))

    except Exception as e:
        print("Error")
        print(e)


if __name__ == "__main__":
    # Main function which is run when the Python is executed
    initialise()
    testStockControl()
