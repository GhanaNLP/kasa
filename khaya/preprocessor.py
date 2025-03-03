from num2words import num2words
import re

# function to deal with digit to words conversion of corresponding numbers
def num_convert(text):
    def replace(match):
        return num2words(int(match.group()))
    
    return re.sub(r'\b\d+\b', replace, text)

