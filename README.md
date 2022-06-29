Oireachtas Data NLP
===================

Some natural language processing of the Dail and Seanad of individual members / political parties. Do things like see the difference between the words people/parties use along with predicting what political party a person will align with given a sample of their speech.

Dependencies
------------

Poppler - `sudo apt install libpoppler-cpp-dev`

PDFToHTML - `sudo apt install pdftohtml`

Usage
=====

After installation run `pull_debates` for a while to get some data. Do thiis for as long as you want. The longer the better


Feature: Sounds Like
====================

Command: `oir_sounds_like`

This generates a classifier with which you can see who sounds like who.

By specifying `--group-by member` you can generate a classifier so you can predict who would have said the body of text you reference in `--compare-file {path_to_file}`

TODO (need to clean up member -> party matching): By specifying `--group-by party` you can generate a classifier so you can predict what party would have said the body of text you reference in `--compare-file {path_to_file}`

TODO: By specifying `--belongs-to member-pid` you can generate a classifier so you can predict what party the member specified speaks like they belong to. member-pid is something like #FirstnameLastname


Feature: Word Usage By
======================

Command: `oir_word_usage_by`

By specifying `--group-by member` you can see what the difference is between all or some members (see --only-groups). This will show what topics are used more by some members and by how much.

TODO (need to clean up member -> party matching): By specifying `--group-by party` you can see what the difference is between all or some parties (see --only-groups). This will show what topics are used more by some parties and by how much.
