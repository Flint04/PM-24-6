from datetime import datetime
from dop_task import parse_datetime, format_datetime, convert_datetime_column

def get_rows_by_number(table, start, stop=None, copy_table=False):
    """
    Получение таблицы из одной строки или из строк из интервала по номеру строки.

    :param table: Исходная таблица.
    :param start: Начальный номер строки.
    :param stop: Конечный номер строки (не включительно). Если None, то берется только одна строка.
    :param copy_table: Флаг, указывающий, нужно ли копировать исходные данные.
    :return: Новая таблица или представление таблицы.
    """
    if stop is None:
        stop = start + 1

    if copy_table:
        new_table = {
            'headers': table['headers'],
            'data': table['data'][start:stop]
        }
        return new_table
    else:
        return {
            'headers': table['headers'],
            'data': table['data'][start:stop]
        }

def get_rows_by_index(table, *vals, copy_table=False):
    """
    Получение новой таблицы из одной строки или из строк со значениями в первом столбце, совпадающими с переданными аргументами.

    :param table: Исходная таблица.
    :param vals: Значения для поиска в первом столбце.
    :param copy_table: Флаг, указывающий, нужно ли копировать исходные данные.
    :return: Новая таблица или представление таблицы.
    """
    if copy_table:
        new_data = [row for row in table['data'] if row[0] in vals]
        new_table = {
            'headers': table['headers'],
            'data': new_data
        }
        return new_table
    else:
        return {
            'headers': table['headers'],
            'data': [row for row in table['data'] if row[0] in vals]
        }

def get_column_types(table, by_number=True):
    """
    Получение словаря вида «столбец: тип значений».

    :param table: Исходная таблица.
    :param by_number: Флаг, указывающий, нужно ли использовать целочисленные индексы столбцов.
    :return: Словарь с типами значений для каждого столбца.
    """
    column_types = {}
    num_columns = len(table['headers'])

    for col_index in range(num_columns):
        column_data = [row[col_index] for row in table['data']]
        column_type = str  # Default type

        for value in column_data:
            if value is None:
                continue
            if isinstance(value, int):
                column_type = int
            elif isinstance(value, float):
                column_type = float
            elif isinstance(value, bool):
                column_type = bool
            elif isinstance(value, datetime):
                column_type = datetime

        if by_number:
            column_types[col_index] = column_type
        else:
            column_types[table['headers'][col_index]] = column_type

    return column_types

def set_column_types(table, types_dict, by_number=True):
    """
    Задание словаря вида столбец: тип_значений.

    :param table: Исходная таблица.
    :param types_dict: Словарь с типами значений для каждого столбца.
    :param by_number: Флаг, указывающий, нужно ли использовать целочисленные индексы столбцов.
    """
    num_columns = len(table['headers'])

    for col_index in range(num_columns):
        if by_number:
            col_key = col_index
        else:
            col_key = table['headers'][col_index]

        if col_key in types_dict:
            target_type = types_dict[col_key]
            for row in table['data']:
                try:
                    if row[col_index] is None:
                        continue
                    if target_type == datetime:
                        row[col_index] = parse_datetime(row[col_index])
                    else:
                        row[col_index] = target_type(row[col_index])
                except ValueError:
                    print(f"Ошибка преобразования значения '{row[col_index]}' в тип {target_type} для столбца {col_key}")

    return table

def get_values(table, column=0):
    """
    Получение списка значений (типизированных согласно типу столбца) таблицы из столбца либо по номеру столбца, либо по имени столбца.

    :param table: Исходная таблица.
    :param column: Номер или имя столбца.
    :return: Список значений из указанного столбца.
    """
    if isinstance(column, int):
        col_index = column
    else:
        col_index = table['headers'].index(column)

    column_data = [row[col_index] for row in table['data']]
    return column_data

def get_value(table, column=0):
    """
    Получение одного значения (типизированного согласно типу столбца) из столбца для таблицы с одной строкой.

    :param table: Исходная таблица.
    :param column: Номер или имя столбца.
    :return: Значение из указанного столбца.
    """
    if isinstance(column, int):
        col_index = column
    else:
        col_index = table['headers'].index(column)

    if table['data']:
        return table['data'][0][col_index]
    else:
        return None

def set_values(table, values, column=0):
    """
    Задание списка значений values для столбца таблицы (типизированных согласно типу столбца) либо по номеру столбца, либо по имени столбца.

    :param table: Исходная таблица.
    :param values: Список значений для установки.
    :param column: Номер или имя столбца.
    """
    if isinstance(column, int):
        col_index = column
    else:
        col_index = table['headers'].index(column)

    num_rows = len(table['data'])
    if len(values) != num_rows:
        raise ValueError(f"Количество значений ({len(values)}) не соответствует количеству строк ({num_rows}) в таблице.")

    for i, value in enumerate(values):
        table['data'][i][col_index] = value

def set_value(table, value, column=0):
    """
    Задание одного значения для столбца таблицы с одной строкой (типизированного согласно типу столбца) либо по номеру столбца, либо по имени столбца.

    :param table: Исходная таблица.
    :param value: Значение для установки.
    :param column: Номер или имя столбца.
    """
    if isinstance(column, int):
        col_index = column
    else:
        col_index = table['headers'].index(column)

    if table['data']:
        table['data'][0][col_index] = value
    else:
        raise ValueError("Таблица пуста, невозможно установить значение.")

def print_table(table):
    """
    Печатает таблицу в консоль.

    :param table: Словарь с атрибутами таблицы и данными.
    """
    try:
        # Печатаем заголовки
        print('\t'.join(table['headers']))
        # Печатаем данные
        for row in table['data']:
            print('\t'.join(map(lambda x: 'None' if x is None else str(x), row)))
    except Exception as e:
        raise ValueError(f"Ошибка при печати таблицы: {e}")
