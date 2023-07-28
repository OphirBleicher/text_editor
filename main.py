from tkinter import *
from tkinter.messagebox import askyesno, askyesnocancel, showerror, WARNING, showinfo
from tkinter.colorchooser import askcolor
from tkinter.simpledialog import askstring, askinteger as askint
from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog import askopenfilename as openfile, asksaveasfilename as savefile
from platform import system
from matplotlib import pyplot as plt
from os import startfile
if system() == "Windows":
    from ctypes import windll
    windll.user32.ShowWindow(windll.kernel32.GetConsoleWindow(), 0)
try:
    f = open("data.txt")
except FileNotFoundError:
    f = open("data.txt", 'w')
    f.write("Courier New\n10\n#000000\n#ffffff\nutf-8")
    f.close()
    f = open("data.txt")
font_properties = f.readlines()
f.close()
font = font_properties[0].strip()
font_size = font_properties[1].strip()
font_color = font_properties[2].strip()
bg_color = font_properties[3].strip()
encoding = font_properties[4].strip()
file_opened = None
is_file_saved = True
now_text = ""
indent = ""


def save_as():
    global file_opened, is_file_saved
    f = savefile(defaultextension=".txt")
    if f is None or f == '':
        return
    f = open(f, "w", encoding=encoding)
    text_to_save = str(txt.get("1.0", END))
    f.write(text_to_save)
    file_opened = f"{f.name}"
    root.title(f"Text Editor - {file_opened}")
    f.close()
    is_file_saved = True
    statusbar.config(text="")


def save_file():
    global file_opened, is_file_saved
    if file_opened is None or file_opened == "":
        save_as()
    else:
        with open(file_opened, 'w', encoding=encoding) as f:
            f.write(txt.get("1.0", END))
    is_file_saved = True
    statusbar.config(text="")


def open_file():
    global file_opened, is_file_saved
    file_opened = openfile(title="Open")
    if file_opened is None or file_opened == "":
        return
    with open(file_opened, encoding=encoding) as f:
        txt.delete("0.0", "end-1c")
        txt.insert("0.0", f.read())
        root.title(f"Text Editor - {file_opened}")
    is_file_saved = True
    statusbar.config(text="")


def new_file():
    global file_opened, is_file_saved
    file_opened = None
    root.title("Text editor")
    txt.delete("1.0", END)
    statusbar.config(text="")
    is_file_saved = True


def change_font():
    global font, file_opened
    new_font = askstring("Font", "What's the new font?")
    if new_font is None:
        return
    if askyesno("Question", "Do you want to determine the font " + new_font + " to default?"):
        with open("data.txt", "w") as f:
            f.write(new_font + "\n" + str(font_size) + "\n" + font_color + "\n" + bg_color + '\n' + encoding)

    txt.config(font=(new_font, font_size))
    font = new_font


def change_font_size():
    global font_size
    new_size = askint("Font", "What's the new font size?")
    if new_size is None:
        return
    if askyesno("Question", f"Do you want to make font size {new_size} to default?"):
        with open("data.txt", "w") as f:
            f.write(font + "\n" + str(new_size) + "\n" + font_color + "\n" + bg_color + "\n" + encoding)
    txt.config(font=(font, new_size))
    font_size = new_size


def change_color():
    global font_color
    new_color = askcolor(title="Color")[1]
    if new_color is None:
        return
    if askyesno("Question", f"Do you want to make font color {new_color} to default?"):
        with open("data.txt", 'w') as f:
            f.write(font + "\n" + str(font_size) + "\n" + new_color + "\n" + bg_color + "\n" + encoding)
    txt.config(fg=new_color)
    font_color = new_color


def change_bgcolor():
    global bg_color
    new_color = askcolor(title="Color")[1]
    if new_color is None:
        return
    if askyesno("Question", f"Do you want to make font color {new_color} to default?"):
        with open("data.txt", 'w') as f:
            f.write(font + "\n" + str(font_size) + "\n" + font_color + "\n" + new_color + "\n" + encoding)
    txt.config(bg=new_color)
    bg_color = new_color


def change_encoding():
    global encoding
    new_encoding = askstring("", "What's the encoding?")
    if new_encoding is None or new_encoding == "":
        return
    if askyesno("Question", f"Do you want to make encoding {new_encoding} to default?"):
        with open("data.txt", 'w') as f:
            f.write(font + "\n" + str(font_size) + "\n" + font_color + "\n" + bg_color + "\n" + new_encoding)
    encoding = new_encoding
    save_file()
    with open(file_opened, encoding=encoding) as f:
        txt.delete("0.0", "end-1c")
        txt.insert("0.0", f.read())


