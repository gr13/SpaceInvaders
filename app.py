import tkinter as tk
from tkinter import ttk
from classes.SpaceInvaders import SpaceInvaders

root = tk.Tk()
root.title = "Space Invaders"
root.resizable(False, False)
board = SpaceInvaders()
board.pack()

root.mainloop()
