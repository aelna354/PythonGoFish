from tkinter import *
import time
import random

class GoFish():
	def __init__(self, master):
		self.master = master

		T = Text(self.master, height=13, width=65)
		T.insert(END, "Turn Count: X\nOpponent's Hand Size:\nYou have completed     X Books.\nComputer has completed X books.")
		T.grid(row=0, column=1)
		T.config(state=DISABLED)

		buttons1 = Frame(self.master)
		for counter, value in enumerate(["A", "2", "3", "4", "5", "6", "7"]):
			Button(buttons1, width=8, text=f"{value} (x)").grid(row=0, column=counter, padx=8)
		buttons1.grid(row=1, column=0, columnspan=7)

		buttons2 = Frame(self.master)
		for counter, value in enumerate(["8", "9", "10", "J", "K", "Q"]):
			Button(buttons2, width=8, height=1, text=f"{value} (x)").grid(row=0, column=counter, padx=8)
		buttons2.grid(row=2, column=0, columnspan=6)

		Button(self.master, width=8, text="Surrender", bg="yellow", fg="black").grid(row=3, column=0)
		Button(self.master, bg='silver', text="Deck (n cards)", height=2).grid(row=3, column=1)
		Button(self.master, width=8, text="Start Turn", bg='green', fg='white').grid(row=3, column=2)

program = Tk()
program.title("Go Fish Game")
program.resizable(False, False)
app = GoFish(program)
program.mainloop()