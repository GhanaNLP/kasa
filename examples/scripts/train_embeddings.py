"#!/usr/bin/env python"

"""
Script for generating embeddings from a supplied file and saving them. 
Also for generating tsv files of the vectors and the metadata to enable visualising them.
AUTHOR : Lawrence Adu-Gyamfi
DATE : 03/06/2020

**********************
Update : 08/06/2020
Add additional option to use pretrained model

Update : 11/06/2020
Add command line options and flags
Add functions and code for computing correlations with wordsim353 
"""

import os
import pandas as pd
from scipy.stats import spearmanr
import argparse
from gensim.models import Word2Vec, FastText
from Kasa.Preprocessing import Preprocessing
from Kasa.StaticEmbeddings import StaticEmbedding


parser = argparse.ArgumentParser()
parser.add_argument("--data", help="Name of datafile to be used for the training")
parser.add_argument("-t", "--test", help="Indicate if current run is for a test or actual training", action="store_true")
parser.add_argument("-v", "--visualize", help="Save TSV files of tensors and metadata for visualization on embedding projector", action="store_true")
parser.add_argument("-s", "--save_model", help="Save learned model", action="store_true")
parser.add_argument("-c", "--corr", help="Compute correlation with wordsim dataset", action="store_true")
parser.add_argument("--init", help="Initialize using a pretrained word embedding model")
parser.add_argument("--epochs", help="Number of epochs to train new embeddings model", type=int)
args = parser.parse_args()

NUMBER_OF_DATASET = 100
DIMENSION = 300
DATA_DIR = "..\data"
MODELS_DIR = "..\models"
TWI_PATH = args.data if args.data else os.path.join(DATA_DIR, "jw300.en-tw.tw")
WORDSIM_PATH = os.path.join(DATA_DIR, "wordsim_tw.csv")

######################### RUNNING PARAMETERS ####################
TEST = True if args.test else False
VISUALIZE_FILE = True if args.visualize else False
SAVE_MODEL = True if args.save_model else False
COMPUTE_CORRELATION = True if args.corr else False
USE_PRETRAINED = True if args.init else False
EPOCHS = args.epochs if args.epochs else 1
#################################################################
init_filepath = args.init if args.init else None

if __name__ == "__main__":
    import datetime, time
    
    if TEST:
        print("This is just a test run!\n")

    GLOBAL_START = time.time()  # to track time for the entire run
    DATE = datetime.datetime.now()
    START_DATE = DATE.strftime("%d/%m/%Y %H:%M:%S")
    
    # create logger file to log details of run
    logger = open(f"log.txt", "w")
    
    logger.write(f"Run started on : {START_DATE}\n")
    logger.write(" ================================================================= \n")
    
    # Create an instance of Kasa preprocessing class
    TwiPreprocessor = Preprocessing()
    
    # Read twi data from supplied path to TWI file and preprocess
    print("Reading and processing dataset ...\n")
    start =time.time()
    number = NUMBER_OF_DATASET if TEST else None
    twi_data = TwiPreprocessor.read_dataset(filepath=TWI_PATH, number = number, normalize=True, language="tw")
    tot_time = time.time() - start
    logger.write(f"Time to complete reading file : {tot_time:.2f}\n")
    
    # create embeddings from preprocessed twi data
    print("Creating Embeddings ...\n")
    start =time.time()
    dimension = 50 if TEST else DIMENSION
    if USE_PRETRAINED:
        embeddings = StaticEmbedding.get_trained_embedding(twi_data, init_filepath, sg=1, negative=10, size=dimension, epochs=EPOCHS)
    else:
        embeddings = StaticEmbedding.get_embedding(twi_data, MODELS_DIR, FastText, size = dimension, sg=1, negative=10,  save=SAVE_MODEL)
    tot_time = time.time() - start
    logger.write(f"Time to complete creating embeddings file : {tot_time:.2f}\n")
    model_details = str(embeddings)
    logger.write(f"Model Details : {model_details}\n")
    print(f"Model Details : {model_details}")
    
    # generate tsv files for the tensors and the meta to be used for visualization
    if VISUALIZE_FILE:
        print("Generating TSV files for visualization ...\n")
        start = time.time()
        StaticEmbedding.prepare_for_visualization(embeddings, save_dir=MODELS_DIR)
        tot_time = time.time() - start
        logger.write(f"Time to complete creating TSV  file : {tot_time:.2f}\n")
    
    #compute correlations with wordsim data
    if COMPUTE_CORRELATION:
        print("Computing Correlation")
        word_sim = pd.read_csv(WORDSIM_PATH, header=None,)
        word_sim.columns = ["word1", "word2", "relatedness"]
        similarities = [StaticEmbedding.get_similarity(*word_sim[["word1","word2"]].values[i], embeddings) for i in range(len(word_sim))]
        word_sim['similarities'] = similarities
        corr =spearmanr(word_sim[["relatedness", "similarities"]])
        logger.write("==================================================================\n")
        logger.write(str(corr))
        logger.write("\n==================================================================\n")
        wordsim_update = f"wordsim_{START_DATE.split()[-1]}.csv"
        word_sim.to_csv(wordsim_update, index=False)
        print(f"Correlation is : {corr}\n")


    logger.write(f"Run completed on : {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")

    logger.close()

    print("Completed Run successfully!\n")
