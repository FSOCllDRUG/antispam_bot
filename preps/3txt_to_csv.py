import csv

# Чтение спам-сообщений из текстового файла
with open('../data/combined_spam.txt', 'r', encoding='utf-8') as file:
    spam_messages = file.readlines()

# Запись спам-сообщений в CSV файл
with open('../data/spam_messages.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['message'])  # Заголовок столбца
    for message in spam_messages:
        csvwriter.writerow([message.strip()])  # Запись каждого сообщения в отдельную строку

print("Спам-сообщения записаны в spam_messages.csv")