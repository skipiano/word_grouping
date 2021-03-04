import csv
import json
import tkinter as tk

folder_dict = {}

# parses input file and outputs a json object of folder names corresponding to the elements inside


def parse(file_name, delimiter='_'):
    with open(file_name) as csv_file:
        temp_names = csv.reader(csv_file)
        names = []
        folders = []
        index = 0
        for name in temp_names:
            names.append(name[0].split(delimiter))
            folders.append(name[0].split(delimiter))
            # possible folder names should not have the last word to avoid having folders that contain empty strings
            folders[index].pop(len(folders[index])-1)
            index += 1
        global folder_dict
        folder_names = group_folders(folders)
        for i in range(len(names)):
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


def create_folder(folder_name):
    global folder_dict
    if folder_name in folder_dict:
        print("A folder with that name already exists: please try a different name.")
    else:
        folder_dict[folder_name] = []


def move_file(init_folder, dest_folder, file_name):
    global folder_dict
    if not dest_folder in folder_dict:
        print("A folder with that name does not exist: please select the correct folder or create a new folder.")
    else:
        folder_dict[init_folder].remove(file_name)
        folder_dict[dest_folder].append(file_name)


def popup():
    print("hi")


print(parse("names.csv"))
m = tk.Tk()
scrollbar = tk.Scrollbar(m)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
folder_list = tk.Listbox(m, selectmod=tk.SINGLE,
                         width=32, yscrollcommand=scrollbar.set)
for folder_name in folder_dict:
    folder_list.insert(tk.END, folder_name)
    for file_name in folder_dict[folder_name]:
        folder_list.insert(tk.END, "\t> " + file_name)
folder_list.pack(side=tk.LEFT, fill=tk.BOTH)
scrollbar.config(command=folder_list.yview)
mb = tk.Menubutton(m, text="Options")
mb.pack()
mb.menu = tk.Menu(mb, tearoff=0)
mb["menu"] = mb.menu
mb.menu.add_command(label="Create New Folder", command=popup)
mb.menu.add_command(label="Move Selected File", command=popup)
mb.pack()
m.mainloop()
