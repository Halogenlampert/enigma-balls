from enigma.Umkehrwalze import Umkehrwalze

class UmkehrwalzeFactory:
    _reflector_configs = {
        "UKW-A": "EJMZALYXVBWFCRQUONTSPIKHGD",
        "UKW-B": "YRUHQSLDPXNGOKMIEBFZCWVJAT",
        "UKW-C": "FVPJIAOYEDRZXWGCTKUQSBNMHL",
    }

    @staticmethod
    def create(name: str) -> Umkehrwalze:
        wiring = UmkehrwalzeFactory._reflector_configs[name]
        return Umkehrwalze(wiring)

    @staticmethod
    def list_available():
        return list(UmkehrwalzeFactory._reflector_configs.keys())
