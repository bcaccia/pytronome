import tkinter as tk
from tkinter import ttk
import time
import numpy as np
import sounddevice as sd
import multiprocessing as mp

class Pytronome:
    def __init__(self, root):
        # Set up the root window        
        self.root = root
        self.root.title("Pytronome")
        self.root.geometry("300x250")
        self.root.resizable(False, False)
        self.start_stop_state = tk.IntVar()
        self.start_stop_state.set(0)
        self.bpm = tk.IntVar(value=120)
        self.seconds_per_beat = 0.5
        self.tap_tempo_taps = []

        # Create top frame
        self.top_frame = tk.Frame(self.root, bg="black", height=150)
        self.top_frame.pack(fill=tk.BOTH, expand=True)

        # BPM label and widget
        self.label_bpm = tk.Label(self.top_frame, text="BPM", font=("Helvetica", 16), fg="white", bg="black")
        self.label_bpm.pack(pady=10)

        self.spinbox_bpm = tk.Spinbox(self.top_frame, from_=30, to=300, width=5, textvariable=self.bpm, command=self.update_bpm)
        # Handle the user pressing Enter or Keypad Enter on manual number entry
        self.spinbox_bpm.bind("<KeyRelease>", self.update_bpm)
        self.spinbox_bpm.pack(pady=10)

        # Time signature label
        self.label_time_signature = tk.Label(self.top_frame, text="Time Signature", font=("Helvetica", 16), fg="white", bg="black")
        self.label_time_signature.pack(pady=10)
        
        # Frame for timesig_1 and timesig_2
        self.timesig_frame = tk.Frame(self.top_frame, bg="black")
        self.timesig_frame.pack()

        # Combobox for timesig_1
        self.timesig1_values = list(range(1, 17))
        self.timesig_1 = ttk.Combobox(self.timesig_frame, values=self.timesig1_values, state="readonly", width=4)
        self.timesig_1.set(1)
        self.timesig_1.pack(side=tk.LEFT, padx=5)

        # Combobox for timesig_2
        self.timesig2_values = [1, 2, 4, 8]
        self.timesig_2 = ttk.Combobox(self.timesig_frame, values=self.timesig2_values, state="readonly", width=4)
        self.timesig_2.set(4)
        self.timesig_2.pack(side=tk.LEFT, padx=5)

        self.button_frame = tk.Frame(self.top_frame, bg="black")
        self.button_frame.pack(pady=10)

        self.tap_button = tk.Button(self.button_frame, text="Tap (t)", command=self.tap_button_clicked)
        root.bind(("t"), self.tap_button_clicked)
        self.start_button = tk.Button(self.button_frame, text="Start (spc)", command=self.toggle_start_stop_state)
        root.bind("<space>", self.toggle_start_stop_state)
        self.tap_button.pack(side=tk.LEFT, padx=5)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
    def update_bpm(self, *args):
        try:
            self.calc_bpm_to_ms()
        except ValueError:
            print("Invalid BPM value")
            pass
        
    def calc_bpm_to_ms(self):
        milliseconds_per_beat = 60000 / int(self.bpm.get())
        self.seconds_per_beat = milliseconds_per_beat / 1000
        print(f'Seconds per beat: {self.seconds_per_beat}')

    def tap_button_clicked(self, *args):
        # At least 4 taps are required by the user to
        # calculate a new BPM value
        self.tap_tempo_taps.append(time.time())
        # Check if it has been more than 3 secs since last tap
        # If so, reset the tap tempo list
        if (self.tap_tempo_taps[-1] - self.tap_tempo_taps[0]) < 3:
            if len(self.tap_tempo_taps) == 4:
                # Calculate the diff in seconds between the first and second
                # and third and fourth taps, then average between them
                tap_diff1 = self.tap_tempo_taps[1] - self.tap_tempo_taps[0]
                tap_diff2 = self.tap_tempo_taps[3] - self.tap_tempo_taps[2]
                tap_average = (tap_diff1 + tap_diff2) / 2
                self.tap_tempo_taps = []
                # Round tap times to the 2nd decimal place, no need for
                # greater accuracy
                self.seconds_per_beat = round(tap_average, 2)
                # Do the math to convert from ms to BPM
                new_bpm = 60000 / (self.seconds_per_beat * 1000)
                self.bpm.set(round(new_bpm))
                print(tap_average)
                print(round(new_bpm))
        else:
            self.tap_tempo_taps = []
            print("Taps reset")
    
    def toggle_start_stop_state(self, *args):
        current_state = self.start_stop_state.get()
        # Toggle the state
        self.start_stop_state.set(1 - current_state)
        if self.start_stop_state.get() == 1:
            self.start_button.config(text="Stop (spc)")
            self.click_process = mp.Process(target=self.play_click)
            self.click_process.start()
        else:
            self.start_button.config(text="Start (spc)")
            self.start_stop_state.set(0)
            self.click_process.terminate()
            self.click_process.join()
        print(self.start_stop_state.get())
        
    def play_click(self):
        while self.start_stop_state.get():
            for beat in range(int(self.timesig_1.get())):
                start = time.time()
                print(f'beat: {beat + 1}')
                # Check if the value is larger than 1 and if so play the
                # accent on the first beat
                if beat == 0 and int(self.timesig_1.get()) > 1:
                    self.play_beep(beep_frequency=1000)
                else:
                    self.play_beep(beep_frequency=500)
                # Subtract 0.01 due to  slowness in the sounddevice play() call
                time.sleep(self.seconds_per_beat - 0.01)
                end = time.time()
                print(end - start)
               
    def generate_sine_wave(self, duration, frequency, sampling_rate):
        t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
        sine_wave = 0.5 * np.sin(2 * np.pi * frequency * t)
        return sine_wave
    
    def play_beep(self, beep_duration=0.05, beep_frequency=500, sampling_rate=44100):
        beep_signal = self.generate_sine_wave(beep_duration, beep_frequency, sampling_rate)
        sd.play(beep_signal, samplerate=sampling_rate)
        
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