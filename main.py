import tkinter as tk
import random as rng

SCORES = [1,
          2,
          3,
          4,
          5,
          6,
          'Three of a Kind',
          'Four of a Kind',
          'Five of a Kind',
          'Full House',
          'Small Straight',
          'Large Straight',
          'Chance']

class Game(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        self.dice = [Die(self) for i in range(5)]
        for i in self.dice: i.pack()


class Die(tk.Checkbutton):
    def __init__(self, master):
        self.bool = tk.BooleanVar()
        self.bool.set(True)
        self.num = tk.IntVar()
        self.num.set(0)
        tk.Checkbutton.__init__(self, master=master, textvar=self.num, var=self.bool)


class ScoreFrame(tk.Frame):

    def __init__(self, master, name):
        self.master = master
        self.name = name
        self.label = tk.Label(self, text=name)



if __name__ == '__main__':
    root = tk.Tk()
    game = Game(root)
    game.pack()
    root.mainloop()