### build a sourcetexts object by reading the sourcetext folder path and constructing a dict of dicts
### keyed by text id, and then trait
### add in functions for passing lists of text pairs and edge directions and returning analysis on this
### make the object saveable?

# TRAITS
# word count
# "sentences" == number of punctuation marks
# word types
# number of pronouns (need a list - generate a list of all word types of the whole set of texts)
# number of conjunctions (need a list)
# (if possible) number of proper nouns
# author (this is more complex to handle)
# 

import constants

class sourcetexts:

    def __init__(self, some_path):
        self.main = "unfinished"