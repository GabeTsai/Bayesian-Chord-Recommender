import tkinter as tk
from tkinter import ttk
from Chord import ChordEncoder
from Model import BayesianModel

import tkinter as tk
from tkinter import ttk
# Assuming ChordEncoder and BayesianModel are defined and implemented correctly
from Chord import ChordEncoder
from Model import BayesianModel

class ChordProgressionGUI:
    def __init__(self, master):
        self.master = master
        master.title("Chord Progression Generator")

        self.model = BayesianModel()
        # Assuming the model has been previously trained and saved, and there's a method to load it.
        self.model.loadModel('bayesianChordNetwork.pkl')

        # Variables to hold user selections
        self.key_type_var = tk.StringVar()
        self.key_choice_var = tk.StringVar()
        self.musical_style_var = tk.StringVar()
        self.roman_numeral_var = tk.StringVar()
        self.recommended_chords_var = tk.StringVar()

        # UI Components
        tk.Label(master, text="Choose Key Type:").pack()
        key_type_dropdown = ttk.Combobox(master, textvariable=self.key_type_var, state="readonly", values=["major", "minor"])
        key_type_dropdown.pack()
        key_type_dropdown.bind("<<ComboboxSelected>>", self.update_key_choices)

        tk.Label(master, text="Choose Key:").pack()
        self.key_choice_dropdown = ttk.Combobox(master, textvariable=self.key_choice_var, state="readonly")
        self.key_choice_dropdown.pack()

        tk.Label(master, text="Choose Musical Style:").pack()
        ttk.Combobox(master, textvariable=self.musical_style_var, state="readonly", values=["pop", "classical"]).pack()

        tk.Label(master, text="Choose Starting Chord's Roman Numeral:").pack()
        ttk.Combobox(master, textvariable=self.roman_numeral_var, state="readonly", values=["I", "II", "III", "IV", "V", "VI", "VII"]).pack()

        tk.Button(master, text="Get Recommendations", command=self.get_recommendations).pack()

        tk.Label(master, text="Recommended Chords:").pack()
        self.recommended_chords_dropdown = ttk.Combobox(master, textvariable=self.recommended_chords_var, state="readonly")
        self.recommended_chords_dropdown.pack()

        tk.Button(master, text="Add Selected Chord to Progression", command=self.add_chord_to_progression).pack()

        self.chord_progression_label = tk.Label(master, text="Your chord progression:")
        self.chord_progression_label.pack()
        self.chord_progression_text = tk.Text(master, height=10, width=50)
        self.chord_progression_text.pack()

        tk.Button(master, text="Quit", command=master.quit).pack()

    def update_key_choices(self, event=None):
        major_keys = ['C', 'G', 'D', 'A', 'E', 'B', 'F#', 'C#', 'F', 'Bb', 'Eb', 'Ab', 'Db', 'Gb', 'Cb']
        minor_keys = ['A', 'E', 'B', 'F#', 'C#', 'G#', 'D#', 'A#', 'D', 'G', 'C', 'F', 'Bb', 'Eb', 'Ab']
        self.key_choice_dropdown['values'] = major_keys if self.key_type_var.get() == "major" else minor_keys
        self.key_choice_dropdown.set('')  # Clear the current selection

    def get_recommendations(self):
        current_roman_numeral = self.roman_numeral_var.get()
        key = self.key_choice_var.get()
        key_type = self.key_type_var.get()
        root = ChordEncoder(key, 'M' if key_type == "major" else 'm')
        if not current_roman_numeral:
            tk.messagebox.showinfo("Error", "Please select a starting chord's Roman numeral.")
            return
        recNote, quality = root.getRomanNumeral(current_roman_numeral)
        self.chord_progression_text.insert(tk.END, f"{current_roman_numeral}: {recNote}{quality} ")
        self.process_recommendations(current_roman_numeral)

    def add_chord_to_progression(self):
        selected_chord = self.recommended_chords_var.get()
        print(selected_chord)
        if not selected_chord:
            tk.messagebox.showinfo("Error", "Please select a chord from the recommendations.")
            return
        self.chord_progression_text.insert(tk.END, f"{selected_chord} ")

        # Automatically fetch new recommendations based on the selected chord
        selected_roman_numeral = selected_chord.split(": ")[0]  # Extract the Roman numeral from the selected chord
        self.roman_numeral_var.set(selected_roman_numeral)
        self.process_recommendations(selected_roman_numeral)

    def process_recommendations(self, current_roman_numeral):
        key = self.key_choice_var.get()
        key_type = self.key_type_var.get()
        musical_style = self.musical_style_var.get()

        if not all([key, key_type, musical_style, current_roman_numeral]):
            tk.messagebox.showinfo("Error", "Please make sure all fields are filled out.")
            return

        # Assuming the model's recommendChords method returns a list of Roman numeral recommendations
        roman_numeral_recs = self.model.recommendChords(current_roman_numeral, key_type, musical_style)
        recommendations = []

        for rec_roman_numeral in roman_numeral_recs:
            chord_encoder = ChordEncoder(key, 'M' if key_type == "major" else 'm')
            recNote, quality = chord_encoder.getRomanNumeral(rec_roman_numeral)
            recommendations.append(f"{rec_roman_numeral}: {recNote}{quality}")

        self.recommended_chords_dropdown['values'] = recommendations
        if recommendations:
            self.recommended_chords_dropdown.set(recommendations[0])  # Pre-select the first recommendation


def main():
    root = tk.Tk()
    my_gui = ChordProgressionGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()