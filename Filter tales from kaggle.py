import re
from string import ascii_lowercase, digits

with open('kaggle_books.txt', 'r+', encoding='utf-8') as file:
    books = file.read()

patterns = [re.compile('_The Moral_.*?_Another_.*?\n\n\n', re.DOTALL),
            re.compile('\[Illustration.*?\]', re.DOTALL),
            re.compile(r'_.*?_\n\n')]

for pattern in patterns:
    books_clear = re.sub(pattern, '', books)

tales = books_clear.split('\n\n\n\n\n')

for tale in tales:
    tale = tale.replace('\n\n', '\n').strip()
    if len(tale) > 0:
        tale_split = tale.split('\n')
        if len(tale_split) > 5:
            allowed_letters = ascii_lowercase + digits + '_'
            title = tale_split[0]
            title = title.split('\n')
            title = title[0] if len(title[0]) > 0 else title[1]
            title = title.strip().replace(' ', '_').lower()
            title = ''.join([letter for letter in title if letter in allowed_letters])
            text = '\n'.join(tale_split[1:])
            with open('tales/' + title + '.txt', 'w+', encoding='utf-8') as t:
                t.write(text)
