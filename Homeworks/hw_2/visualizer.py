import argparse
import tkinter as tk
from tkinter import scrolledtext as st

# Displaying a window with graph code text
def display(text: str)->None:
    window = tk.Tk()
    window.title("Graph code")
    window.wm_attributes("-topmost", 1)
    window.resizable(False, True)
    window.grid_rowconfigure(0, weight=0)
    window.grid_columnconfigure(0, weight=1)
    display = st.ScrolledText(window, height=40, width=100)
    display.configure(background="#000000", foreground="#FFFFFF")
    display.grid(row=0, column=0)
    display.insert(tk.END, f"{text}")
    display.config(state='disabled')
    window.mainloop()

def main()->None:
    parser = argparse.ArgumentParser()
    parser.add_argument("src_path", help="Path to graph code") # Path to the source Mermaid code
    src_path = parser.parse_args().src_path
    with open(src_path, "r") as src:
        text = src.read()
        display(text)

if __name__ == "__main__":
    main()
