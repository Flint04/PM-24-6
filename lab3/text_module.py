def save_table(file_path, table):
    """
    Сохраняет таблицу в текстовый файл.

    :param file_path: Путь к текстовому файлу.
    :param table: Словарь с атрибутами таблицы и данными.
    """
    try:
        with open(file_path, mode='w', encoding='utf-8') as file:
            # Записываем заголовки
            file.write('\t'.join(table['headers']) + '\n')
            # Записываем данные
            for row in table['data']:
                file.write('\t'.join(map(lambda x: '' if x is None else str(x), row)) + '\n')
    except Exception as e:
        raise ValueError(f"Ошибка при сохранении текстового файла: {e}")
