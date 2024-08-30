# Чтение файла и объединение строк
with open('../data/filtered_spam_messages.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

# Объединение строк, разделенных пустыми строками
combined_lines = []
current_paragraph = []

for line in lines:
    stripped_line = line.strip()
    if stripped_line:
        current_paragraph.append(stripped_line)
    else:
        if current_paragraph:
            combined_lines.append(' '.join(current_paragraph))
            current_paragraph = []

# Добавление последнего параграфа, если он существует
if current_paragraph:
    combined_lines.append(' '.join(current_paragraph))

# Запись объединенного текста в новый файл
with open('../data/combined_spam.txt', 'w', encoding='utf-8') as file:
    for line in combined_lines:
        file.write(line + '\n')
