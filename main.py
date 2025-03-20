from src.reports import spending_by_category
from src.services import simple_search
from src.views import main_page
import pandas as pd


df = pd.read_excel('data/operations.xlsx')

if __name__ == '__main__':
    print(main_page('data/operations.xlsx', '2021-07-20 19:38:01'))
    print(simple_search('data/operations.xlsx', 'Топливо'))
    spending_by_category(df, 'ЖКХ', '2021-07-20')
