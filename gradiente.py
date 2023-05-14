import pandas as pd
import pandas_ta as ta
import MetaTrader5 as mt5
import tkinter as tk
import time
import yfinance as yf
import matplotlib as mp
import matplotlib.pyplot as plt
from time import sleep
from datetime import date
import datetime
import pytz

def tradeGradienteLinear(ativo, lots, stopGain, stopLoss):
        mt5.initialize()
        listPrices = []
        listId = []
        while True:
            agoraBR = pytz.timezone('America/Sao_Paulo')
            agora = datetime.datetime.now(agoraBR)
            agora = agora.time()
            # Definir horários de referência
            inicio = datetime.time(10, 0, 0) # 10:00:00
            fim = datetime.time(16, 0, 0)    # 16:00:00
            if inicio <= agora <= fim:
                print(ativo)
                data = pd.DataFrame(mt5.copy_rates_from_pos(ativo, mt5.TIMEFRAME_M1, 0, 90))
                print(data)
                data['time'] = pd.to_datetime(data['time'], unit="s")
                data['mm9'] = data.ta.sma(9)

                comp = "Compra"
                vend = "Venda"
                rob = "Gradiente Linear"
                media = (list(data['mm9'])[-1])
                fechamento = (list(data['close'])[-1])

                print("====================================================")
                
                print("Média: ", media) 
                print("Fechamento:", fechamento)

                position = mt5.positions_total()
                print(position)

                print(position)
                
                if(position == 0):
                    print("Comprar primeira vez!")
                    point = mt5.symbol_info(ativo).point
                    price = mt5.symbol_info_tick(ativo).ask
                    deviation = 200
                    request = {
                        "action": mt5.TRADE_ACTION_DEAL,
                        "symbol": ativo,
                        "volume": lots,
                        "type": mt5.ORDER_TYPE_BUY,
                        "price": price,
                        "sl": price - 100 * point,
                        # "tp": price + 150 * point,
                        "sl": 0.0,
                        "tp": 0.0,
                        "deviation": deviation,
                        "magic": 234000,
                        "comment": "python script open",
                        "type_time": mt5.ORDER_TIME_GTC,
                    }
                    result = mt5.order_send(request)
                    # verificamos o resultado da execução
                    print("1. order_send(): by {} {} lots at {} with deviation={} points".format(ativo,lots,price,deviation));
                    if result.retcode != mt5.TRADE_RETCODE_DONE:
                        print("2. order_send failed, retcode={}".format(result.retcode))

                    listPrices.append(price)

                elif(position > 0 and fechamento < (ultimoPrice - 1.0) and len(listPrices) <= 2):
                    print("Comprar novamente!")
                    point = mt5.symbol_info(ativo).point
                    price = mt5.symbol_info_tick(ativo).ask
                    deviation = 200
                    request = {
                        "action": mt5.TRADE_ACTION_DEAL,
                        "symbol": ativo,
                        "volume": lots,
                        "type": mt5.ORDER_TYPE_BUY,
                        "price": price,
                        # "sl": price - 150 * point,
                        # "tp": price + 150 * point,
                        "sl": 0.0,
                        "tp": 0.0,
                        "deviation": deviation,
                        "magic": 234000,
                        "comment": "python script open",
                        "type_time": mt5.ORDER_TIME_GTC,
                    }
                    result = mt5.order_send(request)
                    # verificamos o resultado da execução
                    print("1. order_send(): by {} {} lots at {} with deviation={} points".format(ativo,lots,price,deviation));
                    if result.retcode != mt5.TRADE_RETCODE_DONE:
                        print("2. order_send failed, retcode={}".format(result.retcode))

                    listPrices.append(price)

                elif(position > 0 and fechamento > (ultimoPrice + 2.0)):
                    # position_id=result.order
                    price=mt5.symbol_info_tick(ativo).bid
                    deviation=200
                    request={
                        "action": mt5.TRADE_ACTION_DEAL,
                        "symbol": ativo,
                        "volume": lots,
                        "type": mt5.ORDER_TYPE_SELL,
                        # "position": position_id,
                        "price": price,
                        "deviation": deviation,
                        "magic": 234000,
                        "comment": "python script close",
                        "type_time": mt5.ORDER_TIME_GTC,
                        "type_filling": mt5.ORDER_FILLING_RETURN,
                    }
                    # enviamos a solicitação de negociação
                    result=mt5.order_send(request)
                    # verificamos o resultado da execução
                    print("3. close position #: sell {} {} lots at {} with deviation={} points".format(ativo,lots,price,deviation));
                    if result.retcode != mt5.TRADE_RETCODE_DONE:
                        print("2. order_sell failed, retcode={}".format(result.retcode))
                    if len(listPrices) != 0:
                        listPrices.pop()            
                else:
                    print("Esperar")                                                                                                                                                                                                                                                                                                                                                                            

                if len(listPrices) != 0:
                    print(listPrices)
                    ultimoPrice = listPrices[-1]


                print(type(price))
                print(type(ultimoPrice))
                print(price)
                print(ultimoPrice)
                print(listPrices)
                time.sleep(10)                                                                                                              
            else:
                print("A bolsa não está aberta")
                sleep(120)


            



tradeGradienteLinear("WINM23", 1.0, 0.0, 0.0)