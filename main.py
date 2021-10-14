import tkinter as tk
import datetime

def current_time():
    return datetime.datetime.utcnow()-datetime.timedelta(hours=5)

win = tk.Tk()
win.title("AoC CI")

year_list = tk.Listbox(win)
year_list.insert(1,"2015")

year_list.pack()
win.mainloop()
