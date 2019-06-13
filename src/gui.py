from tkinter import *
import PIL.Image, PIL.ImageTk
import subprocess
import os
import cv2
from main import GestureHandler


class App:
    def __del__(self):
        self.gesture_handler.cap.release()

    def __init__(self):
        self.root = Tk()
        self.root.title("Gesture recognizer")

        self.vid = None
        self.canvas = None

        self.mainframe = Frame(self.root)
        self.mainframe.bind("<Key>", self.inkey)
        self.mainframe.focus_set()
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S), padx=10, pady=10)
        self.mainframe.columnconfigure(10, weight=1)
        self.mainframe.rowconfigure(10, weight=1)
        self.all_cameras = None

        process = subprocess.Popen('ls /dev/video*', shell=True, stdout=subprocess.PIPE)
        process.wait()
        if process.returncode is not 0:
            print("Cannot get any cam devices")
            exit(1)
        else:
            output = os.popen('ls /dev/video*').read()
            self.all_cameras = list(map(lambda x: x[-1], output.splitlines()))

        self.current_option = StringVar(self.root)
        self.current_option.set(self.all_cameras[2])
        self.popup_menu = OptionMenu(self.mainframe, self.current_option, *self.all_cameras)

        Label(self.mainframe, text="Choose a camera").grid(row=0, column=10, sticky=E)
        self.gesture_text = StringVar("")
        self.gesture_message = Label(self.mainframe, textvariable=self.gesture_text).grid(row=0, column=10, sticky=W)
        self.popup_menu.grid(row=1, column=10, sticky=E)

        def on_change(*args):
            nonlocal self
            self.prepare_window()

        self.current_option.trace('w', on_change)

        self.gesture_handler = GestureHandler(int(self.current_option.get()))
        self.vid = self.gesture_handler.cap
        self.camera_output = self.canvas = Canvas(self.mainframe, width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH),
                                                  height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.camera_output.grid(row=2, column=10)

        self.update()
        self.root.mainloop()

    def prepare_window(self):
        self.gesture_handler.cap.release()
        self.gesture_handler = GestureHandler(int(self.current_option.get()))
        self.vid = self.gesture_handler.cap
        self.camera_output = self.canvas = Canvas(self.mainframe, width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH),
                                                  height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.camera_output.grid(row=2, column=10)


    def update(self):
        ret, msg = self.gesture_handler.update()
        if ret is not None:
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(ret))
            self.canvas.create_image(0, 0, image=self.photo, anchor=NW)
            self.mainframe.update_idletasks()
        if msg is not None:
            self.gesture_text.set(msg)
        # else:
        #     self.gesture_text.set("")
        self.mainframe.update()
        self.root.after(15, self.update)

    def inkey(self, e):
        if e.char == 'q':
            exit(0)
        if e.char == ' ':
            print("\n\n\n")
            for i in self.gesture_handler.get_contour():
                print(i)
        if e.char == 'r':
            self.gesture_handler.reset_history()

App()
