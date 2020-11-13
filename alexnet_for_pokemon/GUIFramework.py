import tkinter
import tkinter.filedialog
import tkinter.messagebox
from tkinter.ttk import *
from PIL import ImageTk, Image

import os


class MainWindow(tkinter.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.filename = None

        # Menu Bar Creation
        menubar = tkinter.Menu(self.parent)
        self.parent["menu"] = menubar

        # Submenu-1 File Toolsets
        fileMenu = tkinter.Menu(menubar)
        for label, command, shortcut_text, shortcut in (
                ("Import Data File", self.fileOpen, "Ctrl+H", "<Control-h>"),
                ("New Session", self.newSession, "Ctrl+S", "<Control-s>")
            ):
            fileMenu.add_command(label=label, command=command, accelerator=shortcut_text)
        menubar.add_cascade(label="File", menu=fileMenu, underline=0)

        # Main Frame
        frame = tkinter.Frame(self.parent)

        # row 1 - status bar
        self.statusbar = tkinter.Label(frame, text="Ready...", anchor=tkinter.NW)
        self.statusbar.grid(row=0, column=0, columnspan=2, sticky=tkinter.SW)

        # row 2 - button and scroll bar
        loadbutton = tkinter.Button(frame, text="Load File", command=self.fileNew)
        loadbutton.grid(row=1, column=0)

        # row 3 - classify as Pokemon
        pkmbutton = tkinter.Button(frame, text="Classify as Pokemon", command=self.classifyPokemon)
        pkmbutton.grid(row=2, column=0)

        # row 4 - classify as nminst
        nminstbutton = tkinter.Button(frame, text="Classify as Number", command=self.classifyNminst)
        nminstbutton.grid(row=3, column=0)

        scrollbar = tkinter.Scrollbar(frame, orient=tkinter.VERTICAL)
        self.resultbox = tkinter.Listbox(frame, yscrollcommand=scrollbar.set)
        self.resultbox.focus_set()
        self.resultbox.grid(row=1, column=1, rowspan=3, sticky=tkinter.NSEW)
        scrollbar.grid(row=1, column=2, rowspan=3, sticky=tkinter.NS)
        scrollbar["command"] = self.resultbox.yview

        blank = tkinter.Frame(frame)
        copyrightlabel = tkinter.Label(blank, text="Copyright reserved by LI Yuyang", anchor=tkinter.SW)
        copyrightlabel.grid(row=0, column=0, sticky=tkinter.NSEW)
        blank.grid(row=4, column=0, sticky=tkinter.NSEW)

        frame.grid(row=0, column=0, sticky=tkinter.NSEW)

        # WS Setting
        frame.columnconfigure(0, weight=25)
        frame.columnconfigure(1, weight=60)
        frame.columnconfigure(2, weight=10)

        frame.rowconfigure(0, weight=10)
        frame.rowconfigure(1, weight=30)
        frame.rowconfigure(2, weight=30)
        frame.rowconfigure(3, weight=30)
        frame.rowconfigure(4, weight=15)

        window = self.parent.winfo_toplevel()
        window.columnconfigure(0, weight=1)
        window.rowconfigure(0, weight=1)

        self.parent.geometry("{0}x{1}+{2}+{3}".format(600, 200, 0, 50))
        # self.parent.title("Hello")

        self.filelist = {}
        # self.changeStatusBar("Well")

    def fileNew(self):
        self.fileOpen()

    def newSession(self):
        createSession()
        # print("?")

    def clearstatusbar(self):
        self.changeStatusBar("Ready...")

    def changeStatusBar(self, message, timeout=-1):
        self.statusbar["text"] = message
        # clear the status bar after specified timeout
        if timeout > 0:
            self.statusbar.after(timeout, self.clearstatusbar)

    def filedata(self):
        indexes = self.resultbox.curselection()
        if not indexes or len(indexes) > 1:
            tkinter.messagebox.showwarning("File Error", "No file selected. Please import or select any file first.", parent=self.parent)
            return
        index = indexes[0]
        name = self.resultbox.get(index)
        return name

    def classifyPokemon(self):
        dir = self.filelist[self.filedata()]
        classtxt = dir.split("/")[-2]
        print("Expected Class:", classtxt)

        pokemon = ClassifyWindow(parent=self, dir=dir, target=classtxt, module="Pokemon")
        # pokemon.run()

    def classifyNminst(self):
        dir = self.filelist[self.filedata()]

    def fileOpen(self):
        dir = os.path.dirname(self.filename) if self.filename is not None else "."
        filename = tkinter.filedialog.askopenfilename(
            title="New file",
            initialdir=dir,
            filetypes=[("JPG file", "*.jpg")],
            defaultextension=".jpg",
            parent=self.parent
        )
        if filename:
            # print(filename)
            folder = filename.split("/")[-1]
            self.resultbox.insert(tkinter.END, folder)
            self.changeStatusBar("Load file name {0}".format(folder), 1000)
            self.filelist[folder] = filename
            self.filename = filename


class ClassifyWindow(tkinter.Frame):
    def __init__(self, parent, dir, target, module):
        super().__init__()
        self.parent = parent        # this reference is not useful
        self.dir = dir
        self.target = target
        self.module = module

        newwindow = tkinter.Toplevel(self.parent)
        newwindow.title("{0} Classifier".format(self.module))
        # application.mainloop()
        self.parent = newwindow

        frame = tkinter.Frame(self.parent)

        # row 1, 2, 3, 4, 5
        image = Image.open(self.dir)
        image = image.resize((250, 250), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(image)

        image2go = tkinter.Label(frame, image=self.img)
        image2go.grid(row=3, column=0, sticky=tkinter.NSEW)

        target = tkinter.Label(frame, text=self.target)
        target.grid(row=4, column=0, sticky=tkinter.W)

        self.targetImages, self.targetTexts = None  # dummy for classifiers
        for i in range(5):
            pred = tkinter.Label(frame, image=self.targetImages[i])
            pred.grid(row=i, column=1, sticky=tkinter.NSEW)

            classtext = tkinter.Label(frame, text=self.targetTexts[i])
            classtext.grid(row=i, column=2, anchor=tkinter.W)

        frame.grid(row=0, column=0, sticky=tkinter.NSEW)
        frame.columnconfigure(0, weight=300)
        frame.columnconfigure(1, weight=300)
        frame.columnconfigure(2, weight=300)
        frame.rowconfigure(0, weight=300)
        frame.rowconfigure(1, weight=300)
        frame.rowconfigure(2, weight=300)
        frame.rowconfigure(3, weight=300)
        frame.rowconfigure(4, weight=300)
        frame.rowconfigure(5, weight=300)
        newwindow.geometry("{0}x{1}+{2}+{3}".format(1800, 800, 0, 50))


def predict(picturedir, mode=None):
    if mode is None:
        print("No module is loaded, please check.")
    elif mode == "Pokemon":
        print("This is a dummy predict module.")
        return None, None
    elif mode == "Nminst":
        print("This is another dummy predict module.")
        return None, None
    else:
        print("No such module designed in this program.")

def createSession():
    # similar serves as Setup function
    application = tkinter.Tk()
    application.title("COMP7404C Group 2")

    window = MainWindow(application)

    # similar serves as Draw function
    application.mainloop()


if __name__ == "__main__":
    createSession()