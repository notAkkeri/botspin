# main.py
import tkinter as tk
from spin import SpinApp

def main():
    root = tk.Tk()
    app = SpinApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
