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
    for j in range(len(folders)):
        name = folders[j]
        max_folder_name = []
        for i in range(len(name)):
            for k in range(len(folders)):
                other_name = folders[k]
                if j == k:
                    continue
                if len(other_name) > i and name[:i+1] == other_name[:i+1]:
                    max_folder_name = name[:i+1]
                    break
        if not max_folder_name:
            folder_names.append(name)
        else:
            folder_names.append(max_folder_name)
    # for name in folders:
    #     max_folder_name = []
    #     for i in range(len(name)):
    #         for other_name in folders:
    #             if other_name == name:
    #                 continue
    #             if len(other_name) > i and name[:i+1] == other_name[:i+1]:
    #                 max_folder_name = name[:i+1]
    #                 break
    #     if not max_folder_name:
    #         folder_names.append(name)
    #     else:
    #         folder_names.append(max_folder_name)
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


class createFolderWindow(object):
    def __init__(self, master):
        w = self.top = tk.Toplevel(master)
        self.t = tk.Label(w, text="New Folder Name:")
        self.t.pack(side=tk.LEFT)
        self.b = tk.Button(w, text="Add", command=self.cleanup)
        self.b.pack(side=tk.RIGHT)
        self.e = tk.Entry(w)
        self.e.pack(side=tk.RIGHT)

    def cleanup(self):
        self.value = self.e.get()
        create_folder(self.value)
        self.top.destroy()


class createFileWindow(object):
    def __init__(self, master, init_folder, file_name):
        w = self.top = tk.Toplevel(master)
        self.t = tk.Label(w, text="Destination Folder Name:")
        self.t.pack(side=tk.LEFT)
        self.b = tk.Button(w, text="Move", command=self.cleanup)
        self.b.pack(side=tk.RIGHT)
        self.e = tk.Entry(w)
        self.e.pack(side=tk.RIGHT)
        self.init_folder = init_folder
        self.file_name = file_name

    def cleanup(self):
        self.value = self.e.get()
        move_file(self.init_folder, self.value, self.file_name)
        self.top.destroy()


class mainWindow(object):
    def __init__(self, master):
        m = self.m = master
        self.scrollbar = tk.Scrollbar(m)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.folder_list = tk.Listbox(
            m, selectmode=tk.SINGLE, width=32, yscrollcommand=self.scrollbar.set)
        for folder_name in folder_dict:
            self.folder_list.insert(tk.END, folder_name)
            for file_name in folder_dict[folder_name]:
                self.folder_list.insert(tk.END, "    > " + file_name)
        self.folder_list.pack(side=tk.LEFT, fill=tk.BOTH)
        self.scrollbar.config(command=self.folder_list.yview)
        self.mb = tk.Menubutton(m, text="Options")
        self.mb.pack()
        self.mb.menu = tk.Menu(self.mb, tearoff=0)
        self.mb["menu"] = self.mb.menu
        self.mb.menu.add_command(label="Create New Folder",
                                 command=self.create_new_folder)
        self.mb.menu.add_command(
            label="Move Selected File", command=self.move_file)
        self.mb.pack()

    def create_new_folder(self):
        self.w = createFolderWindow(self.m)
        self.mb.wait_window(self.w.top)
        self.folder_list.delete(0, self.folder_list.size()-1)
        for folder_name in folder_dict:
            self.folder_list.insert(tk.END, folder_name)
            for file_name in folder_dict[folder_name]:
                self.folder_list.insert(tk.END, "    > " + file_name)

    def move_file(self):
        selected = self.folder_list.curselection()
        print(selected)
        if not selected:
            return
        index = 0
        init_folder = ""
        file_name1 = ""
        is_file = False
        global folder_dict
        print(folder_dict)
        for folder_name in folder_dict:
            if index == selected[0]:
                print("folder not a file")
                break
            index += 1
            print(index)
            for file_name in folder_dict[folder_name]:
                if index == selected[0]:
                    is_file = True
                    init_folder = folder_name
                    file_name1 = file_name
                    break
                index += 1
                print(index)
            if is_file:
                break
        if is_file:
            self.w = createFileWindow(self.m, init_folder, file_name1)
            self.mb.wait_window(self.w.top)
            self.folder_list.delete(0, self.folder_list.size()-1)
            for folder_name in folder_dict:
                self.folder_list.insert(tk.END, folder_name)
                for file_name in folder_dict[folder_name]:
                    self.folder_list.insert(tk.END, "\t> " + file_name)


if __name__ == "__main__":
    print(parse("names.csv"))
    root = tk.Tk()
    m = mainWindow(root)
    root.mainloop()
