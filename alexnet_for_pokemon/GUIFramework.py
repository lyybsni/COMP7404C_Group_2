import tkinter
import tkinter.filedialog
import os


class MainWindow(tkinter.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # Menu Bar Creation
        menubar = tkinter.Menu(self.parent)
        self.parent["menu"] = menubar

        self.filename = None

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

        self.statusbar = tkinter.Label(frame, text="Ready...", anchor=tkinter.W)
        self.statusbar.grid(row=0, column=0, columnspan=2, sticky=tkinter.SW)

        scrollbar = tkinter.Scrollbar(frame, orient=tkinter.VERTICAL)
        scrollbar.grid(row=1, column=1, sticky=tkinter.NS)

        frame.grid(row=0, column=0, sticky=tkinter.NSEW)

        # WS Setting
        frame.columnconfigure(0, weight=999)
        frame.columnconfigure(1, weight=20)
        frame.rowconfigure(0, weight=10)
        frame.rowconfigure(1, weight=290)

        window = self.parent.winfo_toplevel()
        window.columnconfigure(0, weight=1)
        window.rowconfigure(0, weight=1)

        self.parent.geometry("{0}x{1}+{2}+{3}".format(400, 500, 0, 50))
        self.parent.title("Hello")

        # self.changeStatusBar("Well")

    def fileNew(self):
        print("Hello!")

    def newSession(self):
        createSession()
        # print("?")

    def changeStatusBar(self, message):
        self.statusbar["text"] = message

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
            print(filename)


def createSession():
    # similar serves as Setup function
    application = tkinter.Tk()
    application.title("COMP7404C Group 2")

    window = MainWindow(application)

    # similar serves as Draw function
    application.mainloop()


if __name__ == "__main__":
    createSession()