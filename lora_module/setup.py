from setuptools import setup, find_packages

setup(
    name='lora_module',
    version='0.1.0',
    description='A module for LoRa communication',
    author='Nash Reilly',
    author_email='nash.reilly@twosixtech.com',
    packages=find_packages(),  
    install_requires=[
        'pyserial',
        'requests',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
