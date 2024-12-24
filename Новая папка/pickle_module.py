import pickle
from datetime import datetime

def auto_detect_column_types(table):
    """
    Автоматически определяет типы столбцов на основе значений в таблице.

    :param table: Исходная таблица.
    :return: Словарь с типами столбцов.
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
            break  # Останавливаем проверку, как только найден первый непустой элемент

        column_types[table['headers'][col_index]] = column_type

    return column_types

def load_table(file_path):
    """
    Загружает таблицу из Pickle файла.

    :param file_path: Путь к Pickle файлу.
    :return: Словарь с атрибутами таблицы и данными.
    """
    try:
        with open(file_path, mode='rb') as file:
            table = pickle.load(file)
            # Заменяем пустые строки на None
            table['data'] = [[None if cell == '' else cell for cell in row] for row in table['data']]
            table['column_types'] = auto_detect_column_types(table)
            print("В загруженной таблице столбцы имеют типы:", table['column_types'])
            return table
    except Exception as e:
        raise ValueError(f"Ошибка при загрузке Pickle файла: {e}")

def save_table(file_path, table):
    """
    Сохраняет таблицу в Pickle файл.

    :param file_path: Путь к Pickle файлу.
    :param table: Словарь с атрибутами таблицы и данными.
    """
    try:
        with open(file_path, mode='wb') as file:
            pickle.dump(table, file)
    except Exception as e:
        raise ValueError(f"Ошибка при сохранении Pickle файла: {e}")

