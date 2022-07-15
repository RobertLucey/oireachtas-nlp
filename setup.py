from setuptools import (
    find_packages,
    setup
)

INSTALL_REQUIRES = (
    'oireachtas_data',
    'gensim',
    'nltk',
    'cached_property',
    'sklearn_pandas',
    'tqdm'
)

setup(
    name='oireachtas-nlp',
    version='0.0.1',
    python_requires='>=3.6',
    description='',
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
            # TODO: reading level
        ]
    }
)
