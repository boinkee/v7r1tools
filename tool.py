""" json,commands,gui and file picky """
import json
import subprocess as sb
import tkinter as tk
from tkinter.filedialog import askopenfilename

DATA_FILE = "data.json"
com = 0

# def print_to_label(text_string):
    # label_text.set(label_text.get() + '\n' + text_string)
    # root.update()
def extract():
    """ firmware extract (using subprocess and tkinter)"""
    if var.get() == 4:
        sb.run(['del', "0*.bin"], check=False, shell=True)
        return
    f = askopenfilename()
    if not f:
        tk.messagebox.showerror(title="Error", message="Please select a file")
        return
    if var.get() == 1:
        out = sb.run(['balongflash', '-e', f"{f}"], check=False, capture_output=True, text=True)
        showoutput(out.stdout)
    elif var.get() == 2:
        out = sb.run(['balongflash', '-s', f"{f}"], check=False, capture_output=True, text=True)
        showoutput(out.stdout)
    elif var.get() == 3:
        out = sb.run(['balongflash.exe', '-m', f"{f}"], check=False, capture_output=True, text=True)
        showoutput(out.stdout)

def reset():
    """ reset modem (using subprocess module)"""
    out = sb.run(['balongflash.exe', f'-p{com}', '-r'], check=False, capture_output=True, text=True)
    showoutput(out.stdout)

def loadd():
    """ load comport (using json module)"""
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("com", "")
    except FileNotFoundError:
        print("file not found")
        return FileNotFoundError
    except json.JSONDecodeError:
        print("json file is corrupt")
        return json.JSONDecodeError

def save():
    """ save comport (using json module)"""
    inputty = entry_box.get()
    data = {"com": inputty}

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    root.destroy()

def limit_input(p):
    """ input limiter to 3 chars """
    return len(p) <= 3

def reload():
    """ (re)load comport (used pylint comment bcs im lazy)"""
    # pylint: disable=global-statement
    global com
    com = entry_box.get()
    print(f"new comport:{com}")

def showoutput(text_string):
    """show output of a command in a different window. (uses tkinter module)"""
    output_window = None
    label_text = ""
    output_window = tk.Toplevel()
    output_window.withdraw()
    output_window.wm_title("Output")
    output_window.minsize(width=400, height=600)
    output_window.maxsize(width=1000, height=1000)
    label_text = tk.StringVar()
    out_label = tk.Label(output_window,textvariable=label_text, wraplength=350)
    label_text.set('')
    out_label.pack()
    label_text.set(label_text.get() + '\n' + text_string)
    output_window.deiconify()
    output_window.update()

root = tk.Tk()
root.wm_title("Balong V7R1 toolsa")
root.minsize(width=300, height=350)
root.maxsize(width=600, height=700)
vcmd = root.register(limit_input)
var = tk.IntVar()
var.set(1)

flashtext = tk.Label(root, text="V7R1 tools")
flashtext.pack()
flashtext.config(width=15, height=1)

flashtext = tk.Label(root, text="COM port: (only number)")
flashtext.pack()
flashtext.config(width=15, height=1)

entry_box = tk.Entry(root, width=30, validate="key", validatecommand=(vcmd, "%p"))
entry_box.pack(pady=20)
reload = tk.Button(root, text="Reload", command=reload)
reload.pack()
reset = tk.Button(root, text="Reboot the modem", command=reset)
reset.pack()
reset.config(width=15, height=1)

load = tk.Button(root, text="Load USBLoader")
load.pack()
load.config(width=15, height=1)

flash = tk.Button(root, text="Flash from directory")
flash.pack()
flash.config(width=15, height=1)

extracter = tk.Button(root, text="Start", command=extract)
extracter.pack()
extracter.config(width=15, height=1)

r1 = tk.Radiobutton(root, text='Extract with headers (.fw)', variable=var, value=2)
r1.pack()
r2 = tk.Radiobutton(root, text='Extract without headers (.bin)', variable=var, value=1)
r2.pack()
r3 = tk.Radiobutton(root, text='List firmware integrity', variable=var, value=3)
r3.pack()
r4 = tk.Radiobutton(root, text='Clean files', variable=var, value=4)
r4.pack()

# label_text = tk.StringVar()
# out_label = tk.Label(textvariable=label_text, wraplength=350)
# label_text.set('Output')
# out_label.pack()

com = loadd()
entry_box.insert(0, com)
print(f"com port:{com}")

root.protocol("WM_DELETE_WINDOW", save)

root.mainloop()
