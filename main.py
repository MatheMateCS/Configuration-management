import argparse
import tkinter as tk
from tkinter import scrolledtext as st
from tarfile import TarFile

# Class that describes the window of user interface
class GUI: 
    def __init__(self): # Constructor
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
        self.display.insert(tk.END, f"@:$ ") #TODO: add username, hostname, cur dir

    def push_text(self): # Capturing the text from entry
        command = self.input_area.get()
        # processer <-- command 
        self.input_area.delete(0, tk.END)
        
    def display_text(self, text): # Setting text to display
        self.display.insert(tk.END, text + '\n')
        self.prompt_insert()


def get_args(): # Getting arguments transmitted to script
    parser = argparse.ArgumentParser()
    parser.add_argument("username", help="Имя пользователя")
    parser.add_argument("hostname", help="Имя компьютера")
    parser.add_argument("path_to_archive", help="Путь до архива")
    parser.add_argument("path_to_script", help="Путь до стартового скрипта")
    return parser.parse_args()

def main():
    args = get_args()
    Gui = GUI()
    # print(args.username, args.hostname, args.path_to_archive, args.path_to_script)


main()

