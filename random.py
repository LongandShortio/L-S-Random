#! /usr/bin/python3
import os
import rest_api as api
from random import random
from time import sleep
from math import floor

# --------------------------

api_key="" # Type your API key
secret="" # Type your secret key

# --------------------------

session=api.Account(api_key,secret,4) # Connect to Bybit and set the leverage to 4

# --------------------------

def random_side(p=0.5):
# Returns "Buy" with a probability p and "Sell" with a probability (1-p). By default p=0.5
    x=random()
    if x<p: return "Buy"
    return "Sell"


if __name__ == '__main__':
    while True:

        if session.my_position()['result'][0]['side']=="None": # Check if there is a current position open
            if session.get_active_order()['result']['data'][0]['order_status']!="Cancelled": # Cancel any active pending order
                session.cancel_active_order(session.get_active_order()['result']['data'][0]['order_id'])

            side=random_side()
            print(side)
            if side=="Buy": # Go long for random reason
                print("Going long")
                price=floor(float(session.get_orderbook()['result'][0]['ask_price'])-2)
                stop_loss=floor(float(price*0.985)) # SL @ 1.5%
                take_profit=floor(float(price*1.03)) # TP @ 3 %
                wallet_balance=session.my_position()['result'][0]['wallet_balance']
                leverage=session.my_position()['result'][0]['leverage']
                size=floor((wallet_balance*leverage*price-1)*0.9)
                print(price, stop_loss, take_profit,wallet_balance, leverage,size)
                print(session.place_active_order(side, size, price, stop_loss, take_profit))

            else: # Go short for random reason
                print("Going short")
                price=floor(float(session.get_orderbook()['result'][0]['bid_price'])+2)
                stop_loss=floor(float(price*1.015)) # SL @ 1.5%
                take_profit=floor(float(price*0.97)) # TP @ 3 %
                wallet_balance=session.my_position()['result'][0]['wallet_balance']
                leverage=session.my_position()['result'][0]['leverage']
                size=floor((wallet_balance*leverage*price-1)*0.9)
                print(price, stop_loss, take_profit,wallet_balance, leverage,size)
                print(session.place_active_order(side, size, price, stop_loss, take_profit))

        sleep(60*10) # Wait for 10 minutes
