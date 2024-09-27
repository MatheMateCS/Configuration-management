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
        self.file_system = {} # key - full path, value - children
        self.parse_archive()

    def parse_archive(self):
        if not tarfile.is_tarfile(self.path_to_archive):
            print("There is no .tar archive! Please create it before run the program.")
            self.must_exit = True
            return
        
        with tarfile.open(self.path_to_archive, 'r') as tar:
            self.file_system["~"] = list()
            
            for member in tar.getmembers():
                spath = ("~/" + member.path).split("/")
                print(spath)

                if len(spath) == 2:
                    self.file_system["~"].append(spath[1])
                else:
                    if self.file_system.get("/".join(spath[:-1])) == None:
                        self.file_system["/".join(spath[:-1])] = list()
                    self.file_system["/".join(spath[:-1])].append(spath[-1])
        print(self.file_system)

    def process(self, command): # Analysing command
        result, command_s = "", command.split()
        print(command_s)
        if not command_s:
            return result
        elif command_s[0] == "ls":
            result = self._ls(command_s[1:])
        elif command_s[0] == "exit":
            self._exit()
        elif command_s[0] == "cd":
            result = self._cd(command_s[1:])
        elif command_s[0] == "cp":
            result = self._cp(command_s[1:])
        # elif command.startswith("uptime "):

        # elif command.startswith("tree "):

        else:
            result = f'Command "{command_s[0]}" is not found\n'
        return result

    def _ls(self, args):
        print(args)
        if not args or args[0] == "." or args[0] == "./": # current directory
            return " ".join(self.file_system[self.cur_dir]) + "\n"
        elif args[0] == ".." or args[0] == "../": # parent's directory
            if not(self.cur_dir == "~"):
                return " ".join(self.file_system["/".join(self.cur_dir.split("/")[:-1])]) + "\n"
            return ""
        else:
            args[0] = "/".join(filter(None, args[0].split("/"))) # ignore of last '/'
            if self.file_system.get(args[0]) != None: # if path is full
                return " ".join(self.file_system[args[0]]) + "\n"
            if args[0].startswith("./"):
                args[0] = args[0].replace("./", "", 1) # ignore of initial './'
            cur = self.cur_dir
            for dir in args[0].split("/"): # checking path on correctness
                if not (dir in self.file_system[cur]):
                    return f"There is no directory with name '{args[0]}'\n"
                cur += "/" + dir
            return " ".join(self.file_system[cur]) + "\n"

    def _cd(self, args):
        print(args)
        if not args or args[0] == "." or args[0] == "./":
            return ""
        elif args[0] == ".." or args[0] == "../":
            if not(self.cur_dir == "~"):
                self.cur_dir = "/".join(self.cur_dir.split("/")[:-1])
            return ""
        else:
            args[0] = "/".join(filter(None, args[0].split("/")))
            if self.file_system.get(args[0]) != None: 
                self.cur_dir = args[0]
                return ""
            if args[0].startswith("./"):
                args[0] = args[0].replace("./", "", 1)
            cur = self.cur_dir
            for dir in filter(None, args[0].split("/")):
                if not (dir in self.file_system[cur]):
                    return f"There is no directory with name '{args[0]}'\n"
                cur += "/" + dir
            self.cur_dir = cur
            return ""

    def _exit(self):
        self.must_exit = True

    def _cp(self, args):
        print(args)
        # if len(args) != 2:
        #     return "Command 'cp' must have two arguments.\n"
        # else:
            
    
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

