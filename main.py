import tkinter as tk
import tkinter.simpledialog
import datetime
import requests
import json
import os
import subprocess
import base64

_AOC_TOKEN=None

def aoc_token():
    global _AOC_TOKEN
    if _AOC_TOKEN:
        return _AOC_TOKEN
    else:
        _AOC_TOKEN = tkinter.simpledialog.askstring("AoC Token","Advent of Code Token")
        return _AOC_TOKEN

_PROBLEMS_DIR = None

def problems_dir():
    global _PROBLEMS_DIR
    if _PROBLEMS_DIR:
        return _PROBLEMS_DIR
    else:
        _PROBLEMS_DIR = tkinter.simpledialog.askstring("Problems Directory","Problems Directory")
        return _PROBLEMS_DIR

def current_time():
    return datetime.datetime.utcnow()-datetime.timedelta(hours=5)#+datetime.timedelta(days=50)

win = tk.Tk()
win.title("AoC CI")
win.geometry("1000x650")
win.resizable(0, 0)

win.rowconfigure(1,weight=3)
##win.columnconfigure(1,weight=1)
##win.columnconfigure(2,weight=1)

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
year_list_selection = None
def year_select_action(event):
    global year_list_selection
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        data = event.widget.get(index)
##        print(data)
        day_list_widget.delete(0,tk.END)
        for day in range(len(day_list[int(data)])):
            day_list_widget.insert(day,str(day_list[int(data)][day]))
##        day_list_widget.select_set(0)
        saveall()
        sample_input.delete(1.0,tk.END)
        sample_output.delete(1.0,tk.END)
        year_list_selection = data
        openall()
    else:
        print("none selected")
day_list_selection = None
def day_select_action(event):
    global day_list_selection
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        data = event.widget.get(index)
##        print(data)
        saveall()
        sample_input.delete(1.0,tk.END)
        sample_output.delete(1.0,tk.END)
        day_list_selection = data
        openall()
    else:
        print("none selected")
year_list_widget.bind('<<ListboxSelect>>', year_select_action)

day_list_widget.bind('<<ListboxSelect>>', day_select_action)

year_list_widget.grid(column=0,row=0)
day_list_widget.grid(column=0,row=1,stick="nesw")

sample_input_frame = tk.Frame(win)
sample_input_frame.grid(column=1,row=0,rowspan=2)

sample_input_label = tk.Label(sample_input_frame, text="Sample Input")
sample_input_label.pack()
sample_input = tk.Text(sample_input_frame,height=12,width=40)
sample_input.pack()

sample_input_label = tk.Label(sample_input_frame, text="Sample Output")
sample_input_label.pack()
sample_output = tk.Text(sample_input_frame,height=12,width=40)
sample_output.pack()

code_output_frame = tk.Frame(win)
code_output_frame.grid(column=2,row=0,rowspan=2)

code_output_label = tk.Label(code_output_frame, text="Code Output")
code_output_label.pack()
code_output_display = tk.Text(code_output_frame,height=12,width=40)
code_output_display.pack()
code_output_display.config(state=tk.DISABLED)

code_answer_label = tk.Label(code_output_frame, text="Code Answer")
code_answer_label.pack()
code_answer_display = tk.Text(code_output_frame,height=12,width=40)
code_answer_display.pack()
code_answer_display.config(state=tk.DISABLED)
def run_code_sample():
    saveall()
    if day_list_selection and year_list_selection:
        problem_file_path=os.path.join(problems_dir(),year_list_selection,day_list_selection)
        if not os.path.exists(problem_file_path):
            os.makedirs(problem_file_path, exist_ok=True)
        if not os.path.exists(os.path.join(problem_file_path,"problem_io.py")):
            with open(os.path.join(problem_file_path,"problem_io.py"), "w+") as create_problem_io:
                create_problem_io.write("import sys\nimport base64\nclass IO:\n    @property\n    def input(self):\n        return base64.b64decode(sys.argv[1].encode()).decode()\n    def output(self,output):\n        print('__AOC_CI_SYSTEM_OUTPUT_CALL:'+base64.b64encode(str(output).encode()).decode())\nio = IO()\n")
        if not os.path.exists(os.path.join(problem_file_path,"solution.py")):
            with open(os.path.join(problem_file_path,"solution.py"), "w+") as create_main_py:
                create_main_py.write("from problem_io import io\n\nprint('solution.py Exists!')")
        sample_input_data = sample_input.get(1.0,tk.END)
        result = subprocess.run(
            [
                'py',
                os.path.join(
                    problem_file_path,
                    os.path.join(problem_file_path,"solution.py")
                ),
                base64.b64encode(sample_input_data.encode()).decode()
            ],
            stdout=subprocess.PIPE,
            cwd=problem_file_path
        )
        try:
            code_output = result.stdout.decode()
        except:
            print("Failure")
            code_output = ''
        code_answer = ''
        for line in code_output.split("\n"):
            if line.startswith("__AOC_CI_SYSTEM_OUTPUT_CALL:"):
                try:
                    code_answer = base64.b64decode(code_output[28:].encode()).decode()
                except:
                    code_answer = ''
        print(code_output)
        code_output_display.config(state=tk.NORMAL)
        code_output_display.delete(1.0,tk.END)
        code_output_display.insert(0.0,code_output)
        code_output_display.config(state=tk.DISABLED)

        code_answer_display.config(state=tk.NORMAL)
        code_answer_display.delete(1.0,tk.END)
        code_answer_display.insert(0.0,code_answer)
        code_answer_display.config(state=tk.DISABLED)
##    os.system("py ")
    
def run_code_real_input():
    pass
run_code_sample_button = tk.Button(code_output_frame, text="Run Code/Sample", command = run_code_sample)
run_code_sample_button.pack()
run_code_real_input_button = tk.Button(code_output_frame, text="Run Code/Real Input", command = run_code_real_input)
run_code_real_input_button.pack()

def openall():
    if day_list_selection and year_list_selection:
        problem_config_file_path=os.path.join(problems_dir(),year_list_selection,day_list_selection)
        problem_config_file_name="_data.json"
        if os.path.exists(os.path.join(problem_config_file_path,problem_config_file_name)):
            with open(os.path.join(problem_config_file_path,problem_config_file_name)) as problem_config_file:
                problem_config = json.loads(problem_config_file.read())
            sample_input_data = problem_config["sample_input"]
            sample_output_data = problem_config["sample_output"]
            sample_input.delete(1.0,tk.END)
            sample_output.delete(1.0,tk.END)
            sample_input.insert(0.0,sample_input_data)
            sample_output.insert(0.0,sample_output_data)

def saveall():
    if day_list_selection and year_list_selection:
        sample_input_data = sample_input.get(1.0,tk.END)
        sample_output_data = sample_output.get(1.0,tk.END)
        if sample_input_data.strip("\n") or sample_output_data.strip("\n"):
            problem_config = {
                "sample_input":sample_input_data,
                "sample_output":sample_output_data,
                }
            
            problem_config_file_path=os.path.join(problems_dir(),year_list_selection,day_list_selection)
            problem_config_file_name="_data.json"
            if not os.path.exists(problem_config_file_path):
                os.makedirs(problem_config_file_path, exist_ok=True)
            with open(os.path.join(problem_config_file_path,problem_config_file_name),"w+") as problem_config_file:
                problem_config_file.write(json.dumps(problem_config))

def on_closing():
    saveall()
    win.destroy()

win.protocol("WM_DELETE_WINDOW", on_closing)

win.mainloop()
