import pytest
from enigma.UmkehrwalzeFactory import UmkehrwalzeFactory
from enigma.Umkehrwalze import Umkehrwalze

def test_create_returns_valid_umkehrwalze():
    ukw = UmkehrwalzeFactory.create("UKW-A")
    assert isinstance(ukw, Umkehrwalze)
    for i in range(26):
        # Verify symmetry of each built-in reflector
        mapped = ukw.encode(i)
        assert ukw.encode(mapped) == i

def test_list_available_umkehrwalzen():
    available = UmkehrwalzeFactory.list_available()
    expected = ["UKW-A", "UKW-B", "UKW-C"]
    assert set(available) == set(expected)

def test_invalid_reflector_name():
    with pytest.raises(KeyError):
        UmkehrwalzeFactory.create("UKW-Z")
