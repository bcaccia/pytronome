import tkinter as tk
from tkinter import ttk
import time
import multiprocessing as mp
from pydub import AudioSegment
from pydub.playback import play

class Pytronome:
    def __init__(self, root):
        # Set up the root window        
        self.root = root
        self.root.title("Pytronome")
        self.root.geometry("450x450")
        self.root.resizable(False, False)
        self.click_file = AudioSegment.from_wav("sounds/MetroBar1.wav")
        self.start_stop_state = tk.IntVar()
        self.start_stop_state.set(0)

        # Create top frame
        self.top_frame = tk.Frame(self.root, bg="black", height=150)
        self.top_frame.pack(fill=tk.BOTH, expand=True)

        # Widgets in the top frame
        self.label_bpm = tk.Label(self.top_frame, text="BPM", font=("Helvetica", 16), fg="white", bg="black")
        self.label_bpm.pack(pady=10)

        self.spinbox_bpm = tk.Spinbox(self.top_frame, from_=30, to=300, width=5)
        self.spinbox_bpm.pack(pady=10)

        self.label_time_signature = tk.Label(self.top_frame, text="Time Signature", font=("Helvetica", 16), fg="white", bg="black")
        self.label_time_signature.pack(pady=10)
        
        # Frame for timesig_1 and timesig_2
        self.timesig_frame = tk.Frame(self.top_frame, bg="black")
        self.timesig_frame.pack()

        # Spinnerbox for timesig_1
        self.timesig_1 = tk.Spinbox(self.timesig_frame, from_=1, to=12, width=2)
        self.timesig_1.pack(side=tk.LEFT, padx=5)

        # Spinnerbox for timesig_2
        self.timesig_2 = tk.Spinbox(self.timesig_frame, from_=1, to=12, width=2)
        self.timesig_2.pack(side=tk.LEFT, padx=5)
        
        self.label_time_division = tk.Label(self.top_frame, text="Time Division", font=("Helvetica", 16), fg="white", bg="black")
        self.label_time_division.pack(pady=10)

        # Combo box for Time Division
        time_division_options = ["1/1", "1/2", "1/4", "1/8", "1/16", "1/32"]
        self.combo_time_division = ttk.Combobox(self.top_frame, values=time_division_options)
        self.combo_time_division.set("1/4")  # Set default value to 1/4
        self.combo_time_division.bind("<<ComboboxSelected>>", self.get_selected_time_division)
        self.combo_time_division.pack(pady=10)

        self.button_frame = tk.Frame(self.top_frame, bg="black")
        self.button_frame.pack(pady=10)

        self.tap_button = tk.Button(self.button_frame, text="Tap", command=self.tap_button_clicked)
        self.start_button = tk.Button(self.button_frame, text="Start", command=self.toggle_start_stop_state)
        self.tap_button.pack(side=tk.LEFT, padx=5)
        self.start_button.pack(side=tk.LEFT, padx=5)

        # Create bottom frame
        self.bottom_frame = tk.Frame(self.root, bg="blue", height=150)
        self.bottom_frame.pack(fill=tk.BOTH, expand=True)

        # Widget in the bottom frame
        self.label_count = tk.Label(self.bottom_frame, text="1", font=("Helvetica", 48), fg="white", bg="blue")
        self.label_count.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
    def get_selected_time_division():
        # Handle combobox time division selection
        pass

    def tap_button_clicked(self):
        # Handle tap button click
        pass
    
    def toggle_start_stop_state(self):
        current_state = self.start_stop_state.get()
        # Toggle the state
        self.start_stop_state.set(1 - current_state)
        if self.start_stop_state.get() == 1:
            self.start_button.config(text="Stop")
            self.click_process = mp.Process(target=self.play_click_values)
            self.click_process.start()
        else:
            self.start_button.config(text="Start")
            self.start_stop_state.set(0)
            self.click_process.terminate()
            self.click_process.join()
        print(self.start_stop_state.get())
        
    def play_click_values(self):
        while self.start_stop_state.get():
            play(self.click_file)
        
# Required when spawning multiple processes
if __name__ == '__main__':    

    # Create the root window
    root = tk.Tk()

    # Create an instance of the Pytronome class
    app = Pytronome(root)

    # Run the application UI
    root.mainloop()

"""
To calculate BPM use the equation bpm = 60000 / milliseconds per beat
To calculate milliseconds per beat use the formula mpb = 60000 / bpm
"""