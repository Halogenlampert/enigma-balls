import pytest
from enigma.Umkehrwalze import Umkehrwalze

def test_reflector_encodes_symmetrically():
    wiring = "YRUHQSLDPXNGOKMIEBFZCWVJAT"  # UKW-B
    reflector = Umkehrwalze(wiring)

    for i in range(26):
        result = reflector.encode(i)
        back = reflector.encode(result)
        assert back == i, f"Reflector not symmetric at index {i}"

def test_reflector_invalid_length():
    with pytest.raises(AssertionError):
        Umkehrwalze("ABCDE")  # too short

def test_reflector_self_mapping_disallowed():
    # A → A would violate Enigma design
    bad_wiring = list("YRUHQSLDPXNGOKMIEBFZCWVJAT")
    bad_wiring[0] = "A"  # force A → A
    with pytest.raises(ValueError):
        Umkehrwalze("".join(bad_wiring))

def test_reflector_non_symmetric_mapping_disallowed():
    # A → B, but B → C = invalid
    bad_wiring = list("YRUHQSLDPXNGOKMIEBFZCWVJAT")
    bad_wiring[1] = "C"  # B → C instead of A
    with pytest.raises(ValueError):
        Umkehrwalze("".join(bad_wiring))
