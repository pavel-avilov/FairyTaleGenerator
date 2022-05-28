from os import listdir
from os.path import isfile, join

fairytales_in_one_file = [f for f in listdir("tales/allTalesData") if isfile(join("tales/allTalesData", f))]  # list of fairytale files name
with open('tales/one_fairytales.txt', 'w+') as outfile:  # writing all files contents into one file
    for fname in fairytales_in_one_file:
        with open(f"tales/{fname}") as infile:
            for line in infile:
                outfile.write(line + "<|endoftext|>\n")
