import json

import pytest

from src.utils import greeting_now, reader_excel, exchange_rate, stock_prices, sort_operations_by_amount, card_stats
from unittest.mock import patch


@pytest.mark.parametrize('date, expected_result, length',[
    ('2025-01-11 20:13:10', 'Добрый вечер', 12),
    ('2025-01-11 05:13:10', 'Доброй ночи', 11),
    ('2025-01-11 13:13:10', 'Добрый день', 11),
    ('2025-01-11 11:13:10', 'Доброе утро', 11)
        ])
def test_greeting_now(date, expected_result, length):
    assert greeting_now(date) == expected_result
    assert len(greeting_now(date)) == length


def test_reader_excel():
    assert len(reader_excel('data/operations.xlsx')) == 6705


def test_exchange_rate():
    with open("user_settings.json") as f:
        rate = json.load(f)["user_currencies"]
    assert len(exchange_rate('2025-01-01', '2025-01-05')) == len(rate)


@patch('yfinance.Ticker')
def test_stock_prices(mock_res):
    mock_res.return_value.history.return_value.to_dict.return_value = {'Open':{'price_stock': 10}}
    assert stock_prices() == [{'stock': '^GSPC', 'price': 10}]
    with open("user_settings.json") as f:
        stocks = json.load(f)["user_stocks"]
    assert len(stock_prices()) == len(stocks)


def test_sort_operations_by_amount():
    operations = reader_excel('data/operations.xlsx')
    assert len(sort_operations_by_amount(operations, '2021-07-01', '2021-07-20')) == 5
    assert sort_operations_by_amount(operations, '2021-07-01', '2021-07-20') == [{'date': '09.07.2021', 'amount': 13042.75, 'category': 'ЖКХ', 'description': 'ЖКУ Квартира'}, {'date': '09.07.2021', 'amount': 11148.96, 'category': 'ЖКХ', 'description': 'ЖКУ Квартира'}, {'date': '09.07.2021', 'amount': 9750.19, 'category': 'ЖКХ', 'description': 'ЖКУ Квартира'}, {'date': '14.07.2021', 'amount': 8400.0, 'category': 'Дом и ремонт', 'description': 'Magazin Mebel'}, {'date': '14.07.2021', 'amount': 2569.16, 'category': 'Супермаркеты', 'description': 'Дикси'}]



def test_card_stats():
    assert len(card_stats('data/operations.xlsx', '2021-07-01', '2021-07-20')) == 3




