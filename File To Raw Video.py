import tkinter as tk
from tkinter import filedialog, simpledialog, Menu, messagebox
import subprocess
import os
import threading
from tkinter import ttk

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Convert File To Raw Video")
        self.master.geometry("400x350")
        self.master.resizable(False, False)
        self.pack(padx=20, pady=20)
        self.framerate = "10.766666"
        self.resolution = "426x240"
        self.bitrate = "2.5M"
        self.create_widgets()
        self.create_menu()

    def set_quality(self, resolution, bitrate):
        self.resolution = resolution
        self.bitrate = bitrate

    def start_ffmpeg(self):
        if hasattr(self, 'input_file') and hasattr(self, 'output_dir') and hasattr(self, 'output_file'):
            self.progress_window = tk.Toplevel(self.master)
            self.progress_window.geometry("200x50")
            self.progress_window.resizable(False, False)
            self.progress_bar = ttk.Progressbar(self.progress_window, mode='indeterminate')
            self.progress_bar.pack(expand=True, fill='both', side="top")
            self.progress_bar.start()
            threading.Thread(target=self.run_ffmpeg).start()
        else:
            messagebox.showerror("Error", "Please select both input file and output directory, and enter the output file name.", parent=self.master)

    def create_widgets(self):
        self.select_input = tk.Button(self, height=2, width=30, bg='#9ACD32', activebackground='#006400', font=('Arial', 12))
        self.select_input["text"] = "Select File to convert"
        self.select_input["command"] = self.select_input_file
        self.select_input.pack(side="top", pady=10)

        self.select_output = tk.Button(self, height=2, width=30, bg='#9ACD32', activebackground='#006400', font=('Arial', 12))
        self.select_output["text"] = "Select area to save the video to"
        self.select_output["command"] = self.select_output_dir
        self.select_output.pack(side="top", pady=10)

        self.run_command = tk.Button(self, height=2, width=30, bg='#9ACD32', activebackground='#006400', font=('Arial', 12))
        self.run_command["text"] = "Start"
        self.run_command["command"] = self.start_ffmpeg
        self.run_command.pack(side="top", pady=10)

        self.quit = tk.Button(self, text="QUIT", fg="white", bg="#FF6347", activebackground='#8B0000', height=2, width=30, font=('Arial', 12), command=self.master.destroy)
        self.quit.pack(side="bottom", pady=10)

    def create_menu(self):
        self.menubar = Menu(self.master)
        self.master.config(menu=self.menubar)

        self.optionsmenu = Menu(self.menubar, tearoff=0)
        self.optionsmenu.add_command(label="Change Framerate", command=self.change_framerate)

        # Create a submenu for the video quality
        self.qualitymenu = Menu(self.optionsmenu, tearoff=0)
        self.quality_var = tk.StringVar(value="240p")  # Default resolution
        self.qualitymenu.add_radiobutton(label="144p", variable=self.quality_var, value="144p", command=lambda: self.set_quality("256x144", "1M"))
        self.qualitymenu.add_radiobutton(label="240p", variable=self.quality_var, value="240p", command=lambda: self.set_quality("426x240", "2.5M"))
        self.qualitymenu.add_radiobutton(label="480p", variable=self.quality_var, value="480p", command=lambda: self.set_quality("854x480", "5M"))
        self.qualitymenu.add_radiobutton(label="720p", variable=self.quality_var, value="720p", command=lambda: self.set_quality("1280x720", "7.5M"))
        self.qualitymenu.add_radiobutton(label="1080p", variable=self.quality_var, value="1080p", command=lambda: self.set_quality("1920x1080", "10M"))

        # Add the quality submenu to the options menu
        self.optionsmenu.add_cascade(label="Quality", menu=self.qualitymenu)

        self.menubar.add_cascade(label="Options", menu=self.optionsmenu)

    def select_input_file(self):
        self.input_file = filedialog.askopenfilename()

    def select_output_dir(self):
        self.output_dir = filedialog.askdirectory()
        self.output_file = simpledialog.askstring("Save Video", "Enter the name of the Video (include the extention)", initialvalue="output.mp4", parent=self.master)
        if os.path.exists(self.output_dir + "/" + self.output_file):
            if messagebox.askyesno("File exists", "The file already exists. Do you want to replace it?", parent=self.master):
                os.remove(self.output_dir + "/" + self.output_file)

    def change_framerate(self):
        self.framerate = simpledialog.askstring("Change Framerate", "Enter the new framerate", initialvalue=self.framerate, parent=self.master)

    def run_ffmpeg(self):
        output_file = self.output_dir + "/" + self.output_file
        command = f'ffmpeg -f rawvideo -pixel_format rgb32 -video_size 32x32 -framerate {self.framerate} -i "{self.input_file}" -f u8 -ar 44100 -ac 1 -i "{self.input_file}" -sws_flags neighbor -s {self.resolution} -b:v {self.bitrate} "{output_file}"'
        subprocess.run(command, shell=True)
        os.startfile(self.output_dir)
        self.progress_bar.stop()
        self.progress_window.destroy()

root = tk.Tk()
root.iconbitmap('Icon.ico')
app = Application(master=root)
app.mainloop()
