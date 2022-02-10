import tkinter as tk
import time
import threading  # because we don't want the same thread that will be responsible for running the GUI to run the time
import random


class TypeSpeedGUI:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Typing Speed Application')
        self.root.geometry('800x600')

        self.texts = open('texts.txt', 'r').read().split('\n')

        self.frame = tk.Frame(self.root)  # A frame in Tk lets you organize & group widgets. It works like a container.
        # It's a rectangular area in which widgets can be placed.

        self.sample_label = tk.Label(self.frame, text=random.choice(self.texts), font=("Helvetica", 18))
        self.sample_label.grid(row=0, column=0, columnspan=2, padx=5, pady=10)

        self.input_entry = tk.Entry(self.frame, width=50, font=("Helvetica", 24))
        self.input_entry.grid(row=1, column=0, columnspan=2, padx=5, pady=10)
        self.input_entry.bind("<KeyPress>", self.start)
        # The binding function is used to deal with the events. We can bind Python’s Functions and methods to an event
        # as well as we can bind these functions to any particular widget.

        self.speed_label = tk.Label(self.frame, text="Speed: \n0 CPS\n0 CPM\n0 WPS\n0 WPM", font=("Helvetica", 18))
        self.speed_label.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

        self.reset_button = tk.Button(self.frame, text="Reset", command=self.reset, font=("Helvetica", 24))
        self.reset_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

        self.frame.pack(expand=True)

        self.counter = 0
        self.running = False

        self.root.mainloop()

    def start(self, event):
        if not self.running:
            if not event.keycode in [16, 17, 18]:  # 16-shift, 17-ctrl, 18-alt.
                self.running = True
                t = threading.Thread(target=self.time_thread)
                t.start()

        # to check if the words match
        # cget Method to Get text Option Value of Tkinter Label
        if not self.sample_label.cget('text').startswith(self.input_entry.get()):
            self.input_entry.config(fg="red")
        else:
            self.input_entry.config(fg="black")

        if self.input_entry.get() == self.sample_label.cget('text')[:-1]:  # it seems to add a space so we're removing
            self.running = False
            self.input_entry.config(fg="green")

    def time_thread(self):  # the task of timing should be run in a second thread
        while self.running:
            time.sleep(0.1)  # Python time sleep function is used to add delay in the execution of a program.
            # We can use python sleep function to halt the execution of the program for given time in seconds.
            self.counter += 0.1
            cps = len(self.input_entry.get()) / self.counter
            cpm = cps * 60
            wps = len(self.input_entry.get().split(" ")) / self.counter
            wpm = wps * 60
            self.speed_label.config(text=f"Speed: \n{cps:.0f} CPS\n{cpm:.0f} CPM\n{wps:.0f} WPS\n{wpm:.0f} WPM")
            # config is used to access an object's attributes after its initialisation.

    def reset(self):
        self.running = False
        self.counter = 0
        self.speed_label.config(text="Speed: \n0 CPS\n0 CPM\n0 WPS\n0 WPM")
        self.sample_label.config(text=random.choice(self.texts))
        self.input_entry.delete(0, tk.END)  # tk.END is like the ending positon, so it deletes from 0 to end


TypeSpeedGUI()