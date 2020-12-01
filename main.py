'''
The dice game Yahtzee implemented using the tkinter library
'''

import tkinter as tk
from tkinter.messagebox import askyesno
import random as rng

DEBUG = True

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
        self.top_score = 0 
        self.bonus = 0 # If top score is >= 63, score 35 bonus points
        self.bottom_score = 0
        self.temp_scores = {i: 0 for i in SCORES}
        self.remaining_rolls = 3
        for i, n in enumerate(self.dice):
            n.grid(row=i, column=0, padx=25)
        tk.Button(self, text='Roll', command=self.roll).grid(row=i+1, column=0, padx=25)
        row, col = 0, 1
        self.score_table = []
        for i, n in self.scores.items():
            frame = ScoreFrame(self, i, n)
            self.score_table.append(frame)
            frame.grid(row=row, column=col)
            row += 1
            if row == 6:
                row = 0
                col += 1
        self.stats = StatusFrame(self)
        self.stats.grid(row=row, column=col)
        if DEBUG:
            tk.Button(self, text='Test Win', command=self.victory).grid(row=row+1, column=col)
        
    def check_scores(self):
        '''
        Checks scores and stores in a dict to be checked against player score.
        '''
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
        str_values = ''.join(sorted(list(set([str(a) for a in values]))))
        for i in ['1234', '2345', '3456']:
            if i in str_values:
                self.temp_scores['Small Straight'] = 30
                break
        if str_values in ['12345', '23456']:
            self.temp_scores['Large Straight'] = 40
        self.temp_scores['Chance'] = sum(values)
        if DEBUG:
            for a, n in self.temp_scores.items():
                print(f'{a}: {n}')

    def roll(self):
        if self.remaining_rolls:
            for i in self.dice:
                if i.bool.get() or not i.num.get():
                    i.num.set(rng.randint(1, 6))
            self.check_scores()
            self.remaining_rolls -= 1

    def victory(self):
        if None in self.scores.values():
            for i in SCORES:
                self.scores[i] = rng.randint(0, 50)
        top_score = sum([self.scores[i] for i in SCORES[:6]])
        bonus = 35 if top_score >= 63 else 0
        bottom_score = sum([self.scores[i] for i in SCORES[6:]])
        total = top_score + bottom_score + bonus
        msg = f'Top Score: {top_score}\n Bonus: {bonus}\n Bottom Score: {bottom_score}\n Total: {total}'
        if askyesno('Victory!', msg):
            self.scores = {i: None for i in SCORES}
            for i in self.score_table:
                i.reset()
        else:
            self.quit()

    def update(self):
        self.stats.top_score_var.set(self.top_score)
        self.stats.bottom_score_var.set(self.bottom_score)

    def __call__(self):
        self.pack()
        self.mainloop()


class Die(tk.Checkbutton):
    
    def __init__(self, master):
        self.bool = tk.BooleanVar()
        self.bool.set(True)
        self.num = tk.IntVar()
        self.num.set(0)
        tk.Checkbutton.__init__(self, master=master, textvar=self.num, var=self.bool)


class ScoreFrame(tk.Frame):
    # TODO: Add support for bonus Yahtzees
    def __init__(self, master, name, score=None):
        self.master = master
        tk.Frame.__init__(self, master)
        self.name = name
        self.score = score
        self.score_var = tk.IntVar()
        self.button = tk.Button(self, text=name, command=self.press)
        self.button.pack(side='left')
        self.label = tk.Label(self, textvar=self.score_var)
        self.label.pack(side='left')

    def press(self):
        if self.score is None and 0 not in [i.num.get() for i in self.master.dice]:
            self.master.scores[self.name] = self.master.temp_scores[self.name]
            self.score = self.master.temp_scores[self.name]
            self.score_var.set(self.score)
            for i in self.master.dice:
                i.num.set(0)
                i.bool.set(True)
            if self.name in range(1, 7):
                self.master.top_score += self.score
            else:
                self.master.bottom_score += self.score
            self.master.update()
            self.master.remaining_rolls = 3
            self.button.config(bg='cornflower blue')
            self.label.config(bg='cornflower blue')
            if None not in self.master.scores.values():
                self.master.victory()
    
    def reset(self):
        self.score_var.set(0)
        self.button.config(bg='#F0F0F0')
        self.label.config(bg='#F0F0F0')


class YahtzeeFrame(ScoreFrame):

    def __init__(self, master):
        ScoreFrame.__init__(self, master, name='Yahtzee')
    
    def press(self):
        pass


class StatusFrame(tk.Frame):

    def __init__(self, master):
        self.master = master
        tk.Frame.__init__(self, master)
        self.top_score_var = tk.IntVar()
        self.top_score_var.set(self.master.top_score)
        self.bottom_score_var = tk.IntVar()
        self.bottom_score_var.set(self.master.bottom_score)
        self.bonus_var = tk.IntVar()
        self.bonus_var.set(0)
        tk.Label(self, text='Top Score').pack(side='top')
        tk.Label(self, textvar=self.top_score_var).pack(side='top')
        tk.Label(self, text='Bottom Score').pack(side='top')
        tk.Label(self, textvar=self.bottom_score_var).pack(side='top')


if __name__ == '__main__':
    Game(tk.Tk())()
