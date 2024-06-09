import tkinter as tk

from src.clientGUI import ClientGUI


def main():
    root = tk.Tk()
    ClientGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
