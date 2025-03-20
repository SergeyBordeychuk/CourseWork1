from src.decorators import file_writer


@file_writer()
def my_function(x, y):
    return x + y

def test_file_writer(capsys):
    my_function(1,2)
    captured =capsys.readouterr()

    assert captured.out == ''
