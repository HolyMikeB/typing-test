from tkinter import *
from tkinter import messagebox
import math
from collections import Counter
from sentences import paragraphs
import random
from difflib import SequenceMatcher


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


timer = None
typing = False
current_sentence = ''


# function to start timer and get new paragraph
def start_timer():
    global typing
    global current_sentence
    typing = True
    current_sentence = random.choice(paragraphs)
    sample_sentence.config(text=current_sentence)
    count_up(0)


# controls the timer and gets results
def count_up(count):
    global timer
    global typing
    global current_sentence
    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f'0{count_sec}'
    if count_min < 10:
        count_min = f'0{count_min}'

    canvas.itemconfig(timer_text, text=f'{count_min}:{count_sec}')
    if typing:
        timer = window.after(1000, count_up, count + 1)
    else:
        minutes = count / 60
        typed_text = typing_input.get(1.0, 'end-1c')
        typed_words = typed_text.split()
        word_count = len(Counter(typed_words))
        wpm = round(word_count / minutes, 2)

        accuracy = similar(current_sentence, typed_text) * 100

        messagebox.showinfo(title='Results', message=f'Your words per minute was {wpm} with an accuracy of {accuracy}%.'
                                                     f' Press start to try another test.')


# stops timer so results can be calculated
def submit():
    global typing
    typing = False


window = Tk()
window.title('Typing Test')
window.config(padx=100, pady=50, width=800, height=800)

canvas = Canvas(width=306, height=458)
keyboard = PhotoImage(file='header.png')
canvas.create_image(158, 158, image=keyboard)
timer_text = canvas.create_text(158, 382, text='00:00', fill='black', font=('Courier', 35, 'bold'))
canvas.grid(column=0, columnspan=2, row=0)

sample_sentence = Label(text='Press start to begin.', font=('Courier', 15), wraplength=400, justify='left', padx=10)
sample_sentence.grid(column=0, row=1)

typing_input = Text(window, height=18, width=35, font=('Courier', 15))
typing_input.grid(column=1, row=1)

start_button = Button(text='Start', command=start_timer)
start_button.grid(column=0, row=3)

submit_button = Button(text='Submit', command=submit)
submit_button.grid(column=1, row=3)

window.mainloop()
