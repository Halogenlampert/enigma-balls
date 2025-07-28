import pytest
from enigma.RotorFactory import RotorFactory
from enigma.UmkehrwalzeFactory import UmkehrwalzeFactory
from enigma.Plugboard import Plugboard
from enigma.EnigmaMachine import EnigmaMachine

def test_simple_encoding_no_plugboard():
    rotor_r = RotorFactory.create("I", position=0, ring_setting=0)
    rotor_m = RotorFactory.create("II", position=0, ring_setting=0)
    rotor_l = RotorFactory.create("III", position=0, ring_setting=0)
    reflector = UmkehrwalzeFactory.create("UKW-B")
    plugboard = Plugboard([])

    machine = EnigmaMachine(rotor_l, rotor_m, rotor_r, reflector, plugboard)

    result = machine.encode("A")
    assert isinstance(result, str)
    assert len(result) == 1

def test_encoding_is_symmetric():
    rotor_r = RotorFactory.create("I", position=0, ring_setting=0)
    rotor_m = RotorFactory.create("II", position=0, ring_setting=0)
    rotor_l = RotorFactory.create("III", position=0, ring_setting=0)
    reflector = UmkehrwalzeFactory.create("UKW-B")
    plugboard = Plugboard([("A", "B"), ("C", "D")])

    machine1 = EnigmaMachine(rotor_l, rotor_m, rotor_r, reflector, plugboard)

    # Save original rotor positions to clone into the second machine
    text = "HELLOWORLD"
    encrypted = machine1.encode(text)

    # Re-create the machine in the same initial state
    rotor_r2 = RotorFactory.create("I", position=0, ring_setting=0)
    rotor_m2 = RotorFactory.create("II", position=0, ring_setting=0)
    rotor_l2 = RotorFactory.create("III", position=0, ring_setting=0)
    plugboard2 = Plugboard([("A", "B"), ("C", "D")])
    machine2 = EnigmaMachine(rotor_l2, rotor_m2, rotor_r2, reflector, plugboard2)

    decrypted = machine2.encode(encrypted)
    assert decrypted == text

def test_non_alpha_characters_raise_error():
    rotor_r = RotorFactory.create("I", position=0, ring_setting=0)
    rotor_m = RotorFactory.create("II", position=0, ring_setting=0)
    rotor_l = RotorFactory.create("III", position=0, ring_setting=0)
    reflector = UmkehrwalzeFactory.create("UKW-B")
    plugboard = Plugboard([])

    machine = EnigmaMachine(rotor_l, rotor_m, rotor_r, reflector, plugboard)

    with pytest.raises(ValueError):
        machine.encode("A B!C?")


def test_invalid_input_to_encode_char():
    rotor_r = RotorFactory.create("I", position=0, ring_setting=0)
    rotor_m = RotorFactory.create("II", position=0, ring_setting=0)
    rotor_l = RotorFactory.create("III", position=0, ring_setting=0)
    reflector = UmkehrwalzeFactory.create("UKW-B")
    plugboard = Plugboard([])

    machine = EnigmaMachine(rotor_l, rotor_m, rotor_r, reflector, plugboard)

    with pytest.raises(ValueError):
        machine.encode_char("1")

    with pytest.raises(ValueError):
        machine.encode_char("AB")
        
def test_double_stepping_logic_is_triggered():
    # Rotor II has notch at 'E' (index 4)
    # Set rotor M at E, and rotor R at a value that won't trigger middle stepping itself
    rotor_r = RotorFactory.create("I", position=0)
    rotor_m = RotorFactory.create("II", position=4)  # notch position
    rotor_l = RotorFactory.create("III", position=0)

    reflector = UmkehrwalzeFactory.create("UKW-B")
    plugboard = Plugboard([])

    machine = EnigmaMachine(rotor_l, rotor_m, rotor_r, reflector, plugboard)

    # Step once → triggers rotor_m.at_notch() → should step L and M
    machine.encode("A")

    assert rotor_m.position == 5  # stepped from 4 → 5
    assert rotor_l.position == 1  # stepped from 0 → 1 due to middle's notch


def test_normal_right_to_middle_step_only():
    # Rotor I has notch at Q (index 16)
    rotor_r = RotorFactory.create("I", position=16)  # right rotor at notch
    rotor_m = RotorFactory.create("II", position=0)  # middle rotor NOT at notch
    rotor_l = RotorFactory.create("III", position=0)

    reflector = UmkehrwalzeFactory.create("UKW-B")
    plugboard = Plugboard([])

    machine = EnigmaMachine(rotor_l, rotor_m, rotor_r, reflector, plugboard)

    machine.encode("A")

    # Only rotor_r and rotor_m should have stepped
    assert rotor_r.position == 17  # 16 → 17
    assert rotor_m.position == 1   # 0 → 1 (stepped because R was at notch)
    assert rotor_l.position == 0   # unchanged

