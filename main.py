#!/usr/bin/env python3#!/usr/bin/env python3

import tkinter as tk
from tkinter import HORIZONTAL, LEFT, TOP

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


class About(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent, class_=parent.name)
        self.config()

        btn = tk.Button(self, text="Konec", command=self.close)
        btn.pack()

    def close(self):
        self.destroy()


class Application(tk.Tk):
    """name = basename(splitext(basename(__file__.capitalize()))[0])"""
    name = "Foo"

    def __init__(self):
        super().__init__(className=self.name)
        self.title(self.name)
        self.bind("<Escape>", self.quit)
        self.lblMain = tk.Label(self, text="Color Mishmash")
        self.btnQuit= tk.Button(self, text="Quit", command=self.quit)
        self.frameR = tk.Frame(master=self)
        self.frameG = tk.Frame(self)
        self.frameB = tk.Frame(self)
        self.frameMem=tk.Frame(self)
        
        self.lblR = tk.Label(self.frameR, text="R", width=2)
        self.lblG = tk.Label(self.frameG, text="G", width=2)
        self.lblB = tk.Label(self.frameB, text="B", width=2)
        
        self.varR=tk.IntVar()
        self.varR.trace_add("write", self.updateColor)

        self.varG=tk.IntVar()
        self.varG.trace_add("write", self.updateColor)

        self.varB=tk.IntVar()
        self.varB.trace_add("write", self.updateColor)

        self.scaleR = tk.Scale(self.frameR, from_=0, to=255, orient=HORIZONTAL, length=300, command=self.updateColor, variable=self.varR)
        self.scaleG = tk.Scale(self.frameG, from_=0, to=255, orient=HORIZONTAL, length=300, command=self.updateColor, variable=self.varG)
        self.scaleB = tk.Scale(self.frameB, from_=0, to=255, orient=HORIZONTAL, length=300, command=self.updateColor, variable=self.varB)
        
        self.entryR = tk.Entry(self.frameR, textvariable=self.varR, width=3)
        self.entryG = tk.Entry(self.frameG, textvariable=self.varG, width=3)
        self.entryB = tk.Entry(self.frameB, textvariable=self.varB, width=3)

        self.canvas = tk.Canvas(self, background="#FF5588")
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

        self.canvaslist=[]
        for row in range(0,3):
            for col in range(0,7):
                canvas = tk.Canvas(master=self.frameMem, width=50, height=50,background="#12abc3")
                canvas.bind("<Button-1>", self.clickHandler)
                canvas.grid(row=row, column=col)
                self.canvaslist.append(canvas)

        self.btnQuit.pack()
        self.colorLoad()

    def clickHandler(self, event):
        if self.cget("cursor") != "pencil":
            self.config(cursor="pencil")
            self.copycolor=event.widget.cget("background")
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
            event.widget.config(background=self.copycolor)

    def updateColor(self, event=None):
        r = self.scaleR.get()
        g = self.scaleG.get()
        b = self.scaleB.get()
        self.canvas.config(background=f"#{r:02X}{g:02X}{b:02X}")

    def colorSave(self):
        with open("colors.txt", "w") as f:
            f.write(self.canvas.cget("background")+"\n")
            for c in self.canvaslist:
                f.write(c.cget("background")+"\n")

    def colorLoad(self):
        pass

    def quit(self, event=None):
        self.colorSave()
        super().quit()


app = Application()
app.mainloop()

