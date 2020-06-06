"#!/usr/bin/env python"

"""
Script for generating embeddings from a supplied file and saving them. 
Also for generating tsv files of the vectors and the metadata to enable visualising them.
AUTHOR : Lawrence Adu-Gyamfi
DATE : 03/06/2020
"""

import numpy as np
import unicodedata
import re
import os
from gensim.models import Word2Vec, FastText


NUMBER_OF_DATASET = 100  # just a small value used for the test replace with the correct number
DATA_DIR = "./DATA"  # to be replaced with correct directory of text files
MODELS_DIR = "./MODELS" 
ENG_PATH = os.path.join(DATA_DIR, "jw300.en-tw.en") # this is only necessary when using the jw300 dataset.
TWI_PATH = os.path.join(DATA_DIR, "jw300.en-tw.tw") # replace with the correct filenames

# some clean up exercise before starting run
assert os.path.exists(DATA_DIR), "Path to data files does not exist. Please check!"
if not os.path.exists(MODEL_DIR):
    os.mkdir(MODELS_DIR)

def unicode_to_ascii(s):
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn')


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

def get_embedding(data, typeFunc=Word2Vec, size=100, window=5, min_count=5, sg=0, save=False):
    """
    Generate embeddings for input data. Currently works with either word2vec or Fasttext from gensim

    Parameters
    ----------
    data : list[list]
        preprocessed word tokens
    typeFunc : gensim.model name
        Either Word2Vec or FastText (without "") (default is Word2Vec)
    size : int
        Dimension of embeddings to be generated (default=100)
    window : int
        size of window to be considered for word embeddings (default=5)
    min_count : int
        
    sg : int (0,1)
    
    save : bool
        if True, save generated embeddings in current working directory of script

    Returns
    -------
    Embeddings of type gensim.model
    """
    embeddings  = typeFunc(data,size=size, window=window, min_count=min_count, workers=4, sg=sg)
    if save:
        embeddings.save(f"{MODELS_DIR}/{typeFunc.__name__}_embedding.mod")
    return embeddings

def prepare_for_visualization(model, model_path=None, save_dir="."):
    """
    Generates tsv formats of metadata and tensors/vectors for embeddings. 
    Useful for tensorflow embeddings projector.

    Parameters
    ----------
    model : gensim model type
        embeddings created using either word2vec or fasttext
    model_path : path, optional
        Path to a saved embeddings file (default is None)
    save_dir : path
        Path to directory to save created tsv files. (default is current working directory of script)

    Returns
    -------
    A tuple of tensors and metadata of embeddings
    """
    if model_path:   # to do -> check correctness of path
        model = gensim.models.KeyedVectors.load_word2vec_format(f"{model_path}", binary=False, encoding="utf-16")
    with open(f"{save_dir}/embedding_tensors.tsv", 'w+') as tensors:
        with open(f"{save_dir}/embedding_metadata.dat", 'w+') as metadata:
            for word in model.wv.index2word:
                #encoded=word.encode('utf-8')
                encoded = word
                metadata.write(encoded + '\n')
                vector_row = '\t'.join(map(str, model[word]))
                tensors.write(vector_row + '\n')
    return tensors, metadata


if __name__ == "__main__":
    import datetime, time
    
    GLOBAL_START = time.time()  # to track time for the entire run
    DATE = datetime.datetime.now()
    START_DATE = DATE.strftime("%d/%m/%Y %H:%M:%S")
    
    # create logger file to log details of run
    logger = open("log.txt", "w+")
    
    logger.write(f"Run started on : {START_DATE}\n")
    logger.write(" ================================================================= \n")
    
    # Read twi data from supplied path to TWI file and preprocess
    print("Reading and processing dataset ...\n")
    start =time.time()
    twi_data = read_dataset(TWI_PATH, normalize=True, language="twi")
    tot_time = time.time() - start
    logger.write(f"Time to complete reading file : {tot_time:.2f}\n")
    
    # create embeddings from preprocessed twi data
    print("Creating Embeddings ...\n")
    start =time.time()
    embeddings = get_embedding(twi_data, FastText, size = 100, sg=1, save=True)
    tot_time = time.time() - start
    logger.write(f"Time to complete creating embeddings file : {tot_time:.2f}\n")
    
    # generate tsv files for the tensors and the meta to be used for visualization
    print("Generating TSV files for visualization ...\n")
    start = time.time()
    prepare_for_visualization(embeddings, save_dir=MODELS_DIR)
    tot_time = time.time() - start
    logger.write(f"Time to complete creating TSV  file : {tot_time:.2f}\n")
    
    logger.write(f"Run completed on : {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")

    logger.write(f"Time to complete entire run : {GLOBAL_START - time.time():.2f}\n")

    logger.close()

    print("Completed Run successfully!\n")

