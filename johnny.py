# -*- coding: utf-8 -*-
"""
Created on Mon May  4 04:07:48 2020

@author: blue2
"""
from pyrh_crypto import Trader
import time
import numpy as np

trader = Trader('', '')

trader.save_session('test1')
purchased_price = 0
total = 0
balance = 0.01 #dollar
position_balance = 0 #dollar in crypto
position_crypto = 0 #how many crypto i bought
profit = 0 #how much have i made in this session and hwta am i risking this session
ask_price = 0
bid_price = 0
mark_price = 0
calculated_average = np.array([ask_price, bid_price, mark_price])
positions = np.array([total, balance, position_balance, position_crypto, purchased_price, profit], dtype=float)

def get_crypto_price(symbol):
    now = trader.crypto.quote(symbol)
    ask_price, bid_price, mark_price  = now.ask, now.bid, now.mark
    current_price = np.array([ask_price, bid_price, mark_price,])
    return current_price

def calculate_spread(current_price):
    spread = current_price[0] - current_price[1]
    return spread

def calculate_avg_over_time(symbol, length, avg):
    global calculated_average
    start = time.time()
    while time.time() < start + length:
        get = get_crypto_price(symbol)
        time.sleep(1)
        get_next = get_crypto_price(symbol)
        #two_second_sum = (get + get_next)
        two_second_avg = (get + get_next) / 2
        calc_average = two_second_avg
        calculated_average = avg
    return calc_average

def buy_amount_crypto(current_price, symbol, amount_buy_crypto):
    positions[4] = current_price[1]
    positions[2] = amount_buy_crypto
    trader.crypto.buy(symbol, amount_buy_crypto, price = current_price[0])
    print('Bought',{amount_buy_crypto},{symbol},'at',{current_price[1]})

def sell_amount_crypto(current_price, symbol, amount_sell_crypto, previous_price):
    trader.crypto.sell(symbol, amount_sell_crypto, price = current_price[1])
    #profit = previous_price - current_price[2]
    profit = (previous_price/current_price[2])*amount_sell_crypto
    positions[1] = positions[1] + profit
    positions[5] = positions[5] + profit
    print('Sold',{amount_sell_crypto},'at',{current_price[2]},'for',{profit},'profit', 'made $:', {positions[5]})
    
def crypto_trader(symbol, length, balance, purchased_price):
    global calculated_average
    bool_purchase = False

    baseline = calculate_avg_over_time(symbol, length, calculated_average)
    session_avg_ask = baseline[0]
    session_avg_bid = baseline[1]
    session_avg_bid = baseline[2]
    k = 2
    while True:
            time.sleep(2)
            baseline = calculate_avg_over_time(symbol, length, calculated_average)
            time.sleep(1)
            query = calculate_avg_over_time(symbol, length, calculated_average)
            session_avg_ask = (session_avg_ask + max(baseline[0].item(), query[0].item())) / k
            session_avg_bid = (session_avg_bid + max(baseline[1].item(), query[1].item())) / k
            session_avg_mark = (session_avg_bid + max(baseline[2].item(), query[2].item())) / k
            current_session_data = (session_avg_ask, session_avg_bid)
            #ratio = positions[0] / query[3]
            positions[1], purchased_price, position_balance = balance, positions[4], positions[2]
           #print(current_session_data)
            if session_avg_ask > query[0] and balance > 0 and bool_purchase == False:
                if session_avg_mark > query[2]:
                    return
                else:
                    buy_amount_crypto(query, symbol, balance)
                    baseline = query
                    bool_purchase = True
                    print(current_session_data, positions[1])
            elif 1.5*purchased_price < 1.0001*query[1] and position_balance > 0 and bool_purchase == True:
                sell_amount_crypto(query, symbol, balance, baseline[0])
                baseline = query
                bool_purchase = False
                print(current_session_data, positions[1], '1.5')
            elif 1.1*purchased_price < 1.0001*query[1] and position_balance > 0 and bool_purchase == True:
                sell_amount_crypto(query, symbol, balance, baseline[0])
                baseline = query
                bool_purchase = False
                print(current_session_data, positions[1], '1.1')
            elif 1.05*purchased_price < 1.0001*query[1] and position_balance > 0 and bool_purchase == True:
                sell_amount_crypto(query, symbol, balance, baseline[0])
                baseline = query
                bool_purchase = False
                print(current_session_data, positions[1], '1.05')
            elif 1.01*purchased_price < 1.0001*query[1] and position_balance > 0 and bool_purchase == True:
                sell_amount_crypto(query, symbol, balance, baseline[0])
                baseline = query
                bool_purchase = False
                print(current_session_data, positions[1], '1.01')
            elif 1.005*purchased_price < 1.0001*query[1] and position_balance > 0 and bool_purchase == True:
                sell_amount_crypto(query, symbol, balance, baseline[0])
                baseline = query
                bool_purchase = False
                print(current_session_data, positions[1], '1.005')
            elif 1.001*purchased_price < 1.0001*query[1] and position_balance > 0 and bool_purchase == True:
                sell_amount_crypto(query, symbol, balance, baseline[0])
                baseline = query
                bool_purchase = False  
                print(current_session_data, positions[1], '1.001')
            elif 1.0005*purchased_price < 1.0001*query[1] and position_balance > 0 and bool_purchase == True:
                sell_amount_crypto(query, symbol, balance, baseline[0])
                baseline = query
                bool_purchase = False
                print(current_session_data, positions[1], '1.0005')
            elif 1.0003*purchased_price < 1.0001*query[1] and position_balance > 0 and bool_purchase == True:
                sell_amount_crypto(query, symbol, balance, baseline[0])
                baseline = query
                bool_purchase = False
                print(current_session_data, positions[1], '1.0003')
            elif 0.995*purchased_price > 1.0001*query[1] and position_balance > 0 and bool_purchase == True:
                sell_amount_crypto(query, symbol, balance, baseline[0])
                baseline = query
                bool_purchase = False
                print(current_session_data, positions[1], '0.095')
    
#a = calculate_avg_over_time('BTC', 5)
#b = calculate_avg_over_time('BTC', 5)
#crypto_trader_simulator('BTC',1, 0.5*balance, purchased_price)
crypto_trader('BTC', 0.5, balance, purchased_price)
