import argparse
import sys
import tkinter as tk
from tkinter import scrolledtext as st
import tarfile

# Class that describes the window of user interface
class GUI: 
    def __init__(self, args): # Constructor
        # Getting arguments for subsequent using
        self.args = args

        # Binding processer
        self.processer = Processer(args.path_to_archive)
   
        # Window settings
        self.main_window = tk.Tk() 
        self.main_window.title("GUI Shell Emulator")
        self.main_window.wm_attributes("-topmost", 1)
        self.main_window.resizable(False, True)
        self.main_window.grid_rowconfigure(0, weight=1)
        self.main_window.grid_columnconfigure(0, weight=1)

        # Display that shows actions in cmd
        self.display = st.ScrolledText(self.main_window, height=20, width=40)
        self.display.configure(background="#000000", foreground="#7FFF00")
        self.display.grid(row=0, column=0, columnspan=2, pady=5)
        self.prompt_insert()

        # Standard entry
        self.input_area = tk.Entry(self.main_window, width=30)
        self.input_area.configure(background="#000000", foreground="#7FFF00")
        self.input_area.grid(row=1, column=0, pady=2)
        
        # Button that launches the entered command processing
        self.enter_btn = tk.Button(self.main_window, text="Enter", command=self.push_text)
        self.enter_btn.configure(background="#47B1DE", font=("Arial", 14, "bold"), foreground="#FFFFFF")
        self.enter_btn.grid(row=1, column=1, padx=2, pady=2, sticky='n')
        
        self.main_window.mainloop()

    def close(self): # Closing the GUI
        self.main_window.quit()

    def prompt_insert(self): # Entering the prompt
        self.display.insert(tk.END, f"{self.args.username}@{self.args.hostname}:{self.processer.cur_dir}$ ") #TODO: add username, hostname, cur dir

    def push_text(self): # Capturing the text from entry
        # Command text wrapping
        command = self.input_area.get()
        self.input_area.delete(0, tk.END)
        self.display.insert(tk.END, command + '\n')

        # Processing command and printing result
        result = self.processer.process(command) 
        if self.processer.must_exit:
            self.close()
        self.display.insert(tk.END, result)
        self.prompt_insert()

# Class that operating with the user input
class Processer:
    def __init__(self, path_to_archive):
        self.must_exit = False
        self.path_to_archive = path_to_archive
        self.cur_dir = "~" # full path to current directory
        self.file_system = {}
        self.parse_archive()

    def parse_archive(self):
        if not tarfile.is_tarfile(self.path_to_archive):
            print("There is no .tar archive! Please create it before run the program.")
            self.must_exit = True
            return
        
        with tarfile.open(self.path_to_archive, 'r') as tar:
            self.file_system["~"] = list()
            for member in tar.getmembers():
                spath = member.path.split("/")
                if len(spath) == 1:
                    self.file_system["~"].append(spath[0])
                else:
                    if self.file_system.get(spath[-2]) == None:
                        self.file_system[spath[-2]] = list()
                    self.file_system[spath[-2]].append(spath[-1])
        print(self.file_system)

    def process(self, command): # Analysing command
        result, alst = "", command.split(" ")
        if alst[0] == "ls":
            result = self._ls(alst[1:])
        elif alst[0] == "exit":
            self._exit()
        elif alst[0] == "cd":
            result = self._cd(alst[1:])
        # elif command.startswith("cp "):

        # elif command.startswith("uptime "):

        # elif command.startswith("tree "):

        else:
            result = f'Command "{alst[0]}" is not found\n'
        return result

    def _ls(self, lst):
        print(lst)
        if not lst or not lst[0]:
            return " ".join(self.file_system[self.cur_dir.split("/")[-1]]) + "\n"
        else:
            if not(lst[0] in self.file_system[self.cur_dir.split("/")[-1]]):
                return f"There is no directory with name '{lst[0]}'\n"
            return " ".join(self.file_system[lst[0]]) + "\n"
    
    def _cd(self, lst):
        print(lst)
        if not lst or not lst[0]:
            return ""
        elif lst[0] == "..":
            if self.cur_dir == "~":
                return ""
            self.cur_dir = "/".join(self.cur_dir.split("/")[:-1])
            return ""
        else:
            if lst[0][-1] == "/":
                lst[0] = lst[0][:-1]
            if not(lst[0] in self.file_system[self.cur_dir.split("/")[-1]]):
                return f"There is no directory with name '{lst[0]}'\n"
            self.cur_dir += "/" + lst[0]
            return ""

    def _exit(self):
        self.must_exit = True

    # def _cp(self, arg1, arg2):
        #
    
    # def _uptime(self):
        #

    # def _tree(self, root_dir):
        #
    
           

def get_args(): # Getting arguments transmitted to script
    parser = argparse.ArgumentParser()
    parser.add_argument("username", help="Имя пользователя")
    parser.add_argument("hostname", help="Имя компьютера")
    parser.add_argument("path_to_archive", help="Путь до архива")
    parser.add_argument("path_to_script", help="Путь до стартового скрипта")
    return parser.parse_args()

def main():
    args = get_args()
    Gui = GUI(args)
    # print(args.username, args.hostname, args.path_to_archive, args.path_to_script)


main()

