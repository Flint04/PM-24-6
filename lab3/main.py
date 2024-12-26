from csv_module import load_table as load_csv, save_table as save_csv
from pickle_module import load_table as load_pickle, save_table as save_pickle
from text_module import save_table as save_text
from table_operations import get_rows_by_number, get_rows_by_index, get_column_types, set_column_types, get_values, get_value, set_values, set_value, print_table
from dop_task import parse_datetime, format_datetime, convert_datetime_column, load_table_multiple, save_table_multiple, concat, split
# Пример использования
if __name__ == "__main__":
    # Загрузка таблицы из CSV файла с кодировкой utf-8
    csv_table = load_csv(r'файл.csv', encoding='utf-8')
    print("CSV Table:")
    print_table(csv_table)

    # Сохранение таблицы в CSV файл с кодировкой utf-8
    save_csv(r'Сохранение csv.csv', csv_table, encoding='utf-8')

    # Загрузка таблицы из Pickle файла
    pickle_table = load_pickle(r'Для pickle.pkl')
    print("\nPickle Table:")
    print_table(pickle_table)

    # Сохранение таблицы в Pickle файл
    save_pickle(r'Сохранение pickle.pcl', pickle_table)

    # Сохранение таблицы в текстовый файл
    save_text(r'Сохранение txt.txt', csv_table)

    # Получение строк по номеру из CSV таблицы
    rows_by_number_csv = get_rows_by_number(csv_table, 1, 3)
    print("\nСтрока по номеру из CSV таблицы:")
    print_table(rows_by_number_csv)

    # Получение строк по индексу из CSV таблицы
    rows_by_index_csv = get_rows_by_index(csv_table, 'Bob')
    print("\nСтрока по индексу из CSV таблицы:")
    print_table(rows_by_index_csv)

    # Получение строк по номеру из Pickle таблицы
    rows_by_number_pickle = get_rows_by_number(pickle_table, 1, 3)
    print("\nСтрока по номеру из Pickle таблицы:")
    print_table(rows_by_number_pickle)

    # Получение строк по индексу из Pickle таблицы
    rows_by_index_pickle = get_rows_by_index(pickle_table, 'Alice')
    print("\nСтрока по индексу из Pickle таблицы:")
    print_table(rows_by_index_pickle)

    # Получение типов столбцов из CSV таблицы
    column_types_csv = get_column_types(csv_table, by_number=True)
    print("\nТипы столбцов из CSV таблицы (по номеру):")
    print(column_types_csv)

    # Получение типов столбцов из Pickle таблицы
    column_types_pickle = get_column_types(pickle_table, by_number=False)
    print("\nТипы столбцов из Pickle таблицы (по имени):")
    print(column_types_pickle)

    # Задание типов столбцов для CSV таблицы
    new_types_csv = {0: str, 1: float, 2: str}
    csv_table = set_column_types(csv_table, new_types_csv, by_number=True)

    # Задание типов столбцов для Pickle таблицы
    new_types_pickle = {'Name': str, 'Age': str, 'City': str}
    pickle_table = set_column_types(pickle_table, new_types_pickle, by_number=False)

    # Получение типов столбцов из CSV таблицы
    column_types_csv = get_column_types(csv_table, by_number=True)
    print("\nТипы столбцов из CSV таблицы (по номеру):")
    print(column_types_csv)

    # Получение типов столбцов из Pickle таблицы
    column_types_pickle = get_column_types(pickle_table, by_number=False)
    print("\nТипы столбцов из Pickle таблицы (по имени):")
    print(column_types_pickle)

    # Получение значений из столбца CSV таблицы
    values_csv = get_values(csv_table, column=1)
    print("\nЗначения из столбца 1 CSV таблицы:")
    print(values_csv)

    # Получение значений из столбца Pickle таблицы
    values_pickle = get_values(pickle_table, column='Age')
    print("\nЗначения из столбца 'Age' Pickle таблицы:")
    print(values_pickle)

    # Получение значения из столбца Pickle таблицы с одной строкой
    value_pickle = get_value(rows_by_index_pickle, column='Age')
    print("\nЗначение из столбца 'Age' с одной строкой:")
    print(value_pickle)

    # Задание значений для столбца CSV таблицы
    new_values_csv = [10, 20]
    set_values(csv_table, new_values_csv, column=1)
    print("\nCSV Table после изменения значений в столбце 1:")
    print_table(csv_table)

    # Задание значения для столбца CSV таблицы с одной строкой
    set_value(rows_by_number_csv, 40, column=1)
    print("\nCSV Table с одной строкой после изменения значения в столбце 1:")
    print_table(rows_by_number_csv)

    # Задание значений для столбца Pickle таблицы
    new_values_pickle = [25, 35]
    set_values(pickle_table, new_values_pickle, column='Age')
    print("\nPickle Table после изменения значений в столбце 'Age':")
    print_table(pickle_table)

    # Задание значения для столбца Pickle таблицы с одной строкой
    set_value(rows_by_index_pickle, 50, column='Age')
    print("\nPickle Table с одной строкой после изменения значения в столбце 'Age':")
    print_table(rows_by_index_pickle)

    # Преобразование столбца DateTime в формат даты
    csv_table = convert_datetime_column(csv_table, column='DateTime')
    print("\nCSV Table после преобразования столбца DateTime в формат даты:")
    print_table(csv_table)

    # Загрузка таблицы из нескольких CSV файлов
    csv_files = [
        r'файл.csv',
        r'файл2.csv'
    ]
    csv_table = load_table_multiple(*csv_files, encoding='utf-8')
    print("\nТаблица, загруженная из нескольких файлов:")
    print_table(csv_table)

    # Сохранение таблицы в несколько CSV файлов с максимальным количеством строк 2
    save_table_multiple(csv_table, r'Сохранение csv_part_{}.csv', max_rows=2, encoding='utf-8')

    csv_table1 = load_csv(r'файл.csv', encoding='utf-8')
    csv_table2 = load_csv(r'файл2.csv', encoding='utf-8')

    # Склеивание двух таблиц
    combined_csv_table = concat(csv_table1, csv_table2)
    print("\nСклеиная CSV таблица:")
    print_table(combined_csv_table)

    # Разбиение таблицы на две по номеру строки
    table1, table2 = split(combined_csv_table, 2)
    print("\nРабзитая CSV таблица часть 1:")
    print_table(table1)
    print("\nРабзитая CSV таблица часть 2:")
    print_table(table2)

    # Загрузка таблицы из нескольких несовместимых CSV файлов
    csv_files = [
        r'файл.csv',
        r'файл3.csv'
    ]
    csv_table = load_table_multiple(*csv_files, encoding='utf-8')
    print("CSV Table:")
    print_table(csv_table)