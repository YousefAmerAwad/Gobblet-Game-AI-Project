from tkinter import *
from GUI import *

def main():
    root = Tk()
    root.geometry("1200x900")
    Gobblet = GUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
