class Umkehrwalze:
    def __init__(self, wiring: str):
        assert len(wiring) == 26, "Wiring must be 26 letters"
        self.wiring = [ord(c) - ord('A') for c in wiring]

        for i, out in enumerate(self.wiring):
            if out == i:
                raise ValueError(f"Invalid reflector: letter {chr(i + ord('A'))} maps to itself")
            if self.wiring[out] != i:
                raise ValueError(f"Invalid reflector: mapping not symmetric at {chr(i + ord('A'))}")

    def encode(self, c: int) -> int:
        return self.wiring[c]
