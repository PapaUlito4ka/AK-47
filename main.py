import tkinter as tk
from random import randint
from math import fabs
from tkinter import font

WIDTH = 500
HEIGHT  = 200
ROOT = tk.Tk()
ROOT.geometry(str(WIDTH) + 'x' + str(HEIGHT))

class Bits:
    # Respresents 10 bits of a number
    def __init__(self, random=True):
        self.x0 = randint(0, 1) & random
        self.x1 = randint(0, 1) & random
        self.x2 = randint(0, 1) & random
        self.x3 = randint(0, 1) & random
        self.x4 = randint(0, 1) & random
        self.x5 = randint(0, 1) & random
        self.x6 = randint(0, 1) & random
        self.x7 = randint(0, 1) & random
        self.x8 = randint(0, 1) & random
        self.x9 = randint(0, 1) & random

class Digit:
    # Draws one digit from bits of a number
    def __init__(self, bits: Bits=Bits(random=False)):
        self.y0 = (~bits.x2 & 1) | bits.x3 | bits.x1
        self.y1 = (~bits.x1 & 1) | (~(bits.x2 ^ bits.x3) & 1)
        self.y2 = (~(bits.x1 ^ bits.x3) & 1) | bits.x2 | bits.x0
        self.y3 = (bits.x1 ^ bits.x2) | bits.x1 & (~bits.x3 & 1) | bits.x0
        self.y4 = (~bits.x1 & 1) & (~bits.x3 & 1) | (~bits.x1 & 1) & bits.x2 | bits.x2 & (~bits.x3 & 1) | bits.x1 & (~bits.x2 & 1) & bits.x3 | bits.x0
        self.y5 = (~bits.x2 & 1) & (~bits.x3 & 1) | bits.x1 & (~bits.x2 & 1) | bits.x1 & (~bits.x3 & 1) | bits.x0
        self.y6 = (~bits.x1 & 1) & (~bits.x3 & 1) | bits.x2 & (~bits.x3 & 1)
    
    def draw_digit(self, x1, y1, x2, y2, canvas: tk.Canvas):
        # Draws digit in canvas
        x_len = fabs(x2 - x1)
        y_len = fabs(y2 - y1) // 2
        w = 3
        if self.y0:
            canvas.create_line(x2, y2, x2, y2 - y_len, fill='red', width=w)
        if self.y1:
            canvas.create_line(x2, y2 - y_len, x2, y1, fill='red', width=w)
        if self.y2:
            canvas.create_line(x1, y1, x1 + x_len, y1, fill='red', width=w)
        if self.y3:
            canvas.create_line(x1, y1 + y_len, x1 + x_len, y1 + y_len, fill='red', width=w)
        if self.y4:
            canvas.create_line(x1, y2, x2, y2, fill='red', width=w)
        if self.y5:
            canvas.create_line(x1, y1, x1, y1 + y_len, fill='red', width=w)
        if self.y6:
            canvas.create_line(x1, y1 + y_len, x1, y2, fill='red', width=w)


class Circle:
    # Circle for one diode
    def __init__(self, color='green'):
        self.color = color

    def draw_diode(self, x, y, r, canvas: tk.Canvas):
        # Draws diode
        return canvas.create_oval(x, y, x + r, y + r, fill=self.color)

class Number:
    # Represent whole number with 3 digits in it
    def __init__(self, bits: Bits):
        self.height = 100
        self.width = WIDTH
        self.digits = self.process_number(bits)
        self.canvas = tk.Canvas(ROOT, bg='green', height=self.height)
        self.canvas.pack(side='top', fill='x')
        self.bits = bits

    def sum_bits(self, number: Bits):
        # Get full number from bits
        num = 0
        for i, bit in enumerate(sorted(number.__dict__.keys(), key=lambda x: int(x[1]))):
            num += number.__dict__[bit] << i
        return num

    def get_digit(self, number):
        # Get digit bits from number
        digit = number % 10
        digit_bits = Bits(random=False)
        i = 0
        while digit > 0:
            digit_bits.__dict__[f'x{3 - i}'] = digit % 2
            digit //= 2
            i += 1
        return digit_bits

    def process_number(self, number):
        # Makes number with 3 digits
        num = self.sum_bits(number)
        bits_array = []
        for i in range(3):
            bits_array.append(Digit(bits=self.get_digit(num)))
            num //= 10
        return bits_array[::-1]

    def draw_number(self):
        # Draws 3 digits of a number
        pad = 20
        digit_height = 90
        digit_width = 50
        # First digit
        x01 = WIDTH // 2 - pad - digit_width
        x02 = x01 + digit_width
        # Second digit
        x11 = WIDTH // 2
        x12 = x11 + digit_width
        # Third digit
        x21 = WIDTH // 2 + pad + digit_width
        x22 = x21 + digit_width

        x_axis = [(x01, x02), (x11, x12), (x21, x22)]
        y1 = self.height - digit_height
        y2 = digit_height
        for i, digit in enumerate(self.digits):
            digit.draw_digit(x_axis[i][0], y1, x_axis[i][1], y2, self.canvas)

