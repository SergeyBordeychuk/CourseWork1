import pytest

from src.reports import spending_by_category
import pandas as pd

df = pd.read_excel('data/operations.xlsx')

@pytest.mark.parametrize('category, expected_result',[
    ('Переводы', '22773.0'),
    ('ЖКХ', '15618.67')
])
def test_spending_by_category(category, expected_result):
    assert spending_by_category(df, category, '2021-07-20') == expected_result