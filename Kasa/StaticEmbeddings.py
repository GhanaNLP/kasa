# -*- coding: utf-8 -*-
"""
Created on Tue Jun 22 18:05:25 2021

@author: azunr
"""
import os
from gensim.models import Word2Vec, FastText, fasttext
from gensim.test.utils import datapath
from scipy.stats import spearmanr
import argparse

# A subclass of kasa for preprocessing data
class StaticEmbedding:
    # dummy initialization method
    def __init__(self):
        # initialize with some default parameters here later
        pass

    def get_embedding(data, MODELS_DIR, typeFunc=Word2Vec, size=100, window=5, min_count=5, sg=0, save=False, negative=10):
        """
        Generate embeddings for input data using either word2vec or Fasttext from gensim
    
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
        embeddings  = typeFunc(data,size=size, window=window, min_count=min_count, workers=4, sg=sg, negative=negative)
        if save:
            embeddings.save(f"{MODELS_DIR}/{typeFunc.__name__}_embedding.mod")
        return embeddings
    
    
    
    def get_trained_embedding(data, model, typeFunc=fasttext, epochs = 5, size=100, window=5, min_count=5, sg=0, save=False, negative=10):
        """
        Train embeddings for input data, starting from pretrained model. Currently works with either word2vec or Fasttext from gensim
    
        """
        # load the pretrained model
        print("Loading pretrained model ..\n")
        embeddings = typeFunc.load_facebook_model(datapath(os.path.abspath(model)))
        # build the vocab
        embeddings.build_vocab(sentences=data, update=True)
       # embeddings  = typeFunc(size=size, window=window, min_count=min_count, workers=4, sg=sg)
        print("Training embeddings ...\n")
        embeddings.train(sentences=data, epochs=epochs,word_count=0, total_examples=embeddings.corpus_count, window=window, min_count=min_count, sg=sg, total_words=embeddings.corpus_total_words, negative=negative)
        if save:
            embeddings.save(f"./{typeFunc.__name__}_embedding.mod")
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
    
    def get_similarity(word1, word2, model):
        """
        Return cosine similarity between word1 and word2 using the supplied model
    
        Parameters
        ----------
        word1 : str
        word2 : str
        model : gensim model type of learned word embeddings
    
        """
        return model.wv.similarity(word1, word2)
    
    def get_most_similar_words(word, model):
        """
        Return most similar words for a given model
    
        Parameters
        ----------
        word : str
        model : gensim model type of learned word embeddings
    
        """
        return word2vec.wv.most_similar(word)
