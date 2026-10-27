from setuptools import (
    find_packages,
    setup
)

INSTALL_REQUIRES = (
    'oireachtas_data<0.2.0',
    'setuptools<82',  # oireachtas_data imports pkg_resources at runtime.
    'textstat',
    'gensim',
    'nltk',
    'cached_property',
    'sklearn_pandas',
    'tqdm',
    'textgenrnn',
    'gpt_2_simple'
)

setup(
    name='oireachtas-nlp',
    version='1.0.17',
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
            'oir_word_usage_by = oireachtas_nlp.bin.word_usage_by:main',
            'oir_sounds_like = oireachtas_nlp.bin.sounds_like:main',
            'oir_belong = oireachtas_nlp.bin.belong:main',
            'oir_sentiment = oireachtas_nlp.bin.sentiment:main',
            'oir_lexical_diversity = oireachtas_nlp.bin.lexical_diversity:main',
            'oir_lexical_difficulty = oireachtas_nlp.bin.lexical_difficulty:main',
            'oir_generate_text = oireachtas_nlp.bin.generate_text:main',
            'oir_generate_text_from_model = oireachtas_nlp.bin.generate_text_from_model:main',
        ]
    }
)
