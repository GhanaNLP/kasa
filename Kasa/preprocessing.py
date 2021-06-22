import re
import unicodedata

# A subclass of kasa for preprocessing data
class Preprocessing:
    # dummy initialization method
    def __init__(self):
        # initialize with some default parameters here later
        pass
    
    def read_dataset(file_path, number=None, normalize=False, language="eng"):
    """
    Read NUMBER_OF_DATASET lines of data in supplied file_path
    Perform normalization (if normalize=True) based on input language(default:"eng", option:"twi")

    Returns
    -------
    List[list] of processed word tokens for sentences in file_path
    """

    with open(file_path) as file:
        data = file.read()
    data = data.split("\n")
    if number:
        assert number < len(data), "Number of dataset less than required subset"
        data = data[:number]
    if normalize:
        data = [normalize_line(line, language=language).split() for line in data]
    return data
    
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

    
    def normalize_line(s, language="eng"):
    """
    Perform some cleanup on supplied str based on language.
    
    Parameters
    ----------
    s : str
    language: str
        default is "eng" for english. option is "twi"
    
    Returns
    -------
    str of cleaned sentence
    """
    s = unicode_to_ascii(s)
    s = re.sub(r'([!.?])', r' \1', s)
    s = s.lower()
    if language == "twi":
        s = re.sub(r'[^a-zA-Z.ƆɔɛƐ!?’]+', r' ', s)
    elif language == "eng":
        s = re.sub(r'[^a-zA-Z.!?]+', r' ', s)
    s = re.sub(r'\s+', r' ', s)
    
    return s