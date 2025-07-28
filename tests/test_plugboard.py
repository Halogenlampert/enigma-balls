import pytest
from enigma.Plugboard import Plugboard

def test_basic_plugboard_encoding():
    pb = Plugboard([("A", "Z"), ("B", "Y")])

    assert pb.encode(ord("A") - ord("A")) == ord("Z") - ord("A")
    assert pb.encode(ord("Z") - ord("A")) == ord("A") - ord("A")
    assert pb.encode(ord("B") - ord("A")) == ord("Y") - ord("A")
    assert pb.encode(ord("Y") - ord("A")) == ord("B") - ord("A")
    assert pb.encode(ord("C") - ord("A")) == ord("C") - ord("A")  # unplugged passthrough

def test_identity_plugboard():
    pb = Plugboard()
    for i in range(26):
        assert pb.encode(i) == i

def test_plugboard_too_many_pairs():
    with pytest.raises(ValueError):
        Plugboard([("A", "B"), ("C", "D"), ("E", "F"), ("G", "H"), ("I", "J"),
                   ("K", "L"), ("M", "N"), ("O", "P"), ("Q", "R"), ("S", "T"),
                   ("U", "V")])  # 11 pairs

def test_plugboard_letter_used_twice():
    with pytest.raises(ValueError):
        Plugboard([("A", "B"), ("A", "C")])  # A used twice

def test_plugboard_self_plug():
    with pytest.raises(ValueError):
        Plugboard([("A", "A")])  # self-mapping not allowed
