
# class LoadingBar:
#     def __init__(self) -> None:
#         self.root = tkinter.Tk()
#         self.root.config(bg = "black")
#         self.root.title("Custom Loading Bar")
#         self.root.attributes("-fullscreen", True)

#         # Loading text:
#         tkinter.Label(master = self.root, text = "Loading...", font = "Bahnschrift 15", bg = "black",
#             fg = "#FFBD09"
#         ).place(x = 490, y = 320)

#         # Loading blocks:
#         for i in range(16):
#             tkinter.Label(master = self.root, bg = "#1F2732", width = 2, height = 1).place(x = (i+22)*22, y = 350)
        
#         # update root to see animation
#         self.root.update()
        
#         self.playAnimation()
    
#     # Loader animation:
#     def playAnimation(self):
#         for _ in range(200):
#             for j in range(16):

#                 # make block yellow:
#                 tkinter.Label(master = self.root, bg = "#FFBD09", width = 2, height = 1).place(x = (j+22)*22, y = 350)
#                 time.sleep(0.06)
#                 self.root.update_idletasks()

#                 # make block dark
#                 tkinter.Label(master = self.root, bg = "#1F2732", width = 2, height = 1).place(x = (j+22)*22, y = 350)
#         else:
#             self.root.destroy()
#             exit(0)

# if __name__=="__main__":
#     LoadingBar()

import tkinter as tk
from tkinter import ttk
import threading
import queue
import time


class App(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.queue = queue.Queue()
        self.listbox = tk.Listbox(self, width=20, height=5)
        self.progressbar = ttk.Progressbar(self, orient='horizontal',
                                           length=300, mode='determinate')
        self.button = tk.Button(self, text="Start", command=self.spawnthread)
        self.listbox.pack(padx=10, pady=10)
        self.progressbar.pack(padx=10, pady=10)
        self.button.pack(padx=10, pady=10)

    def spawnthread(self):
        self.button.config(state="disabled")
        self.thread = ThreadedClient(self.queue)
        self.thread.start()
        self.periodiccall()

    def periodiccall(self):
        self.checkqueue()
        if self.thread.is_alive():
            self.after(100, self.periodiccall)
        else:
            self.button.config(state="active")

    def checkqueue(self):
        while self.queue.qsize():
            try:
                msg = self.queue.get(0)
                self.listbox.insert('end', msg)
                self.progressbar.step(25)
            except queue.Empty:
                pass


class ThreadedClient(threading.Thread):

    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        for x in range(1, 5):
            time.sleep(2)
            msg = "Function %s finished..." % x
            self.queue.put(msg)


if __name__ == "__main__":
    app = App()
    app.mainloop()