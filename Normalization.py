import os
import re
import codecs


def clean_space(string):
    """
    Removes spaces at the beginning of a line
    :param string:
        The line of text to check.
    :return:
        Clean line of text
    """
    string = ' '.join(string.split())
    return string


def remove_invalid_symbols(dir):
    """
    Remove invalid symbols in textfile
    :param dir:
        Directory with fairytales, which needs to be cleaned of unnecessary symbols
    :return:
        Cleaned fairytales files
    """
    tail = ''
    with open(dir, "r+", encoding='utf-8') as file_in:
        lines = file_in.readlines()
        for line in lines:
            line = clean_space(line)  # call function to remove spaces between words
            tail += line

    with open(dir, "w+") as file_out:
        replacements = {'\n\n': ' ', '--': ' ', '-': ' ', ';': '.', 'NOTE': '', '&': ' ', '[1]': '', '[2]': '',
                        '[3]': '', '[4]': '', '[5]': '', '[6]': '', '[7]': '', '[8]': '', '[9]': '',
                        '[10]': '',
                        '[': '(', ']': ')', 'Illustration': '', '\n': ' '}
        clear_tail = re.sub('({})'.format('|'.join(map(re.escape, replacements.keys()))),
                            lambda m: replacements[m.group()], tail)
        file_out.write(clear_tail)  # overwrite the file


for x in os.listdir('./tales'):  # loop through all files in a directory
    fullname = os.path.join('./tales', x)
    try:
        remove_invalid_symbols(fullname)
    except:
        continue