def back_default():
    global font, font_size, font_color, bg_color
    with open("data.txt", "w") as f:
        f.write("Courier New\n10\n#000000\nwhite")
    txt.config(font=("Courier New", 10), fg="#000000", bg="white")
    font_color = "#000000"
    font = "Courier New"
    font_size = 10
    bg_color = "#ffffff"


def text_changed():
    global is_file_saved, now_text
    if now_text != txt.get("1.0", END).strip("\n"):
        is_file_saved = False
        statusbar.config(text="Changes not saved")
        now_text = txt.get("1.0", END)


def display_as_graph():
    try:
        function = txt.get("1.0", END).strip("y").strip().strip("=").strip()
        x_values = range(-100, 101)
        y_values = []
        for x in x_values:
            try:
                y = eval(function)
                y_values.append(y)
            except ZeroDivisionError:
                y_values.append(None)
                showerror(message=f"Undefined for x = {x}")
        plt.plot(x_values, y_values, color=askstring("", "Color of the line"))
        plt.show()
    except Exception as e:
        showerror(message=e)


def exit_from_root():
    if not is_file_saved:
        answer = askyesnocancel("Question", "Changes Not Saved.\nDo You want to save changes?", icon="warning")
        if answer:
            save_file()
            root.destroy()
        elif answer is False:
            root.destroy()
    else:
        root.destroy()


def on_return(event):
    current_line = txt.get('insert linestart', 'insert lineend')
    indent = current_line[:len(current_line) - len(current_line.lstrip())]
    txt.insert('insert', '\n' + indent)
    return 'break'


def on_backspace(event):
    current_line = txt.get("insert linestart", "insert lineend")
    if current_line.strip() == '':
        if len(current_line) > 0:
            txt.delete("insert -1c")
            return "break"


def open_in_app():
    startfile(file_opened)


def show_encoding():
    showinfo(message="The current encoding is %s" % encoding)


def main():
    global is_file_saved, txt, root, statusbar, encoding
    root = Tk()
    root.title("Text Editor")
    root.geometry("500x500")
    root.iconbitmap("icon.ico")
    root.bind("<Key>", lambda x: text_changed())
    root.bind("<F5>", lambda x: open_in_app())
    root.protocol("WM_DELETE_WINDOW", exit_from_root)
    statusbar = Label(root, text="", bd=1, relief="sunken", anchor="w")
    statusbar.pack(side=BOTTOM, fill="x")
    txt = ScrolledText(root, width=500, height=500, font=(font, font_size) or ("Courier New", font_size), fg=font_color,
                       bg=bg_color)
    txt.pack()
    txt.bind("<Return>", on_return)
    txt.bind("<BackSpace>", on_backspace)
    menubar = Menu(root)
    filemenu = Menu(menubar, tearoff=0)
    fontmenu = Menu(menubar, tearoff=0)
    viewmenu = Menu(menubar, tearoff=0)
    mathmenu = Menu(menubar, tearoff=0)
    funcmenu = Menu(mathmenu, tearoff=0)
    encodemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Open", command=open_file)
    filemenu.add_command(label="Save", command=save_file)
    filemenu.add_command(label="Save As", command=save_as)
    filemenu.add_command(label="New", command=new_file)
    fontmenu.add_command(label="Change Font", command=change_font)
    fontmenu.add_command(label="Change Font Size", command=change_font_size)
    fontmenu.add_command(label="Change Font Color", command=change_color)
    fontmenu.add_command(label="Change Background Color", command=change_bgcolor)
    fontmenu.add_command(label="Return To Default", command=back_default)
    viewmenu.add_command(label="Open in default app", command=open_in_app)
    funcmenu.add_command(label="Display As Function Graph", command=display_as_graph)
    encodemenu.add_command(label="Show Encoding", command=show_encoding)
    encodemenu.add_command(label="Change Encoding", command=change_encoding)
    mathmenu.add_cascade(label="Functions", menu=funcmenu)
    menubar.add_cascade(label="File", menu=filemenu)
    menubar.add_cascade(label="Font", menu=fontmenu)
    menubar.add_cascade(label="View", menu=viewmenu)
    menubar.add_cascade(label="Math", menu=mathmenu)
    menubar.add_cascade(label="Encoding", menu=encodemenu)
    menubar.add_command(label="Quit", command=exit_from_root)
    root.config(menu=menubar)
    show_encoding()
    root.mainloop()


if __name__ == "__main__":
    main()
