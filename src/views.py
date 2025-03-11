import datetime
import json

from src.utils import card_stats, exchange_rate, greeting_now, reader_excel, sort_operations_by_amount, stock_prices


now = str(datetime.datetime.now())

start_time = str(datetime.datetime.now().date())[:8] + '01'
end_time = str(datetime.datetime.now().date())


def main_page(path:str, date: str):
    """Вовзращает json-строку главной страницы"""
    date_end = date[:10]
    date_start = f'{date[:8]}01'
    operations = reader_excel(path)
    string = {"greeting":"",
                   "cards":[{
                       "last_digits": '',
                       "total_spent": '',
                       "cashback": ''
                   }
                ],
                   "top_transactions": [],
                   "currency_rates": [{
                       "currency": '',
                        "rate": 0
                   }],
                   "stock_prices": []
                   }
    string['greeting'] = greeting_now(date)
    string['cards'] = card_stats(path, date_start, date_end)
    string["top_transactions"] = sort_operations_by_amount(operations, date_start, date_end)
    string["currency_rates"] = exchange_rate(date_start, date_end)
    string["stock_prices"] = stock_prices()
    json_string = json.dumps(string)
    return json_string


# def events_page(date:str, diaposone:str = f'{start_time}-{end_time}'):
#     json_string = {"expenses": {
#             "total_amount": 0,
#             "main": [],
#             "transfers_and_cash": []
#           },
#           "income": {
#             "total_amount": 0,
#             "main": []
#           },
#           "currency_rates": [],
#           "stock_prices": []
#         }
#
#     json_string["currency_rates"] = exchange_rate()
#     json_string["stock_prices"] = stock_prices()
