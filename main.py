#!/usr/bin/env python3

import tkinter as tk
from tkinter import HORIZONTAL, TOP, LEFT
from os.path import exists
from datetime import datetime


# from tkinter import ttk


class MyEntry(tk.Entry):
    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)

        if "textvariable" not in kw:
            self.variable = tk.StringVar()
            self.config(textvariable=self.variable)
        else:
            self.variable = kw["textvariable"]

    @property
    def value(self):
        return self.variable.get()

    @value.setter
    def value(self, new: str):
        self.variable.set(new)


class Application(tk.Tk):
    name = "Foo"

    def __init__(self):
        super().__init__(className=self.name)
        self.title(self.name)
        self.bind("<Escape>", self.destroy)
        self.lblMain = tk.Label(self, text="Color Mishmash", font="Terminus 22", fg="#12abc3")
        self.lblMain.bind("<Button-1>", self.timestringHandler)
        self.btnQuit = tk.Button(self, text="Quit", command=self.quit)
        self.frameR = tk.Frame(master=self)
        self.frameG = tk.Frame(self)
        self.frameB = tk.Frame(self)
        self.frameMem = tk.Frame(self)

        self.lblR = tk.Label(self.frameR, text="R", width=2)
        self.lblG = tk.Label(self.frameG, text="G", width=2)
        self.lblB = tk.Label(self.frameB, text="B", width=2)

        self.varR = tk.IntVar()
        self.varR.trace_add("write", self.updateColor)
        self.scaleR = tk.Scale(
            self.frameR,
            from_=0,
            to=255,
            orient=HORIZONTAL,
            length=300,
            variable=self.varR,
        )
        self.entryR = tk.Entry(self.frameR, textvariable=self.varR, width=3)

        self.varG = tk.IntVar()
        self.varG.trace_add("write", self.updateColor)
        self.scaleG = tk.Scale(
            self.frameG,
            from_=0,
            to=255,
            orient=HORIZONTAL,
            length=300,
            variable=self.varG,
        )
        self.entryG = tk.Entry(self.frameG, textvariable=self.varG, width=3)

        self.varB = tk.IntVar()
        self.varB.trace_add("write", self.updateColor)
        self.scaleB = tk.Scale(
            self.frameB,
            from_=0,
            to=255,
            orient=HORIZONTAL,
            length=300,
            variable=self.varB,
        )
        self.entryB = tk.Entry(self.frameB, textvariable=self.varB, width=3)

        self.canvas = tk.Canvas(self, background="#FF5588", width=30)
        self.canvas.bind("<Button-1>", self.clickHandler)

        self.lblMain.pack(side=TOP)
        self.frameR.pack(side=TOP)
        self.frameG.pack(side=TOP)
        self.frameB.pack(side=TOP)

        self.lblR.pack(side=LEFT, anchor="s")
        self.scaleR.pack(side=LEFT, anchor="s")
        self.entryR.pack(side=LEFT, anchor="s")

        self.lblG.pack(side=LEFT, anchor="s")
        self.scaleG.pack(side=LEFT, anchor="s")
        self.entryG.pack(side=LEFT, anchor="s")

        self.lblB.pack(side=LEFT, anchor="s")
        self.scaleB.pack(side=LEFT, anchor="s")
        self.entryB.pack(side=LEFT, anchor="s")

        self.canvas.pack(side=TOP, fill="both")
        self.frameMem.pack(side=TOP, fill="both")

        self.canvaslist = []
        for row in range(3):
            for col in range(7):
                canvas = tk.Canvas(self.frameMem, width=50, height=50, bg="#12abc3")
                canvas.bind("<Button-1>", self.clickHandler)
                canvas.grid(row=row, column=col)
                self.canvaslist.append(canvas)

        self.btnQuit.pack()
        self.colorLoad()
        # self.protocol("WM_DELETE_WINDOW", self.colorSave)
        self.timestring()

    def clickHandler(self, event):
        if self.cget("cursor") != "pencil":
            self.config(cursor="pencil")
            self.copycolor = event.widget.cget("background")
        else:
            self.config(cursor="")
            if event.widget is self.canvas:
                r = int(self.copycolor[1:3], 16)
                g = int(self.copycolor[3:5], 16)
                b = int(self.copycolor[5:], 16)
                self.varR.set(r)
                self.varG.set(g)
                self.varB.set(b)
            else:
                event.widget.config(background=self.copycolor)

    def updateColor(self, newvalue=None, neco=None, dalsi=None):
        r = self.scaleR.get()
        g = self.scaleG.get()
        b = self.scaleB.get()
        self.canvas.config(background=f"#{r:02X}{g:02X}{b:02X}")
        self.lblMain.config(foreground=f"#{r:02X}{g:02X}{b:02X}")

    def colorSave(self):
        with open("colors.txt", "w") as f:
            f.write(self.canvas.cget("background") + "\n")
            for c in self.canvaslist:
                f.write(c.cget("background") + "\n")

    def colorLoad(self):
        if not exists("colors.txt"):
            return
        with open("colors.txt", "r") as f:
            try:
                color = f.readline().strip()
                r = int(color[1:3], 16)
                g = int(color[3:5], 16)
                b = int(color[5:], 16)
                self.varR.set(r)
                self.varG.set(g)
                self.varB.set(b)
                for canvas in self.canvaslist:
                    canvas.config(background=f.readline().strip())
            except (ValueError, tk.TclError):
                pass

    def timestring(self):
        current_time = datetime.now()
        string = current_time.strftime("%y-%m-%d %H:%M:%S")
        self.lblMain.configure(text=string)
        self.timestring_id = self.after(1000, self.timestring)

    def timestringHandler(self, event):
        if self.timestring_id:
            self.after_cancel(self.timestring_id)
            self.timestring_id=None
        else:
            self.timestring()

    def destroy(self, event=None):
        self.colorSave()
        super().destroy()


app = Application()
app.mainloop()

