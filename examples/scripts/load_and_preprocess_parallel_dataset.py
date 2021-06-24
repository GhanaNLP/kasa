# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 16:20:38 2020

@author: azunr
"""

from Kasa.Preprocessing import Preprocessing # note form of library import

# Create an instance of Kasa preprocessing class
TwiPreprocessor = Preprocessing()

# Read raw parallel dataset
raw_data_twi,raw_data_en = TwiPreprocessor.read_parallel_dataset(
        filepath1='../../data/jw300.en-tw.tw',
        filepath2='../../data/jw300.en-tw.en')

# Normalize the raw data
raw_data_en = [TwiPreprocessor.normalize_line(data,language="en") for data in raw_data_en]
raw_data_twi = [TwiPreprocessor.normalize_line(data,language="tw") for data in raw_data_twi]

# Tokenize into words - which just means split each sentence into word units/tokens
data=[]
for tw in raw_data_twi:
    data.append(tw.split())
    
# Print sample data - first ten sentences - to make sure it is working as expected 
print("Output from parallel data read")
print(data[:10])

# Or just read a monolingual dataset
raw_data_gur = TwiPreprocessor.read_dataset(filepath='../../data/gur.tok')

print("Output from monolingual data read:")
print(raw_data_gur[:10])