class Diodes:
    # Diode row with text 256...1
    def __init__(self, number: Number, random: Bits=None):
        self.height = 100
        self.width = WIDTH
        self.diodes = [Circle() for i in range(10)]
        self.canvas = tk.Canvas(ROOT, bg='green', height=self.height)
        self.canvas.pack(side='top', fill='x')
        self.number = number
        self.bits = self.number.bits
        self.random_bits = random

    def draw_diodes(self, one_player=False, bits: Bits=None):
        # Draws diode row
        pad = 20
        r = 15
        x = WIDTH // 2 - 4 * (pad + r)
        y = 50
        for i, diode in enumerate(self.diodes):
            self.diodes[i] = diode.draw_diode(x, y, r, self.canvas)
            self.canvas.tag_bind(self.diodes[i], '<Button-1>', self._helper(self.diodes[i]))
            self.canvas.create_text(x + r // 2, y - r, text='{}'.format(2 ** (9 - i)))
            if one_player:
                self.canvas.create_text(x + r // 2, y + 2 * r, text='no' if bits.__dict__[f'x{9 - i}'] else 'yes')
            x += pad + r
    
    def diode_clicked(self, diode):
        # Event for changing diode state
        if self.canvas.itemcget(diode, 'fill') == 'green':
            self.canvas.itemconfig(diode, fill='red')
            idx = self.diodes.index(diode)
            self.bits.__dict__[f'x{9 - idx}'] = 1
            self._refresh_number()
            if self.random_bits and self.bits.__dict__ == self.random_bits.__dict__:
                self._end_game()
        else:
            self.canvas.itemconfig(diode, fill='green')
            idx = self.diodes.index(diode)
            self.bits.__dict__[f'x{9 - idx}'] = 0
            self._refresh_number()
            if self.random_bits and self.bits.__dict__ == self.random_bits.__dict__:
                self._end_game()

    def _helper(self, obj):
        return lambda event: self.diode_clicked(obj)

    def _refresh_number(self):
        self.number.canvas.delete('all')
        self.number.digits = self.number.process_number(self.bits)
        self.number.draw_number()

    def _end_game(self):
        for child in ROOT.winfo_children():
            child.destroy()
        win = tk.Label(ROOT, text='You win', fg='green')
        number = tk.Label(ROOT, text='Number is {}'.format(self.number.sum_bits(self.bits)), fg='green')
        win['font'] = font.Font(family='Helvetica', size=30, weight='bold')
        number['font'] = font.Font(family='Helvetica', size=30, weight='bold')
        win.place(x=WIDTH // 2 - 50, y=HEIGHT // 2 - 20)
        number.place(x=WIDTH // 2 - 50, y=HEIGHT // 2 + 20)
        

class Interface:
    # Game interface
    def __init__(self):
        self.one_player = tk.Button(ROOT, text='One player', command=self.one_player_game)
        self.one_player['font'] = font.Font(family='Helvetica', size=30, weight='bold')
        self.two_players = tk.Button(ROOT, text='Two players', command=self.two_players_game)
        self.two_players['font'] = font.Font(family='Helvetica', size=30, weight='bold')
        self.one_player.place(x=0, y=HEIGHT // 2)
        self.two_players.place(x=WIDTH - 180, y=HEIGHT // 2)
        
    def one_player_game(self):
        # Game for one player
        self.one_player.destroy()
        self.two_players.destroy()

        random_number = Bits()
        number = Bits(random=False)

        num = Number(bits=number)
        diodes = Diodes(num, random_number)
        num.draw_number()
        diodes.draw_diodes(one_player=True, bits=random_number)

    def two_players_game(self):
        # Game for two players
        self.one_player.destroy()
        self.two_players.destroy()

        number = Bits(random=False)

        num = Number(number)
        diodes = Diodes(num)
        num.draw_number()
        diodes.draw_diodes()
        

if __name__ == '__main__':
    i = Interface()
    ROOT.mainloop()