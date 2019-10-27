#! /usr/bin/python3
import os
os.chdir('') # working dir
import rest_api as api
from random import random
from time import sleep
from math import floor
import logging
logger=logging.getLogger()
logger.handlers = []
logging.basicConfig(filename=f"{os.getcwd()}/random_bot.log",format='%(asctime)s - %(process)d-%(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.DEBUG)


# --------------------------

api_key="" # put your your API key
secret="" # put your secret key
leverage= 4 # Set the leverage to 4
# --------------------------

session=api.Account(api_key,secret,leverage)


##

def random_side(p=0.5):
    x=random()
    if x<p: return "Buy"
    return "Sell"


if __name__ == '__main__':
    logging.info('Bot starts')

    while True:
        if session.my_position()['result'][0]['side']=="Buy":
            session.cancel_all_pending_order()
            logging.info('Close long position @ market')
            size=session.my_position()['result'][0]['size']
            session.market_close("Sell", size)

        if session.my_position()['result'][0]['side']=="Sell":
            session.cancel_all_pending_order()
            logging.info('Close short position @ market')
            size=session.my_position()['result'][0]['size']
            session.market_close("Buy", size)



        if session.my_position()['result'][0]['side']=="None":
            session.cancel_all_pending_order()
            logging.info('No position')
            if session.get_active_order()['result']['data'][0]['order_status']!="Cancelled":
                logging.info('Cancel active orders if any')
                session.cancel_active_order(session.get_active_order()['result']['data'][0]['order_id'])

            side=random_side()
            logging.info('Choose random side')
            if side=="Buy": # Go long for random reason
                logging.info('Going long randomly')
                price=floor(float(session.get_orderbook()['result'][0]['ask_price'])-0.5)
                stop_loss=floor(float(price*0.99)) # SL @ 1%
                take_profit=floor(float(price*1.03)) # TP @ 3 %
                wallet_balance=session.my_position()['result'][0]['wallet_balance']
                leverage=session.my_position()['result'][0]['leverage']
                size=floor((wallet_balance*leverage*price-1)*0.9)
                session.place_active_order(side, size, price, stop_loss, take_profit)

            else: # Go short for random reason
                logging.info('Going short randomly')
                price=floor(float(session.get_orderbook()['result'][0]['bid_price'])+0.5)
                stop_loss=floor(float(price*1.01)) # SL @ 1%
                take_profit=floor(float(price*0.97)) # TP @ 3 %
                wallet_balance=session.my_position()['result'][0]['wallet_balance']
                leverage=session.my_position()['result'][0]['leverage']
                size=floor((wallet_balance*leverage*price-1)*0.9)
                session.place_active_order(side, size, price, stop_loss, take_profit)
        logging.info('Sleep for 2 hours')
        sleep(2*3600)


