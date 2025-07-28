class Plugboard:
    def __init__(self, pairs=None):
        self.mapping = list(range(26))  # identity by default

        if pairs is None:
            pairs = []

        if len(pairs) > 10:
            raise ValueError("At most 10 plug pairs allowed")

        used = set()

        for a, b in pairs:
            ia, ib = ord(a.upper()) - ord('A'), ord(b.upper()) - ord('A')
            if ia in used or ib in used:
                raise ValueError(f"Letter already plugged: {a} or {b}")
            if ia == ib:
                raise ValueError("Cannot plug a letter to itself")
            self.mapping[ia] = ib
            self.mapping[ib] = ia
            used.add(ia)
            used.add(ib)

    def encode(self, c: int) -> int:
        return self.mapping[c]
