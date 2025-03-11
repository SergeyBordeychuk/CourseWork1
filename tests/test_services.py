import pytest

from src.services import simple_search

@pytest.mark.parametrize('string_search, length',[
    ('Переводы', 351),
    ('Перевод', 526),
    ('Топливо', 75)
])

def test_simple_search(string_search, length):
    assert len(simple_search('data/operations.xlsx', string_search)['transactions']) == length
