import requests
import re
from collections import Counter
from bs4 import BeautifulSoup, NavigableString
from string import ascii_lowercase, digits


def save_txt(text, path):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)


def format_file_name(title, titles):
    allowed_letters = ascii_lowercase + digits + '_'

    title = title.split('\n')
    title = title[0] if len(title[0]) > 0 else title[1]
    title = title.strip().replace(' ', '_').lower()
    title = ''.join([letter for letter in title if letter in allowed_letters])
    titles.append(title)

    if title in titles:
        title = title + str(titles.count(title))

    return title + '.txt', titles


def exclude_black_list(content, black_list):
    return False if content.lower() in black_list else True


def format_text(start, end, exclude, num_words):
    text = ' '.join(t for t in between(start, end, exclude))
    text = '\n'.join(text.split("\n")[1:]).strip()
    num_words.append(len(text.split(' ')))
    return text, num_words


def between(start, end, exclude=[]):
    while start != end:
        if isinstance(start, NavigableString):
            yield start
        elif start.name in exclude:
            start = start.next_element
        start = start.next_element


main_urls = ['https://www.pitt.edu/~dash/folktexts.html',
             'https://www.pitt.edu/~dash/folktexts2.html']
base_url = 'https://www.pitt.edu/~dash/'

links = []

for url in main_urls:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    for a in soup.find_all('a'):
        a_href = a.get('href')
        links.append(a_href)

internal_links = [link.split('#')[0] for link in links if
                  link != None and 'folktexts' not in link and 'http' not in link]
internal_links.remove('')
internal_links = list(set(internal_links))

pages = []
total_progress = len(internal_links)
p = 0

for link in internal_links:
    progress = p * 100 / total_progress

    sub_url = base_url + link
    sub_page = requests.get(sub_url)

    pages.append(sub_page)

    if p in range(0, total_progress, 20):
        print(progress, '%')
    p += 1

soup_list = [BeautifulSoup(page.content, 'html.parser') for page in pages]
print(len(internal_links) == len(soup_list))

h2_count = {}
h2_content = []

for i in range(len(internal_links)):
    h2_list = soup_list[i].find_all('h2')
    h2_content.extend([h2.text.strip().lower() for h2 in h2_list])
    h2_count[internal_links[i]] = len(h2_list)

h2_content_count = Counter(h2_content).most_common()

h2_black_list = ['contents', 'links to related sites', 'related links', 'links to related tales',
                 'notes and bibliography', 'links']

type1 = [k for k, v in h2_count.items() if v != 0]
type2 = [k for k, v in h2_count.items() if v == 0]

content_dict = {internal_links[i]: soup_list[i] for i in range(len(internal_links))}

type1_content = {}

for page in type1:
    h2_list = content_dict[page].find_all('h2')
    h2_text = [h2.text.strip().lower() for h2 in h2_list]
    type1_content[page] = h2_text.count('contents') + h2_text.count('table of contents')

type1_with_content = [k for k, v in type1_content.items() if v != 0]
type1_without_content = [k for k, v in type1_content.items() if v == 0]

page_skip = 0
titles = []
num_words = []
exclude = ['h3']
end = soup_list[0].new_tag('hr')

for page in type1_with_content:
    type1_page_links = content_dict[page].find_all('a', attrs={'name': True})

    for a in type1_page_links[1:]:
        start = a.find_parent('h2')
        if start != None and exclude_black_list(start.get_text(), h2_black_list):
            title, titles = format_file_name(start.get_text(), titles)
            text, num_words = format_text(start, end, exclude, num_words)
            save_txt(text, 'tales/' + title) if num_words[-1] >= 15 else num_words.pop()
        else:
            page_skip += 1
