# Kasa
English to Twi translation library/system being put together by the Ghana NLP team.

# Quickstart
Install Kasa directly from online link:

1. `pip install git+https://github.com/GhanaNLP/kasa`

When editing Kasa locally, it is helpful to install from a local copy of Kasa instead:

1. `git clone https://github.com/GhanaNLP/kasa`

2. `cd kasa`

3. `pip install .`

The `examples/` folder of the repo constains examples you can directly run to test various functionalities, e.g., 

`python load_and_preprocess_parallel_dataset.py`

This may require obtaining some data files and accordingly passing the right paths to the methods in `load_and_preprocess_parallel_dataset.py`. All this should be self-explanatory if you look at the code.

# Data Files
You will need to download two corpus (English and Twi) into a data folder on your local machine in order to run the examples, using the link below.

`https://www.kaggle.com/azunre/jw300entw`

# Contributing
Please first clone this repo to your local machine, using a command line tool such as Cygwin or Anaconda Prompt:

`git clone https://github.com/GhanaNLP/kasa`

Create a branch for your contributions, and check it out:

1. `git branch <your-branch-name>`

2. `git checkout <your-branch-name>`

Try to pick a branch name that described what you are planning to add to the library, see current branch names in this repo for ideas.

Write your code, test it and then push to your branch:

1. `git push origin <your-branch-name>`

Create a pull request using the online github repo page, making sure to include a senior member of the team to review your work before merging it into the master branch of the repo. 

Never push changes to master!!!

# Notebooks
Usually, we start our work by implementing it directly as a Jupyter Python notebook and host it on Kaggle runtime so team members can play around with ideas. Below is a list of the notebooks we have worked on so far, as well as links to where they are hosted on Kaggle so . They are located in the `notebooks/` subfolder of this repo, and the hope is to convert all useful methods they contain into refined methods within the `Kasa` library.

*)The `data_processing.ipynb` preprocessing notebook is also loaded on kaggle @ https://www.kaggle.com/azunre/ghananlp-kasa-preprocessing-word2vec-v0-1 

*)The `ghananlp-kasa-retrieval-v0-1.ipynb` retrieval "proof-of-concept" notebook is also loaded on kaggle @ https://www.kaggle.com/azunre/ghananlp-kasa-retrieval-v0-

*)The `eng_twi_transformer.ipynb` transformer-based english-to-twi NMT model notebook is also loaded on kaggle @ 
https://www.kaggle.com/azunre/ghananlp-kasa-nmt-transformer-v0-1

# Description of Key Files
It is helpful to know the function of the following files when contributing:

*)`HISTORY.md` -- what functionality was added during each version/release, and what is planned to be added next/in the near future.

*)`setup.py` -- specify dependencies for added methods here

*)`__init__.py` -- * import specification file, does not exist for now...

*)`MANIFEST.in` -- (yet to be added) this will be used to make sure required files are copied over when the library is installed (no such requirement yet)

# Need More Information on Syntax for Classes, Methods, etc?
The method `dir` is very useful for debugging your classes and methods, example:

1. `from Kasa import Preprocessing`
2. `dir(Preprocessing)`

If you need further information, either contact Ghana NLP members directly, or see a repo on github like this one:

https://github.com/algorine/simon
