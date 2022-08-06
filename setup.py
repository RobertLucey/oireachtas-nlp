from setuptools import (
    find_packages,
    setup
)

INSTALL_REQUIRES = (
    'oireachtas_data',
    'textstat',
    'gensim',
    'nltk',
    'cached_property',
    'sklearn_pandas',
    'tqdm',
    'textgenrnn',
    'tensorflow==2.3.2'  # Required by textgenrnn
)

setup(
    name='oireachtas-nlp',
    version='1.0.8',
    python_requires='>=3.6',
    description='nlp on data from the oireachtas api relating to members / parties',
    long_description='nlp on data from the oireachtas api relating to members / parties',
    author='Robert Lucey',
    url='https://github.com/RobertLucey/oireachtas-nlp',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=INSTALL_REQUIRES,
    entry_points={
        'console_scripts': [
            'oir_word_usage_by = oireachtas_nlp.bin.sounds_like:main',
            'oir_sounds_like = oireachtas_nlp.bin.word_usage_by:main',
            'oir_belong = oireachtas_nlp.bin.belong:main',
            'oir_sentiment = oireachtas_nlp.bin.sentiment:main',
            'oir_lexical_diversity = oireachtas_nlp.bin.lexical_diversity:main',
            'oir_lexical_difficulty = oireachtas_nlp.bin.lexical_difficulty:main',
            'oir_generate_text = oireachtas_nlp.bin.generate_text:main',
            'oir_generate_text_from_model = oireachtas_nlp.bin.generate_text_from_model:main',
        ]
    }
)
