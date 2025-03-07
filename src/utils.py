import datetime
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
    if int(current_time[11:13]) <= 6:
        return 'Доброй ночи'
    elif int(current_time[11:13]) <= 12:
        return 'Доброе утро'
    elif int(current_time[11:13]) <= 18:
        return 'Добрый день'
    elif int(current_time[11:13]) <= 24:
        return 'Добрый вечер'


def sort_operations_by_amount(list_operations:list) ->list:
    sorted_operations_by_amount = [0]
    top_operations = []
    top_tranzitions = [{"date": '', "amount": 0, "category": '', "description": ''},{"date": '', "amount": 0, "category": '', "description": ''},{"date": '', "amount": 0, "category": '', "description": ''},{"date": '', "amount": 0, "category": '', "description": ''},{"date": '', "amount": 0, "category": '', "description": ''}]
    for operation in list_operations:
        if operation['Сумма платежа'] * -1 > sorted_operations_by_amount[-1]:
            if operation['Статус'] == 'OK':
                sorted_operations_by_amount.append(operation['Сумма платежа'] * -1)
    sort_operations = sorted(sorted_operations_by_amount[1:], reverse=True)[:5]
    for top_amount in sort_operations:
        for operation in list_operations:
            if top_amount == operation['Сумма платежа'] * -1:
                top_operations.append(operation)
    top_operations = top_operations[:5]
    for i in range(0,5):
        top_tranzitions[i]["date"] = top_operations[i]['Дата платежа']
        top_tranzitions[i]["amount"] = top_operations[i]['Сумма платежа'] * -1
        top_tranzitions[i]["category"] = top_operations[i]['Категория']
        top_tranzitions[i]["description"] = top_operations[i]['Описание']
    return top_tranzitions


def exchange_rate_usd_eur():
    start_date = str(datetime.datetime.now().date())[:8] + '01'
    end_date = str(datetime.datetime.now().date())
    base = 'RUB'
    url = f"https://api.apilayer.com/exchangerates_data/fluctuation?start_date={start_date}&end_date={end_date}&base={base}"

    payload = {}
    headers = {
        "apikey": API_KEY
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    result = response.json()
    list_currency = [{},{}]
    list_currency[0]['currency'] = 'USD'
    list_currency[1]['currency'] = 'EUR'
    list_currency[0]['rate'] = result['rates']['USD']['end_rate']
    list_currency[1]['rate'] = result['rates']['EUR']['end_rate']
    return list_currency


def card_stats(path):
    operations = reader_excel(path)
    card = []
    for operation in operations:
        card.append(operation['Номер карты'])
    card_numbers = list(Counter(card))
    cards_statistic = [{"last_digits": '', "total_spent": 0, "cashback": 0} for _ in range(len(card_numbers))]
    for operation in operations:
        if operation['Статус'] == 'OK':
            for i in range(0, len(card_numbers)):
                 cards_statistic[i]['last_digits'] = card_numbers[i]
                 if operation['Номер карты'] == card_numbers[i]:
                     cards_statistic[i]['total_spent'] += operation['Сумма платежа'] * -1
                 if operation['Номер карты'] == card_numbers[i]:
                     cards_statistic[i]['cashback'] += operation['Сумма платежа'] * -1 / 100
    return cards_statistic


def stock_prices():
    to = '^GSPC'
    stock_prices = {'stock': to, 'price': 0}
    sp500 = yf.Ticker(to)
    hist = sp500.history(period="1d").to_dict()['Open']
    for key, value in hist.items():
        stock_prices['price'] = value
    return stock_prices


def all_cost(path:str):
    operations = reader_excel(path)
    all_cost = {"expenses":{"total_amount": 0, "main": [{},{},{},{},{},{},{},{}], "transfer_and_cash":[{},{}]}}
    cost = 0
    for operation in operations:
        if operation['Статус'] == 'OK':
            if operation['Сумма платежа'] < 0:
                cost += operation['Сумма платежа'] * -1
    all_cost["expenses"]["total_amount"] = cost


    return all_cost




# print(all_cost('C:/Users/1/PycharmProjects/Coursework1/data/operations.xlsx'))















