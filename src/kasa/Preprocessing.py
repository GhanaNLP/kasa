import re
import unicodedata

# A subclass of kasa for preprocessing data
class Preprocessing:
    # dummy initialization method
    def __init__(self):
        # initialize with some default parameters here later
        pass
    
    # read in parallel twi - english dataset
    def read_parallel_dataset(self,filepath_twi='../data/jw300.en-tw.tw',
                              filepath_english='../data/jw300.en-tw.en'):
        
        # read english data
        english_data = []
        with open(filepath_english, encoding='utf-8') as file:
            line = file.readline()
            cnt = 1
            while line:
                english_data.append(line.strip())
                line = file.readline()
                cnt += 1

        # read twi data
        twi_data = []
        with open(filepath_twi, encoding='utf-8') as file:
    
            # twi=file.read()
            line = file.readline()
            cnt = 1
            while line:
                twi_data.append(line.strip())
                line = file.readline()
                cnt += 1
                
        return twi_data,english_data
    
    # convert input sentence from unicode to ascii format
    def unicode_to_ascii(self,s):
        return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

    # normalize input twi sentence
    def normalize_twi(self,s):
        s = self.unicode_to_ascii(s)
        s = re.sub(r'([!.?])', r' \1', s)
        s = re.sub(r'[^a-zA-Z.ƆɔɛƐ!?’]+', r' ', s)
        s = re.sub(r'\s+', r' ', s)
        return s
    
    # normalize input english sentence
    def normalize_eng(self,s):
        s = self.unicode_to_ascii(s)
        s = re.sub(r'([!.?])', r' \1', s)
        s = re.sub(r'[^a-zA-Z.!?]+', r' ', s)
        s = re.sub(r'\s+', r' ', s)
        return s
      

