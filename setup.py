from setuptools import setup, find_packages

setup(
    name='mgnify_ro_crates',
    version='0.1.2',
    packages=find_packages(),
    install_requires=[
        'tqdm', 'requests', 'beautifulsoup4', 'arcp'
    ],
    author='Mahfouz Shehu, Aleksander Rajkovic, Sandy  Rogers',
    author_email='mahfouz@ebi.ac.uk, metagenomics@ebi.ac.uk',
    description='A packge for creating browsable RO-Crates from pipeline results',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/EBI-Metagenomics/mgnify-ro-crates.git',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'motus_ro_crates_preparer=motus_ro_crates_preparer:main',
        ],
    },
)