import csv
import json

folder_dict = {}

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
            # possible folder names should not have the last word to avoid having folders that contain empty strings
            folders[index].pop(len(folders[index])-1)
        global folder_dict
        folder_names = group_folders(folders)
        for i in range(names):
            folder_name = delimiter.join(folder_names[i])
            elt_name = delimiter.join(names[i][len(folder_names[i]):])
            if folder_name in folder_dict:
                folder_dict[folder_name].append(elt_name)
            else:
                folder_dict[folder_name] = [elt_name]
        return json.dumps(folder_dict)

# given an array of possible folder names return an array of folder name that should be used for each name


def group_folders(folders):
    folder_names = []
    for name in folders:
        max_folder_name = []
        for i in range(len(name)):
            for other_name in folders:
                if other_name == name:
                    continue
                if len(other_name) > i and name[:i+1] == other_name[:i+1]:
                    max_folder_name = name[:i+1]
                    break
        if not max_folder_name:
            folder_names.append(name)
        else:
            folder_names.append(max_folder_name)
    return folder_names
