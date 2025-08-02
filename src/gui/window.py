from tkinter import Label, Button

class Window:
    def __init__(self, master):
        self.master = master
        master.title("Auto Clicker")

        self.label = Label(master, text="Auto Clicker Tool")
        self.label.pack()

        self.start_button = Button(master, text="Start", command=self.start_clicking)
        self.start_button.pack()

        self.stop_button = Button(master, text="Stop", command=self.stop_clicking)
        self.stop_button.pack()

        self.is_clicking = False

    def start_clicking(self):
        self.is_clicking = True
        self.label.config(text="Clicking...")

    def stop_clicking(self):
        self.is_clicking = False
        self.label.config(text="Stopped")