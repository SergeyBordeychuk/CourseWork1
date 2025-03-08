import datetime
from functools import wraps

date = str(datetime.datetime.now())

def file_writer(file_name:str = 'reports.txt'):
    def my_decorator(func):
        '''Пишет результаты функций в файлы'''

        @wraps(func)
        def wrapper(*args,**kwargs):
            func_res = func(*args, **kwargs)
            with open(file_name, 'a') as f:
                f.write(f'{date} {func.__name__}\n')
                f.write(func_res)
        return wrapper
    return my_decorator
