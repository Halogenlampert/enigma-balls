from enigma.Rotor import Rotor

class RotorFactory:
    _rotor_configs = {
        "I":     ("EKMFLGDQVZNTOWYHXUSPAIBRCJ", 'Q'),
        "II":    ("AJDKSIRUXBLHWTMCQGZNPYFVOE", 'E'),
        "III":   ("BDFHJLCPRTXVZNYEIWGAKMUSQO", 'V'),
        "IV":    ("ESOVPZJAYQUIRHXLNFTGKDCMWB", 'J'),
        "V":     ("VZBRGITYUPSDNHLXAWMJQOFECK", 'Z'),
    }

    @staticmethod
    def create(rotor_name: str, position=0, ring_setting=0) -> Rotor:
        wiring, notch = RotorFactory._rotor_configs[rotor_name]
        return Rotor(wiring, notch, ring_setting=ring_setting, position=position)

    @staticmethod
    def list_available():
        return list(RotorFactory._rotor_configs.keys())
