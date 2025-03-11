import datetime
import json
import os
from collections import Counter
from dotenv import load_dotenv

import pandas as pd
import requests
import yfinance as yf

load_dotenv()
API_KEY = os.getenv("API_KEY")

def reader_excel(path: str):
    """Функция считывает финансовые операции excel файлов"""
    excel_file = pd.read_excel(path)
    list_excel = excel_file.to_dict(orient='records')
    return list_excel


def greeting_now(current_time:str):
    """Возвращает приветствие по текущему времени"""
    if int(current_time[11:13]) <= 6:
        return 'Доброй ночи'
    elif int(current_time[11:13]) <= 12:
        return 'Доброе утро'
    elif int(current_time[11:13]) <= 18:
        return 'Добрый день'
    elif int(current_time[11:13]) <= 24:
        return 'Добрый вечер'


def sort_operations_by_amount(list_operations:list, date_start: str, date_end: str) ->list:
    """Возвращает топ 5 транзакций по платежу"""
    sorted_operations_by_amount = [0]
    date = date_end.split('-')
    top_operations = []
    top_tranzitions = [{"date": '', "amount": 0, "category": '', "description": ''},{"date": '', "amount": 0, "category": '', "description": ''},{"date": '', "amount": 0, "category": '', "description": ''},{"date": '', "amount": 0, "category": '', "description": ''},{"date": '', "amount": 0, "category": '', "description": ''}]
    for operation in list_operations:
        if isinstance(operation['Дата платежа'], str):
            date_operations = operation['Дата платежа'].split('.')
        if ((operation['Статус'] == 'OK') and (date[0] == date_operations[2]) and (date[1] == date_operations[1]) and
                (int(date[2]) >= int(date_operations[0]))):
            if operation['Сумма платежа'] * -1 > sorted_operations_by_amount[-1]:
                sorted_operations_by_amount.append(operation['Сумма платежа'] * -1)
    sort_operations = sorted(sorted_operations_by_amount[1:], reverse=True)[:5]
    for top_amount in sort_operations:
        for operation in list_operations:
            if isinstance(operation['Дата платежа'], str):
                date_operations = operation['Дата платежа'].split('.')
                if (top_amount == operation['Сумма платежа'] * -1) and (operation['Статус'] == 'OK') and (date[0] == date_operations[2]) and (
                     date[1] == date_operations[1]) and (int(date[2]) >= int(date_operations[0])):
                    top_operations.append(operation)
    top_operations = top_operations[:5]
    for i in range(0,5):
        top_tranzitions[i]["date"] = top_operations[i]['Дата платежа']
        top_tranzitions[i]["amount"] = top_operations[i]['Сумма платежа'] * -1
        top_tranzitions[i]["category"] = top_operations[i]['Категория']
        top_tranzitions[i]["description"] = top_operations[i]['Описание']
    return top_tranzitions


def exchange_rate(start_date: str, end_date: str):
    """Возвращает цену валюты"""
    base = 'RUB'
    url = f"https://api.apilayer.com/exchangerates_data/fluctuation?start_date={start_date}&end_date={end_date}&base={base}"

    payload = {}
    headers = {
        "apikey": API_KEY
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    result = response.json()
    with open('user_settings.json') as f:
        currency_settings = json.load(f)["user_currencies"]
    list_currency = [{} for _ in range(len(currency_settings))]
    for i in range(0, len(currency_settings)):
        list_currency[i]['currency'] = currency_settings[i]
        list_currency[i]['rate'] = round(1 / result['rates'][currency_settings[i]]['end_rate'], 2)
    return list_currency


def card_stats(path: str, date_start:str, date_end: str) -> list:
    """Возвращает статистику по каждой карте"""
    operations = reader_excel(path)
    card = []
    date = date_end.split('-')
    for operation in operations:
        if isinstance(operation['Дата платежа'], str):
            date_operations = operation['Дата платежа'].split('.')
        if (operation['Статус'] == 'OK') and (date[0] == date_operations[2]) and (date[1] == date_operations[1]) and (int(date[2]) >= int(date_operations[0])):
            card.append(operation['Номер карты'])
    card_numbers = list(Counter(card))
    cards_statistic = [{"last_digits": '', "total_spent": 0, "cashback": 0} for _ in range(len(card_numbers))]
    for operation in operations:
        if isinstance(operation['Дата платежа'], str):
            date_operations = operation['Дата платежа'].split('.')
        if (operation['Статус'] == 'OK') and (date[0] == date_operations[2]) and (date[1] == date_operations[1]) and (int(date[2]) >= int(date_operations[0])): # and (operation['Дата платежа'][3:5] == date_start[5:7]) and (operation['Дата платежа'][6:] == date_start[:4]) and (int(operation['Дата платежа'][:2]) <= int(date_end[8:10])):
            for i in range(0, len(card_numbers)):
                 cards_statistic[i]['last_digits'] = card_numbers[i]
                 if operation['Номер карты'] == card_numbers[i]:
                     cards_statistic[i]['total_spent'] += operation['Сумма платежа'] * -1
                 if operation['Номер карты'] == card_numbers[i]:
                     cards_statistic[i]['cashback'] += round(operation['Сумма платежа'] * -1 / 100, 2)
    return cards_statistic


def stock_prices():
    """Возвращает цену валюты s&p500"""
    with open('user_settings.json') as f:
        stock_settings = json.load(f)["user_stocks"]
    stock_prices = [{'stock': '', 'price': 0} for _ in range(len(stock_settings))]
    for i in range(len(stock_settings)):
        for to in stock_settings:
            stock = yf.Ticker(to)
            hist = stock.history(period="1d").to_dict()['Open']
            for key, value in hist.items():
                stock_prices[i]['price'] = value
                stock_prices[i]['stock'] = to
    return stock_prices





# def all_cost(path:str):
#     operations = reader_excel(path)
#     all_cost = {"expenses":{"total_amount": 0, "main": [{},{},{},{},{},{},{},{}], "transfer_and_cash":[{},{}]}}
#     cost = 0
#     for operation in operations:
#         if operation['Статус'] == 'OK':
#             if operation['Сумма платежа'] < 0:
#                 cost += operation['Сумма платежа'] * -1
#     all_cost["expenses"]["total_amount"] = cost
#
#
#     return all_cost




# print(all_cost('C:/Users/1/PycharmProjects/Coursework1/data/operations.xlsx'))















