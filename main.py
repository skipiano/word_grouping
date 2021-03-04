import csv

# parses input file and outputs a json object of folder names corresponding to the elements inside
# uses _ as the default delimiter
def parse(file_name):
    parse(file_name, '_')

def parse(file_name, delimiter):
    with open(file_name) as csv_file:
        temp_names = csv.reader(csv_file)
        names = [[]]
        folders = [[]]
        index = 0
        for name in temp_names:
            names[index] = name.split(delimiter)
            folders[index] = list(names[index])
            folders[index].pop(len(folders[index])-1)
        folder_dict = {}