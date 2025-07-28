import pytest
from enigma.RotorFactory import RotorFactory
from enigma.Rotor import Rotor

def test_create_returns_rotor_instance():
    rotor = RotorFactory.create("I")
    assert isinstance(rotor, Rotor)
    assert hasattr(rotor, 'encode_forward')
    assert hasattr(rotor, 'encode_backward')

def test_rotor_encoding_consistency():
    rotor = RotorFactory.create("II", position=0, ring_setting=0)
    for i in range(26):
        forward = rotor.encode_forward(i)
        backward = rotor.encode_backward(forward)
        assert backward == i, f"Rotor II failed encoding round-trip at index {i}"

def test_list_available_rotors():
    available = RotorFactory.list_available()
    expected = ["I", "II", "III", "IV", "V"]
    assert set(available) == set(expected)
