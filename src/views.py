import datetime
import os

from dotenv import load_dotenv

from src.utils import (card_stats, exchange_rate_usd_eur, greeting_now,
                       reader_excel, sort_operations_by_amount, stock_prices)

load_dotenv()
API_KEY = os.getenv("API_KEY")

now = str(datetime.datetime.now())


def main_page(path:str):
    operations = reader_excel(path)
    json_string = {"greeting":"",
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
    json_string['greeting'] = greeting_now(now)
    json_string['cards'] = card_stats(path)
    json_string["top_transactions"] = sort_operations_by_amount(operations)
    json_string["currency_rates"] = exchange_rate_usd_eur()
    json_string["stock_prices"] = stock_prices()
    return json_string


def events_page(date:str, diaposone:str = ):
    json_string = {"expenses": {
            "total_amount": 0,
            "main": [],
            "transfers_and_cash": []
          },
          "income": {
            "total_amount": 0,
            "main": []
          },
          "currency_rates": [],
          "stock_prices": []
        }
    json_string["currency_rates"] = exchange_rate_usd_eur()
    json_string["stock_prices"] = stock_prices()
