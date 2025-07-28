class Rotor:
    def __init__(self, wiring: str, notch: str, ring_setting: int = 0, position: int = 0):
        assert len(wiring) == 26, "Wiring must be 26 letters"
        self.wiring = [ord(c) - ord('A') for c in wiring]
        self.reverse_wiring = [0] * 26
        for i, val in enumerate(self.wiring):
            self.reverse_wiring[val] = i
        
        self.notch = ord(notch) - ord('A')  # Turnover position as index
        self.ring_setting = ring_setting  # Ringstellung (0-indexed)
        self.position = position  # Rotor's current offset (0 = A)

    def step(self):
        self.position = (self.position + 1) % 26

    def at_notch(self):
        adjusted_notch = (self.notch - self.ring_setting) % 26
        return self.position == adjusted_notch


    def encode_forward(self, c: int) -> int:
        """Pass signal from right to left (keyboard → reflector)"""
        offset = (c + self.position - self.ring_setting) % 26
        mapped = self.wiring[offset]
        return (mapped - self.position + self.ring_setting) % 26

    def encode_backward(self, c: int) -> int:
        """Pass signal from left to right (reflector → lampboard)"""
        offset = (c + self.position - self.ring_setting) % 26
        mapped = self.reverse_wiring[offset]
        return (mapped - self.position + self.ring_setting) % 26
