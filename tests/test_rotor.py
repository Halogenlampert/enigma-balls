import pytest
from enigma.Rotor import Rotor

def test_rotor_encoding_identity():
    """Test that encoding forward then backward returns the same letter"""
    rotor = Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", notch='Q', ring_setting=0, position=0)
    
    for i in range(26):
        forward = rotor.encode_forward(i)
        backward = rotor.encode_backward(forward)
        assert backward == i, f"Failed at index {i}: forward={forward}, backward={backward}"

def test_rotor_step_changes_encoding():
    """Test that stepping the rotor changes the output"""
    rotor = Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", notch='Q', ring_setting=0, position=0)

    c = ord('A') - ord('A')  # input = 0
    first_output = rotor.encode_forward(c)
    
    rotor.step()
    second_output = rotor.encode_forward(c)

    assert first_output != second_output, "Rotor stepping should change the encoding"

def test_rotor_at_notch():
    """Test that at_notch returns True only when at notch position"""
    rotor = Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", notch='Q', ring_setting=0, position=0)
    assert rotor.at_notch() is False
    
    rotor.position = ord('Q') - ord('A')
    assert rotor.at_notch() is True
