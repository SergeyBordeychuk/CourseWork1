from src.utils import reader_excel


def simple_search(path:str, string_search:str):
    """Простой поиск по строке"""
    operations = reader_excel(path)
    operations_with_string = []
    json_answer = {}
    for operation in operations:
        if isinstance(operation['Категория'], str) and (string_search in operation['Категория']):
            operations_with_string.append(operation)
        elif isinstance(operation['Описание'], str) and (string_search in operation['Описание']):
            operations_with_string.append(operation)
    json_answer['transactions'] = operations_with_string
    return json_answer
