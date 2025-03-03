import pytest
from khaya.preprocessor import num_convert

def test_convert_basic_number():
    input_text = "I have 3 apples."
    expected = "I have three apples."
    assert num_convert(input_text) == expected

def test_convert_multiple_numbers():
    input_text = "There are 5 cats and 10 dogs."
    expected = "There are five cats and ten dogs."
    assert num_convert(input_text) == expected

def test_convert_zero():
    input_text = "The value is 0."
    expected = "The value is zero."
    assert num_convert(input_text) == expected

def test_convert_large_number():
    input_text = "The population is 123456789."
    expected = "The population is one hundred and twenty-three million, four hundred and fifty-six thousand, seven hundred and eighty-nine."
    assert num_convert(input_text) == expected

def test_convert_number_with_punctuation():
    input_text = "He is 25, and she is 30."
    expected = "He is twenty-five, and she is thirty."
    assert num_convert(input_text) == expected

def test_convert_number_in_word():
    input_text = "h3llo world"
    expected = "h3llo world"  # when numbers are used to replace special characters, they should not be converted
    assert num_convert(input_text) == expected

def test_convert_empty_input():
    input_text = ""
    expected = ""
    assert num_convert(input_text) == expected

def test_convert_no_numbers():
    input_text = "Hello world!"
    expected = "Hello world!"
    assert num_convert(input_text) == expected

def test_convert_negative_number():
    input_text = "Temperature is -5 degrees."
    expected = "Temperature is -five degrees."  
    assert num_convert(input_text) == expected

def test_convert_decimal_number():
    input_text = "The price is 19.99."
    expected = "The price is nineteen.ninety-nine."  
    assert num_convert(input_text) == expected