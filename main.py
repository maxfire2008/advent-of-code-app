import tkinter as tk
import datetime

def current_time():
    return datetime.datetime.utcnow()-datetime.timedelta(hours=5)#+datetime.timedelta(days=50)

win = tk.Tk()
win.title("AoC CI")
win.geometry("200x650")
win.resizable(0, 0)

year_list_widget = tk.Listbox(win, exportselection=False)
day_list_widget = tk.Listbox(win, exportselection=False)

year_list = []
day_list = {}

for year_to_add in range(2015,current_time().year+int(current_time().month/12)):
    year_list.append(year_to_add)
    day_list[year_to_add] = []
    for day in range(max(25*int(current_time().year>year_to_add),current_time().day*int(current_time().month/12))):
        day_list[year_to_add].append(day+1)
for year_to_add in range(len(year_list)):
    year_list_widget.insert(year_to_add+1,str(year_list[year_to_add]))
print(day_list)
def year_select_action(event):
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        data = event.widget.get(index)
        print(data)
        day_list_widget.delete(0,tk.END)
        for day in range(len(day_list[int(data)])):
            day_list_widget.insert(day,str(day_list[int(data)][day]))
##        day_list_widget.select_set(0)
    else:
        print("none selected")
def day_select_action(event):
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        data = event.widget.get(index)
        print(data)
    else:
        print("none selected")
year_list_widget.bind('<<ListboxSelect>>', year_select_action)

day_list_widget.bind('<<ListboxSelect>>', day_select_action)

year_list_widget.grid(column=0,row=0)
day_list_widget.grid(column=0,row=1, columnspan=2)

##year_list_widget.select_set(tk.END)
##year_list_widget.event_generate("<<ListboxSelect>>")

win.mainloop()
