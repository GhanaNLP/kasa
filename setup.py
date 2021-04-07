from distutils.core import setup

setup(name='Kasa',
    version='0.2.5',
    description = 'A library of translation and other NLP tools for the Ghanaian language Twi',
    author='Dr.Paul Azunre',
    author_email='azunre@gmail.com',
    license='MIT',
    packages=['Kasa'],
    install_requires=['gensim == 3.8.1' , 'transformers', 'tokenizers==0.10.2'],
    include_package_data=True
)
 

