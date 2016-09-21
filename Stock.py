#!/usr/bin/python
# This is a base class for the stock object
# It holds parameters which are loaded upon start up and used for internal calculation
# It exposes a number of functions and  stores stock transactions in a list object.
from __future__ import division     # Necesary to allow floats to be calulated
import time                         # Necessary to calulate 'Now'


class Stock:
    # Common base class for Stock
    def __init__(self, symbol, type, lastDividend, fixedDividend, parVal):

        # Initialise the stock object
        self.symbol = symbol
        self.type = type
        self.lastDividend = lastDividend
        self.fixedDividend = fixedDividend
        self.parVal = parVal
        
        # Debug - initialisation confirmation
        print("Initialise Stock - {} {} {} {} {}".format(
            self.symbol, self.type, self.lastDividend, self.fixedDividend, self.parVal))

        # Initialise transactions list
        self.transactions = []


    def getDivYeild(self, marketPrice):
        # Calculate the Dividend Yeild
        try:
            if self.type == "Common":
                # Divide the last Dividend by the price to get the yeild
                print("Common Div Yeild {} / {}".format(self.lastDividend, marketPrice))
                return self.lastDividend/marketPrice
            else :
                # Divide fix div by 100 to get %, multiply by Par Value / Market price
                print("Fixed Div Yeild {} /{} {}".format(self.fixedDividend, self.parVal, marketPrice))
                return (((self.fixedDividend/100) * self.parVal)/ marketPrice)

        except Exception as e:
            raise e


    def getPERatio(self, marketPrice):
        # Calculate the P E ratio
        try:
            # Assumption here that dividend is dividend yeild
            dividend = self.getDivYeild(marketPrice)
            print("Div - {}".format(dividend))
            # Test for 0 as can't divide by 0
            if dividend == 0:
                return 0
            else:
                return marketPrice/dividend

        except Exception as e:
            raise e


    def addTransaction(self, timestamp, quantity, buySell, price):
        # Add a transaction to the transactions list
        try:
            transaction = [timestamp, quantity, buySell, price]
            print("Transaction - {}".format(transaction))       # debug
            self.transactions.append(transaction)               
            print("Transactions len {}".format(len(self.transactions)))  # debug
        except Exception as e:
            raise e


    def getVolWeightedPrice(self):
        # Return the volume weighted price of tx in the last 15 mins
        try:
            # Initialise variables
            price=0
            quantity=0
            now = int(time.time())

            # Loop through the transactions storing the value of any within the last 15 mins
            for transaction in self.transactions:
                # Assumption epoch timestamp is ok - if not then epoch needs calulating here
                if transaction[0] > (now - (15 * 60)):
                    # Sum the price * quantity (assumption - buy/sell is not relevant)
                    price += transaction[1] * transaction[3]
                    # Sum the quantity
                    quantity += transaction[1]

            # Return the Volume Weighted price
            return price/quantity

        except Exception as e:
            raise e


    def getMeanParams(self):
        # Return the sum of the tx prices and the total no of
        # tx for the All share index calculation
        try:
            # Initialise variables - use 1 as it will be multiplied
            sumPrice=1
            # Step through each transaction
            for transaction in self.transactions:
                # Buy/Sell assumed not to be relevant here so not taken into account
                sumPrice *= transaction[3]
                print("tx {} sum {}".format(transaction[3], sumPrice))  # Debug

            txCount = len(self.transactions)
            return sumPrice, txCount

        except Exception as e:
            raise e

