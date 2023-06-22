import tkinter as tk
from datetime import datetime


class App:
    def __init__(self, master):
        self.master = master
        self.master.title("IoT Project")
        self.master.geometry("800x900")
        self.counter = 0
        self.max_value = 50
        self.state = False
        self.threshold = 5
        self.events = []

        # Counter Label
        self.counter_label = tk.Label(self.master, text="Counter: {}".format(self.counter), width=120)
        self.counter_label.grid(row=0, column=0, columnspan=2)

        # State Label
        self.state_label = tk.Label(self.master, text="State: {}".format(self.state), bg="green", width=120)
        self.state_label.grid(row=1, column=0, columnspan=2)

        # Button
        self.button = tk.Button(self.master, text="Click me!", command=self.button_click, width=60)
        self.button.grid(row=2, column=0)

        # Entry Field
        self.entry_label = tk.Label(self.master, text="Change threshold value: ", width=60)
        self.entry_label.grid(row=3, column=0)
        self.entry = tk.Entry(self.master, width=60)
        self.entry.insert(0, self.threshold)
        self.entry.grid(row=4, column=0)
        self.entry.bind("<Return>", self.entry_update)

        # Threshold Label
        self.threshold_label = tk.Label(self.master, text="Threshold Value: {}".format(self.threshold), width=120)
        self.threshold_label.grid(row=5, column=0, columnspan=2)

        # Scale Widget
        self.scale_label = tk.Label(self.master, text="Change Counter Value: ", width=120)
        self.scale_label.grid(row=6, column=0, columnspan=2)
        self.scale = tk.Scale(self.master, from_=0, to=self.max_value, orient=tk.HORIZONTAL, length=600)
        self.scale.set(self.counter)
        self.scale.bind("<ButtonRelease-1>", self.scale_update)
        self.scale.grid(row=7, column=0, columnspan=2)

        # Listbox Widget
        self.listbox_label = tk.Label(self.master, text="History of Events: ", width=120)
        self.listbox_label.grid(row=8, column=0, columnspan=2)

        # Scrollbar Widget
        self.scrollbar = tk.Scrollbar(self.master)
        self.scrollbar.grid(row=9, column=1, sticky='ns')

        self.listbox = tk.Listbox(self.master, width=120, yscrollcommand=self.scrollbar.set)  # added yscrollcommand
        self.listbox.grid(row=9, column=0, sticky='nsew')
        self.scrollbar.config(command=self.listbox.yview)

        # to make the scrollbar resize with the window
        self.master.grid_rowconfigure(9, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

    def button_click(self):
        if self.counter < self.max_value:
            self.counter += 1
        else:
            self.listbox_update("Button Click", "Max value reached")
            return
        self.scale.set(self.counter)
        self.events.append(
            "[Button Click on {}: Counter={}: {}]".format(datetime.now().strftime("%H:%M:%S"), self.counter,
                                                          self.threshold))
        self.counter_label.config(text="Counter: {}".format(self.counter))
        self.state = not self.state
        self.state_label.config(text="State: {}".format(self.state))
        if self.counter >= self.threshold:
            self.state_label.config(bg="red")
        else:
            self.state_label.config(bg="green")
        self.listbox_update("Button Click")

    def entry_update(self, _):
        try:
            temp_threshold = int(self.entry.get())
            if temp_threshold > 0 and temp_threshold <= self.max_value:
                self.threshold = temp_threshold
                self.threshold_label.config(text="Threshold Value: {}".format(self.threshold))
                if self.counter >= self.threshold:
                    self.state_label.config(bg="red")
                else:
                    self.state_label.config(bg="green")
                self.events.append("[Threshold Change on {}: Counter={}: {}]".format(datetime.now().strftime("%H:%M:%S"), self.counter, self.threshold))
                self.listbox_update("Threshold Change")
            else:
                self.listbox_update("Threshold Change", "Invalid value. Enter a number between 1 and {}.".format(self.max_value))
        except ValueError:
            self.listbox_update("Threshold Change", "Invalid value. Please enter a number.")

    def scale_update(self, _):
        self.counter = int(self.scale.get())
        self.counter_label.config(text="Counter: {}".format(self.counter))
        self.events.append("[Scale Change on {}: Counter={}: {}]".format(datetime.now().strftime("%H:%M:%S"), self.counter, self.threshold))
        self.listbox_update("Scale Change")
        if self.counter >= self.threshold:
            self.state_label.config(bg="red")
        else:
            self.state_label.config(bg="green")

    def listbox_update(self, widget_name, error_message=None):
        self.listbox.delete(0, tk.END)
        if error_message:
            self.listbox.insert(tk.END, "[Error on {}: {}]".format(widget_name, error_message))
        for event in self.events:
            self.listbox.insert(tk.END, event)


root = tk.Tk()
app = App(root)
root.mainloop()