import tkinter as tk
from tkinter import filedialog, simpledialog
import subprocess
import os

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Convert File To Raw Video")
        self.master.geometry("400x300")
        self.pack(padx=20, pady=20)
        self.create_widgets()

    def create_widgets(self):
        self.select_input = tk.Button(self, height=2, width=30, bg='light blue', font=('Arial', 12))
        self.select_input["text"] = "Select File to convert"
        self.select_input["command"] = self.select_input_file
        self.select_input.pack(side="top", pady=10)

        self.select_output = tk.Button(self, height=2, width=30, bg='light blue', font=('Arial', 12))
        self.select_output["text"] = "Select area to save the video to"
        self.select_output["command"] = self.select_output_dir
        self.select_output.pack(side="top", pady=10)

        self.run_command = tk.Button(self, height=2, width=30, bg='light blue', font=('Arial', 12))
        self.run_command["text"] = "Start"
        self.run_command["command"] = self.run_ffmpeg
        self.run_command.pack(side="top", pady=10)

        self.quit = tk.Button(self, text="QUIT", fg="white", bg="red", height=2, width=30, font=('Arial', 12), command=self.master.destroy)
        self.quit.pack(side="bottom", pady=10)

    def select_input_file(self):
        self.input_file = filedialog.askopenfilename()

    def select_output_dir(self):
        self.output_dir = filedialog.askdirectory()
        self.output_file = simpledialog.askstring("Save Video", "Enter the name of the Video (include the extention)", initialvalue="output.mp4")

    def run_ffmpeg(self):
        if hasattr(self, 'input_file') and hasattr(self, 'output_dir') and hasattr(self, 'output_file'):
            output_file = self.output_dir + "/" + self.output_file
            command = f'ffmpeg -f rawvideo -pixel_format rgb32 -video_size 32x32 -framerate 10.766666 -i "{self.input_file}" -f u8 -ar 44100 -ac 1 -i "{self.input_file}" -sws_flags neighbor -s 240x240 "{output_file}"'
            subprocess.run(command, shell=True)
            os.startfile(self.output_dir)  # Open the directory after ffmpeg is done
        else:
            print("Please select both input file and output directory, and enter the output file name.")

root = tk.Tk()
root.iconbitmap('Icon.ico')
app = Application(master=root)
app.mainloop()
