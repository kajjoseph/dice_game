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
        self.scores = {i: None for i in SCORES}
        self.temp_scores = {i: 0 for i in SCORES}
        # TODO: pack and test ScoreFrames
        for i in self.dice: i.pack()
        tk.Button(self, text='Roll', command=self.roll).pack()

    def check_scores(self):
        self.temp_scores = {i: 0 for i in SCORES}
        values = sorted([n.num.get() for n in self.dice])
        for i in range(1, 7):
            self.temp_scores[i] = sum([x for x in values if x == i])
            if values.count(i) >= 3:
                self.temp_scores['Three of a Kind'] = sum(values)
                if len(set(values)) == 2:
                    self.temp_scores['Full House'] = 25
            if values.count(i) >= 4:
                self.temp_scores['Four of a Kind'] = sum(values)
        if len(set(values)) == 1:
            self.temp_scores['Five of a Kind'] = 50
        str_values = [str(a) for a in values]
        for i in ['1234', '2345', '3456']:
            if i in ''.join(str_values):
                self.temp_scores['Small Straight'] = 30
                break
        if ''.join(str_values) in ['12345', '23456']:
            self.temp_scores['Large Straight'] = 40
        self.temp_scores['Chance'] = sum(values)
        for a, n in self.temp_scores.items():
            print(f'{a}: {n}')

    def roll(self):
        for i in self.dice:
            if i.bool.get() or not i.num.get():
                i.num.set(rng.randint(1, 6))
        self.check_scores()


class Die(tk.Checkbutton):
    
    def __init__(self, master):
        self.bool = tk.BooleanVar()
        self.bool.set(True)
        self.num = tk.IntVar()
        self.num.set(0)
        tk.Checkbutton.__init__(self, master=master, textvar=self.num, var=self.bool)


class ScoreFrame(tk.Frame):

    def __init__(self, master, name, score=None):
        self.master = master
        tk.Frame.__init__(self, master)
        self.name = name
        self.score = score
        self.button = tk.Button(self, text=name, command=self.press)

    def press(self):
        if self.score is None:
            self.master.scores[self.name] = self.master.temp_scores[self.name]


if __name__ == '__main__':
    root = tk.Tk()
    game = Game(root)
    game.pack()
    root.mainloop()
