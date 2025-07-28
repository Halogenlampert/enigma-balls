import tkinter as tk
from tkinter import ttk, messagebox
from enigma.RotorFactory import RotorFactory
from enigma.UmkehrwalzeFactory import UmkehrwalzeFactory
from enigma.Plugboard import Plugboard
from enigma.EnigmaMachine import EnigmaMachine
import random
import json
import pyperclip

class EnigmaGUI:
    def __init__(self, root):
        self.root = root
        root.title("Enigma Machine Simulator")

        self.available_rotors = RotorFactory.list_available()
        self.reflectors = UmkehrwalzeFactory.list_available()
        self.plug_pairs = []

        self._build_widgets()
        self._create_machine()

    def _build_widgets(self):
        # Rotor Selection
        frame = ttk.LabelFrame(self.root, text="Walzenkonfiguration")
        frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.rotor_vars = []
        self.position_vars = []
        self.ring_vars = []

        for i in range(3):
            rotor_var = tk.StringVar(value=self.available_rotors[i])
            position_var = tk.IntVar(value=0)
            ring_var = tk.IntVar(value=0)

            ttk.Label(frame, text=f"Rotor {i+1}").grid(row=0, column=i)
            ttk.Combobox(frame, textvariable=rotor_var, values=self.available_rotors).grid(row=1, column=i)
            ttk.Spinbox(frame, from_=0, to=25, textvariable=position_var, width=5).grid(row=2, column=i)
            ttk.Spinbox(frame, from_=0, to=25, textvariable=ring_var, width=5).grid(row=3, column=i)
            ttk.Label(frame, text="Position").grid(row=4, column=i)
            ttk.Label(frame, text="Ring").grid(row=5, column=i)

            self.rotor_vars.append(rotor_var)
            self.position_vars.append(position_var)
            self.ring_vars.append(ring_var)

        # Reflector
        self.reflector_var = tk.StringVar(value=self.reflectors[0])
        ttk.Label(self.root, text="Umkehrwalze").grid(row=1, column=0, sticky="w", padx=10)
        ttk.Combobox(self.root, textvariable=self.reflector_var, values=self.reflectors).grid(row=1, column=0)

        # Plugboard config
        plug_frame = ttk.LabelFrame(self.root, text="Steckerbrett (z.B. AB CD)")
        plug_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.plug_entry = ttk.Entry(plug_frame)
        self.plug_entry.grid(row=0, column=0, padx=5)

        # Message I/O
        io_frame = ttk.Frame(self.root)
        io_frame.grid(row=3, column=0, padx=10, pady=10)

        self.input_field = tk.Text(io_frame, height=5, width=50)
        self.input_field.grid(row=0, column=0)
        self.input_field.bind("<KeyRelease>", self._on_key_release)

        self.output_field = tk.Text(io_frame, height=5, width=50, state="disabled")
        self.output_field.grid(row=1, column=0)
        
        
        button_frame = ttk.Frame(self.root)
        button_frame.grid(row=4, column=0, pady=10)
        # buttons
        ttk.Button(self.root, text="Randomize Settings", command=self._randomize_settings).grid(row=0, column=1, padx=5)
        ttk.Button(self.root, text="Export Settings", command=self._copy_settings).grid(row=1, column=1, padx=5)
        ttk.Button(self.root, text="Import Settings", command=self._paste_settings).grid(row=2, column=1, padx=5)


    def _create_machine(self):
        try:
            rotors = [
                RotorFactory.create(self.rotor_vars[2].get(), self.position_vars[2].get(), self.ring_vars[2].get()),
                RotorFactory.create(self.rotor_vars[1].get(), self.position_vars[1].get(), self.ring_vars[1].get()),
                RotorFactory.create(self.rotor_vars[0].get(), self.position_vars[0].get(), self.ring_vars[0].get())
            ]
            reflector = UmkehrwalzeFactory.create(self.reflector_var.get())

            plug_text = self.plug_entry.get().upper().strip()
            plugs = []
            if plug_text:
                parts = plug_text.split()
                for p in parts:
                    if len(p) != 2:
                        raise ValueError(f"Invalid plug pair: {p}")
                    plugs.append((p[0], p[1]))

            plugboard = Plugboard(plugs)
            self.machine = EnigmaMachine(rotors[0], rotors[1], rotors[2], reflector, plugboard)
            self.output_field.config(state="normal")
            self.output_field.delete("1.0", "end")
            self.output_field.config(state="disabled")

        except Exception as e:
            messagebox.showerror("Setup Error", str(e))

    def _on_key_release(self, event):
        text = self.input_field.get("1.0", "end").strip().upper()
        self._create_machine()  # Reset machine each time to keep consistent output
        try:
            output = self.machine.encode(text)
            self.output_field.config(state="normal")
            self.output_field.delete("1.0", "end")
            self.output_field.insert("1.0", output)
            self.output_field.config(state="disabled")
        except ValueError as e:
            self.output_field.config(state="normal")
            self.output_field.delete("1.0", "end")
            self.output_field.insert("1.0", f"[ERROR] {e}")
            self.output_field.config(state="disabled")
            
    def _randomize_settings(self):
        rotors = random.sample(self.available_rotors, 3)
        for i in range(3):
            self.rotor_vars[i].set(rotors[i])
            self.position_vars[i].set(random.randint(0, 25))
            self.ring_vars[i].set(random.randint(0, 25))

        self.reflector_var.set(random.choice(self.reflectors))
        
        # Generate random plugboard pairs
        alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        random.shuffle(alphabet)
        plug_pairs = [alphabet[i:i+2] for i in range(0, 20, 2)]  # Up to 10 pairs
        formatted_pairs = [f"{a}{b}" for a, b in plug_pairs if len(a) == 1 and len(b) == 1]
        self.plug_entry.delete(0, "end")
        self.plug_entry.insert(0, " ".join(formatted_pairs))
        
        self._create_machine()
        
    def _copy_settings(self):
        config = {
            "rotors": [var.get() for var in self.rotor_vars],
            "positions": [var.get() for var in self.position_vars],
            "rings": [var.get() for var in self.ring_vars],
            "reflector": self.reflector_var.get(),
            "plugboard": self.plug_entry.get().strip().upper()
        }
        pyperclip.copy(json.dumps(config))
        messagebox.showinfo("Copied", "Settings copied to clipboard!")

    def _paste_settings(self):
        try:
            config = json.loads(pyperclip.paste())
            for i in range(3):
                self.rotor_vars[i].set(config["rotors"][i])
                self.position_vars[i].set(config["positions"][i])
                self.ring_vars[i].set(config["rings"][i])
            self.reflector_var.set(config["reflector"])
            self.plug_entry.delete(0, "end")
            self.plug_entry.insert(0, config["plugboard"])
            self._create_machine()
        except Exception as e:
            messagebox.showerror("Paste Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = EnigmaGUI(root)
    root.mainloop()
