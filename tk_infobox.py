__author__ = 'tremity'

from tkinter import *

#class InfoBox():
#    def __init__(self, master, text, width=250, height=250):
class InfoBox(Frame):
    def __init__(self, master, *args, **kw):

        text=""
        if "text" in kw:
            text = kw["text"]
            del kw["text"]

        Frame.__init__(self, master, *args, **kw)

        self.vartext = None
        if isinstance(text, StringVar):
            self.vartext = text
            self.vartext.trace("w", lambda  name, index, mode: self._vartext_update())
            text = self.vartext.get()

        #self.container = Frame(master, width=width, height=height)

        self.scrollbar = Scrollbar(self)
        self.scrollbar.grid(row=0, column=1, sticky=N+S)

        self.text_widget = Text(self, width=10, height=10, wrap=WORD, yscrollcommand=self.scrollbar.set, cursor="arrow")

        self.set_text(text)
        self.text_widget.grid(row=0, column=0, sticky=N+S+W+E)
        self.grid_propagate(False)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.scrollbar.config(command=self.text_widget.yview)


    def set_text(self, text):
        self.text_widget.config(state=NORMAL)
        self.text_widget.delete(1.0, END)
        self.text_widget.insert(INSERT, text)
        self.text_widget.config(state=DISABLED)

    def _vartext_update(self):
        self.set_text(self.vartext.get())

#FUNZIONANTE!!!
# class InfoBox():
#     def __init__(self, master, text, width=25, height=10):
# # class InfoBox():
# #     def __init__(self, master, *args, **kw):
# #         Frame.__init__(self, master, *args, **kw)
#
#         self.scrollbar = Scrollbar(master)
#         self.scrollbar.grid(row=0, column=1, sticky=N+S)
#
#         self.text_widget = Text(master, width=width, height=height, wrap=WORD, yscrollcommand=self.scrollbar.set, cursor="arrow")
#         self.set_text(text)
#         self.text_widget.grid(row=0, column=0, sticky=N+S+W+E)
#         master.columnconfigure(0, weight=1)
#         master.rowconfigure(0, weight=1)
#
#         self.scrollbar.config(command=self.text_widget.yview)
#
#
#     def set_text(self, text):
#         self.text_widget.config(state=NORMAL)
#         self.text_widget.delete(1.0, END)
#         self.text_widget.insert(INSERT, text)
#         self.text_widget.config(state=DISABLED)