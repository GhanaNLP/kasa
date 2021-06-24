from distutils.core import setup

setup(name='Kasa',
    version='0.3.0',
    description='A library of translation and other NLP tools for the Ghanaian language Twi',
    author='NLPGhana',
    author_email='natural.language.processing.gh@gmail.com',
    license='MIT',
    packages=['Kasa'],
    install_requires=['gensim == 3.8.1', 'transformers@git+https://github.com/huggingface/transformers@eb3e072a3b24806c72e35e9246e1cf972de1c77f#egg=transformers', 'tokenizers'],
    include_package_data=True
)
