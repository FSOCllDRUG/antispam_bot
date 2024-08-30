with open('data/spam_messages.txt', 'r') as file:
    lines = file.readlines()

with open('data/filtered_spam_messages.txt', 'w') as file:
    for line in lines:
        if not line.startswith('YOUR_NICKNAME'):
            file.write(line)
