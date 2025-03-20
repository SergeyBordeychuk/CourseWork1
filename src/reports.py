import datetime

from pandas import DataFrame

today = str(datetime.datetime.now().date())


def spending_by_category(operations: DataFrame, category: str, date: str = today):
    """Возвращает отчёт трат по категориям"""
    spending = 0
    date_end = date
    month_end = int(date[5:7]) - 3
    if month_end <= 0:
        date_start = str(int(date[:4])-1) + '-' + str(12 + month_end) + '-' + date[8:]
    else:
        if len(str(int(date[5:7])- month_end)) == 1:
            date_start = date[:5] + '0' + str(int(date[5:7])- 3) + date[7:]
        else:
            date_start = date[:5] + str(int(date[5:7]) - 3) + date[7:]
    operations_dict = operations.to_dict()
    list_end = date_end.split('-')
    list_start = date_start.split('-')
    for i in range(len(operations_dict['Категория'])):
        if isinstance(operations_dict['Дата платежа'][i], str):
            list_date = operations_dict['Дата платежа'][i].split('.')
        else:
            continue
        if date_end[:4] == date_start[:4]:
            if (operations_dict['Статус'][i] == 'OK') and ((operations_dict['Категория'][i] == category)
                and ((list_date[2] == list_start[0]) and (int(list_start[1])) <= int(list_date[1]) <= int(list_end[1])-1)):
                spending += operations_dict['Сумма платежа'][i] * -1

            if (operations_dict['Статус'][i] == 'OK') and ((operations_dict['Категория'][i] == category)
                and ((list_date[2] == list_start[0])) and ((list_date[1] == list_end[1]) and (list_date[0] == list_end[2]))):
                spending += operations_dict['Сумма платежа'][i] * -1
        else:
            if (operations_dict['Статус'][i] == 'OK') and ((operations_dict['Категория'][i] == category) and
            (((list_date[2] == list_start[0]) and (int(list_date[1]) >= int(list_start[1]))
            or ((list_date[2] == list_end[0]) and
                (int(list_date[1]) <= int(list_end[1])-1))))):
                spending += operations_dict['Сумма платежа'][i] * -1
            if (operations_dict['Статус'][i] == 'OK') and ((list_date[2] == list_end[0]) and
                    ((int(list_date[1]) == int(list_end[1])) and (list_date[0] <= list_end[2]))):
                spending += operations_dict['Сумма платежа'][i] * -1
    return f'{spending}'
