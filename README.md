Oireachtas Data NLP
===================

Some natural language processing of the Dail and Seanad of individual members / political parties. Do things like see the difference between the words people/parties use along with predicting what political party a person will align with given a sample of their speech.

Dependencies
------------

Poppler - `sudo apt install libpoppler-cpp-dev`

PDFToHTML - `sudo apt install pdftohtml`

Installation
============

`pip install oireachtas-nlp`

Usage
=====

After installation run `pull_debates` for a while to get some data. Do this for as long as you want. The longer the better

Also run `pull_members` to get member data.


Features
========

Look at the help of any of the below for a better description of how to use it.

`oir_sounds_like`
This generates a classifier with which you can see what a pice of text beongs to (a member or a party)

`oir_belong`
This will go through members and determine if they speak like the party they belong to (or not and which one they do sound like they belong to).

`oir_word_usage_by`
This will show the difference in words used between members or parties.

`oir_sentiment`
This will show how positive / negative members / parties are.

`oir_lexical_diversity`
This shows how diverse the word usage is of members / parties.

`oir_lexical_difficulty`
This shows how difficult the language is of members / parties. Many methods of calculation available.

`oir_generate_text`
Generate sentences based on the content of a party / member. You can also give prefixes and have the sentence finished with generated text. TODO: With this is another command for pretrained models `oir_generate_text_from_model`
