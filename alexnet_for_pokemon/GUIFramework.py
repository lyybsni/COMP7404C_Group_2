import os
import tkinter
import tkinter.filedialog
import tkinter.messagebox

import tensorflow as tf
import numpy as np
from PIL import ImageTk, Image

import helper
import validation

dataset_path = '/Users/richardli/Documents/Academia/HKU-2020/COMP7404/Group_Project/dataset'
checkpoint_path = '/Users/richardli/Documents/Academia/HKU-2020/COMP7404/Group_Project/training/cp.ckpt'

class MainWindow(tkinter.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.filename = None

        # Menu Bar Creation
        menubar = tkinter.Menu(self.parent)
        self.parent["menu"] = menubar

        # Submenu-1 File Toolsets
        file_menu = tkinter.Menu(menubar)
        for label, command, shortcut_text, shortcut in (
                ("Import Data File", self.file_open, "Ctrl+H", "<Control-h>"),
                ("New Session", self.new_session, "Ctrl+S", "<Control-s>")
        ):
            file_menu.add_command(label=label, command=command, accelerator=shortcut_text)
        menubar.add_cascade(label="File", menu=file_menu, underline=0)

        # Main Frame
        frame = tkinter.Frame(self.parent)

        # row 1 - status bar
        self.statusbar = tkinter.Label(frame, text="Ready...", anchor=tkinter.NW)
        self.statusbar.grid(row=0, column=0, columnspan=2, sticky=tkinter.SW)

        # row 2 - button and scroll bar
        load_button = tkinter.Button(frame, text="Load File", command=self.file_new)
        load_button.grid(row=1, column=0)

        # row 3 - classify as Pokemon
        pkm_button = tkinter.Button(frame, text="Classify as Pokemon", command=self.classify_pokemon)
        pkm_button.grid(row=2, column=0)

        # row 4 - classify as nminst
        nminst_button = tkinter.Button(frame, text="Classify as Number", command=self.classify_nminst)
        nminst_button.grid(row=3, column=0)

        scrollbar = tkinter.Scrollbar(frame, orient=tkinter.VERTICAL)
        self.result_box = tkinter.Listbox(frame, yscrollcommand=scrollbar.set)
        self.result_box.focus_set()
        self.result_box.grid(row=1, column=1, rowspan=3, sticky=tkinter.NSEW)
        scrollbar.grid(row=1, column=2, rowspan=3, sticky=tkinter.NS)
        scrollbar["command"] = self.result_box.yview

        blank = tkinter.Frame(frame)
        copyright_label = tkinter.Label(blank, text="Copyright reserved by LI Yuyang", anchor=tkinter.SW)
        copyright_label.grid(row=0, column=0, sticky=tkinter.NSEW)
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

        self.file_list = {}
        # self.changeStatusBar("Well")

    def file_new(self):
        self.file_open()

    def new_session(self):
        create_session()
        # print("?")

    def clear_statusbar(self):
        self.change_statusbar("Ready...")

    def change_statusbar(self, message, timeout=-1):
        self.statusbar["text"] = message
        # clear the status bar after specified timeout
        if timeout > 0:
            self.statusbar.after(timeout, self.clear_statusbar)

    def file_data(self):
        indexes = self.result_box.curselection()
        if not indexes or len(indexes) > 1:
            tkinter.messagebox.showwarning("File Error", "No file selected. Please import or select any file first.",
                                           parent=self.parent)
            return
        index = indexes[0]
        name = self.result_box.get(index)
        return name

    def classify_pokemon(self):
        dir_ = self.file_list[self.file_data()]
        class_txt = dir_.split("/")[-2]
        print("Expected Class:", class_txt)

        pokemon = ClassifyWindow(parent=self, dir_=dir_, target=class_txt, module="Pokemon")
        # pokemon.run()

    def classify_nminst(self):
        _dir = self.file_list[self.file_data()]

    def file_open(self):
        dir_ = os.path.dirname(self.filename) if self.filename is not None else "."
        filename = tkinter.filedialog.askopenfilename(
            title="New file",
            initialdir=dir_,
            filetypes=[("JPG file", "*.jpg")],
            defaultextension=".jpg",
            parent=self.parent
        )
        if filename:
            # print(filename)
            folder = filename.split("/")[-1]
            self.result_box.insert(tkinter.END, folder)
            self.change_statusbar("Load file name {0}".format(folder), 1000)
            self.file_list[folder] = filename
            self.filename = filename


class ClassifyWindow(tkinter.Frame):
    def __init__(self, parent, dir_, target, module):
        super().__init__()
        self.parent = parent  # this reference is not useful
        self.dir_ = dir_
        self.target = target
        self.module = module

        new_window = tkinter.Toplevel(self.parent)
        new_window.title("{0} Classifier".format(self.module))
        # application.mainloop()
        self.parent = new_window

        frame = tkinter.Frame(self.parent)

        # row 1, 2, 3, 4, 5
        image = Image.open(self.dir_)
        image = image.resize((250, 250), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(image)

        image2go = tkinter.Label(frame, image=self.img)
        image2go.grid(row=3, column=0, sticky=tkinter.NSEW)

        target = tkinter.Label(frame, text=self.target)
        target.grid(row=4, column=0, sticky=tkinter.W)

        self.targetImages, self.targetTexts = predict(self.dir_, self.module)  # dummy for classifiers

        print(self.targetTexts)
        for i in range(5):
            # pred = tkinter.Label(frame, image=self.targetImages[i])
            # pred.grid(row=i, column=1, sticky=tkinter.NSEW)

            class_text = tkinter.Label(frame, text=self.targetTexts[i])
            class_text.grid(row=i, column=2, sticky=tkinter.W)

        frame.grid(row=0, column=0, sticky=tkinter.NSEW)
        frame.columnconfigure(0, weight=300)
        frame.columnconfigure(1, weight=3000)
        frame.columnconfigure(2, weight=3000)
        frame.rowconfigure(0, weight=300)
        frame.rowconfigure(1, weight=300)
        frame.rowconfigure(2, weight=300)
        frame.rowconfigure(3, weight=300)
        frame.rowconfigure(4, weight=300)
        frame.rowconfigure(5, weight=300)
        new_window.geometry("{0}x{1}+{2}+{3}".format(1800, 800, 0, 50))


def predict(picture_dir, mode=None):
    if mode is None:
        print("No module is loaded, please check.")
    elif mode == "Pokemon":

        model = tf.saved_model.load(checkpoint_path)
        _, _, name2label = helper.load_pokemon(dataset_path, None)

        label2name = {}
        for key in name2label:
            temp = name2label[key]
            label2name[temp] = key

        print(label2name)

        res = validation.predict(picture_dir, model).numpy()[0]

        idx = np.argpartition(res, -5)[-5:]  # Indices not sorted
        lst = idx[np.argsort(res[idx])][::-1]  # Indices sorted by value from largest to smalles

        text = []
        for i in lst:
            text = text + [(label2name[i] + " " + str(res[i]))]
        # print(label2name.get(np.asarray(lst)))
        return None, text
    elif mode == "Nminst":
        print("This is another dummy predict module.")
        return None, None
    else:
        print("No such module designed in this program.")


def create_session():
    # similar serves as Setup function
    application = tkinter.Tk()
    application.title("COMP7404C Group 2")

    window = MainWindow(application)

    # similar serves as Draw function
    application.mainloop()


if __name__ == "__main__":
    create_session()
