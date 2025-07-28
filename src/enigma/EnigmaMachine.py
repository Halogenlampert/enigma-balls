from enigma.Rotor import Rotor
from enigma.Umkehrwalze import Umkehrwalze
from enigma.Plugboard import Plugboard

class EnigmaMachine:
    def __init__(self, rotor_left: Rotor, rotor_middle: Rotor, rotor_right: Rotor,
                 reflector: Umkehrwalze, plugboard: Plugboard):
        self.rotor_left = rotor_left
        self.rotor_middle = rotor_middle
        self.rotor_right = rotor_right
        self.reflector = reflector
        self.plugboard = plugboard

    def _step_rotors(self):
        # Double-stepping logic
        if self.rotor_middle.at_notch():
            self.rotor_left.step()
            self.rotor_middle.step()
        elif self.rotor_right.at_notch():
            self.rotor_middle.step()

        self.rotor_right.step()

    def encode_char(self, char: str) -> str:
        if not char.isalpha() or len(char) != 1:
            raise ValueError("Input must be a single A-Z character")

        c = ord(char.upper()) - ord('A')

        self._step_rotors()

        # Pass through plugboard (pre)
        c = self.plugboard.encode(c)

        # Forward through rotors (right to left)
        c = self.rotor_right.encode_forward(c)
        c = self.rotor_middle.encode_forward(c)
        c = self.rotor_left.encode_forward(c)

        # Reflect
        c = self.reflector.encode(c)

        # Reverse through rotors (left to right)
        c = self.rotor_left.encode_backward(c)
        c = self.rotor_middle.encode_backward(c)
        c = self.rotor_right.encode_backward(c)

        # Pass through plugboard (post)
        c = self.plugboard.encode(c)

        return chr(c + ord('A'))

    def encode(self, text: str) -> str:
        if not text.isalpha():
            raise ValueError("Input must contain only A–Z letters")
        return ''.join(self.encode_char(c) for c in text)

