from datetime import datetime
from csv_module import load_table as load_csv, save_table as save_csv
from pickle_module import load_table as load_pickle, save_table as save_pickle

# Задание 5 (работа с DateTime) - сложность 1
def parse_datetime(date_str, date_format="%m/%d/%Y"):
    """
    Преобразует строку в объект datetime.

    :param date_str: Строка с датой и временем.
    :param date_format: Формат строки даты и времени.
    :return: Объект datetime.
    """
    try:
        return datetime.strptime(date_str, date_format)
    except ValueError as e:
        raise ValueError(f"Ошибка при преобразовании строки '{date_str}' в datetime: {e}")

def format_datetime(date_obj, date_format="%m/%d/%Y"):
    """
    Преобразует объект datetime в строку.

    :param date_obj: Объект datetime.
    :param date_format: Формат строки даты и времени.
    :return: Строка с датой и временем.
    """
    try:
        return date_obj.strftime(date_format)
    except AttributeError as e:
        raise ValueError(f"Ошибка при преобразовании объекта '{date_obj}' в строку: {e}")

def convert_datetime_column(table, column=0, date_format="%m/%d/%Y"):
    """
    Преобразует столбец DateTime в формат даты.

    :param table: Исходная таблица.
    :param column: Номер или имя столбца.
    :param date_format: Формат строки даты и времени.
    :return: Обновленная таблица с преобразованным столбцом DateTime.
    """
    if isinstance(column, int):
        col_index = column
    else:
        col_index = table['headers'].index(column)

    for row in table['data']:
        try:
            row[col_index] = parse_datetime(row[col_index], date_format)
        except ValueError as e:
            print(f"Ошибка при преобразовании значения '{row[col_index]}' в столбце '{table['headers'][col_index]}': {e}")

    return table

#Задание 1 - сложность 1
def load_table_multiple(*file_paths, encoding='utf-8'):
    """
    Загружает таблицу из нескольких файлов и объединяет их в одну таблицу.

    :param file_paths: Пути к файлам.
    :param encoding: Кодировка файлов (по умолчанию 'utf-8').
    :return: Словарь с атрибутами таблицы и данными.
    """
    combined_table = None
    for file_path in file_paths:
        if file_path.endswith('.csv'):
            table = load_csv(file_path, encoding=encoding)
        elif file_path.endswith('.pkl'):
            table = load_pickle(file_path)
        else:
            raise ValueError(f"Неподдерживаемый формат файла: {file_path}")

        if combined_table is None:
            combined_table = table
        else:
            if combined_table['headers'] != table['headers']:
                raise ValueError(f"Несоответствие структуры столбцов файлов: {file_path}")
            combined_table['data'].extend(table['data'])

    return combined_table

#Задание 2 - сложность 1
def save_table_multiple(table, file_path_pattern, max_rows, encoding='utf-8'):
    """
    Сохраняет таблицу в несколько файлов, разбивая её на части по заданному максимальному количеству строк в каждом файле.

    :param table: Словарь с атрибутами таблицы и данными.
    :param file_path_pattern: Шаблон пути к файлам (например, 'part_{}.csv').
    :param max_rows: Максимальное количество строк в каждом файле.
    :param encoding: Кодировка файлов (по умолчанию 'utf-8').
    """
    headers = table['headers']
    data = table['data']
    num_files = (len(data) + max_rows - 1) // max_rows

    for i in range(num_files):
        start = i * max_rows
        end = start + max_rows
        part_data = data[start:end]
        part_table = {'headers': headers, 'data': part_data}
        file_path = file_path_pattern.format(i + 1)

        if file_path.endswith('.csv'):
            save_csv(file_path, part_table, encoding=encoding)
        elif file_path.endswith('.pkl'):
            save_pickle(file_path, part_table)
        else:
            raise ValueError(f"Неподдерживаемый формат файла: {file_path}")

#Задание 3 - сложность 1
def concat(table1, table2):
    """
    Склеивает две таблицы.

    :param table1: Первая таблица.
    :param table2: Вторая таблица.
    :return: Объединенная таблица.
    """
    if table1['headers'] != table2['headers']:
        raise ValueError("Структуры столбцов таблиц не совпадают.")

    combined_table = {
        'headers': table1['headers'],
        'data': table1['data'] + table2['data']
    }
    return combined_table

def split(table, row_number):
    """
    Разбивает одну таблицу на две по номеру строки.

    :param table: Исходная таблица.
    :param row_number: Номер строки, по которой разбивается таблица.
    :return: Две таблицы.
    """
    if row_number < 0 or row_number >= len(table['data']):
        raise ValueError("Некорректный номер строки для разбиения таблицы.")

    table1 = {
        'headers': table['headers'],
        'data': table['data'][:row_number]
    }

    table2 = {
        'headers': table['headers'],
        'data': table['data'][row_number:]
    }

    return table1, table2
