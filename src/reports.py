import datetime

from pandas import DataFrame

from src.decorators import file_writer

today = str(datetime.datetime.now().date())

@file_writer('reports.txt')
def spending_by_category(operations, category: str, date: str = today):
    date_end = date
    month_end = int(date[5:7]) - 3
    print(month_end)
    if month_end <= 0:
        date_start = str(int(date[:4])-1) + '-' + str(12 + month_end) + '-' + date[8:]
    else:
        if len(str(int(date[5:7])- month_end)) == 1:
            date_start = date[:5] + '0' + str(int(date[5:7])- 3) + date[7:]
        else:
            date_start = date[:5] + str(int(date[5:7]) - 3) + date[7:]
    # operations_dict = operations.to_dict()
    # return date_start, date_end
    # for i in range(len(operations_dict['category'])):
    #     if (operations_dict['category'][i] == category) and ((operations_dict['date'][:4] == date_start[:4]) and (operations_dict['date'][:4] == date_start[:4]))
    return
print(spending_by_category('', '', today))