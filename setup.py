from distutils.core import setup

setup(name='Kasa',
    author='Dr.Paul Azunre',
    author_email='azunre@gmail.com',
    license='MIT',
    packages=['Kasa'],
    install_requires=['gensim == 3.8.1' , 'tokenizers==0.10.2'],
    include_package_data=True
)
 

