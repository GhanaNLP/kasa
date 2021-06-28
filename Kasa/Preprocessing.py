import re
import unicodedata

# A subclass of kasa for preprocessing data
class Preprocessing:
    # dummy initialization method
    def __init__(self):
        # initialize with some default parameters here later
        pass
    
    def read_dataset(self,filepath, number=None, normalize=False, language="en"):
        """
        Read NUMBER_OF_DATASET lines of data in supplied file_path
        Perform normalization (if normalize=True) based on input language(default:"en",
        list of all option:["en","tw"])
    
        Returns
        -------
        List[list] of processed word tokens for sentences in file_path
        """
        with open(filepath, encoding='utf-8') as file:
            data = file.read()
        data = data.split("\n")
        if number:
            assert number < len(data), "Number of dataset less than required subset"
            data = data[:number]
        if normalize:
            data = [self.normalize_line(line, language=language).split() for line in data]
        return data
    
    # read in parallel twi - english dataset
    def read_parallel_dataset(self,filepath1,filepath2):
        
        # read 1st data
        data1 = []
        with open(filepath1, encoding='utf-8') as file:
    
            # twi=file.read()
            line = file.readline()
            cnt = 1
            while line:
                data1.append(line.strip())
                line = file.readline()
                cnt += 1
        
        # read 2nd data
        data2 = []
        with open(filepath2, encoding='utf-8') as file:
            line = file.readline()
            cnt = 1
            while line:
                data2.append(line.strip())
                line = file.readline()
                cnt += 1

        return data1,data2
    
    # convert input sentence from unicode to ascii format
    def unicode_to_ascii(self,s):
        return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

    
    def normalize_line(self,s, language="en"):
        """
        Perform some cleanup on supplied str based on language.
        
        Parameters
        ----------
        s : str
        language: str
            default is "en" for english. Current option list is ["en","tw"]
        
        Returns
        -------
        str of cleaned sentence
        """
        s = self.unicode_to_ascii(s)
        s = re.sub(r'([!.?])', r' \1', s)
        s = s.lower()
        if language == "tw":
            s = re.sub(r'[^a-zA-Z.ƆɔɛƐ!?’]+', r' ', s)
        elif language == "en":
            s = re.sub(r'[^a-zA-Z.!?]+', r' ', s)
        s = re.sub(r'\s+', r' ', s)
    
        return s