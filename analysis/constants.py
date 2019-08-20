#PATH CONSTANTS
SOURCE = "./annotation_source_data/" #the location of the text files used to generate the tasks
ORIGINALS = SOURCE + "originals/" #the location of the original text files
ORIGINALS_CONFIG = ORIGINALS + "config.json"
DATA = "./annotation_user_data/" #the location of the tasks generated for each user
DATA_META = DATA + "meta/" #the location of the meta-data associated with each user
DATA_ANNOTATIONS = DATA + "annotations/" #the location of the annotations given by each user
OUTPUT = "./output/" #location of analysis output
GENERAL_OUTPUT = OUTPUT + "general_data_output.txt"
TEXT_TYPES_OUTPUT = OUTPUT + "text_types.txt"

#STRING CONSTANTS
SLIDER = "slider"
BINARY = "binary"
LEFT = "left"
RIGHT = "right"
NULL = "null"
MODE = "mode"
WEIGHT = "weight"
WEIGHT_SUM = "weight_sum"
WEIGHT_INSTANCES = "weight_instances"
NUMBER_OF_SOURCE_TEXTS = "Number_of_Texts"

TEXT = "text"
WORD_COUNT = "word count"
SENTENCES = "sentences"

#NUMBER CONSTANTS
NUMBER_OF_FILES = 15
NUM_OF_BLOCKS = 4 #the number of blocks in total for the source dataset
BLOCK_SIZE = 33

CSV_TIME = 0
CSV_NAME = 1
CSV_TEXT = 2
CSV_WORDCOUNT = 3
CSV_ORG_FILE = 4
CSV_TAG = 5
CSV_ID = 6

#LIST CONSTANTS
OUTPUT_PATHS = [GENERAL_OUTPUT, TEXT_TYPES_OUTPUT]
PUNCTUATION = [",", ".", "?", "!"] #partial, based on most common sentence boundary markers
CONJUNCTIONS = ["og", "men", "eller", "at", "da", "fordi", "hvis", "når"] #partial, based on website lists
# the following were harvested from the type-list by hand
PURE_PRONOUNS = ["han", "hun", "jeg", "vi", "sig", "noget" "andre", "nogle", "dem", "mig", "vores", "deres", "mit", "sin"]
DET_PRON_LIST = ["den", "de", "en", "det", "et"] #can't be used for simple pron-checking due to also working as DETs
PROPER_NOUNS = ["ordføreren", "kommunerne", "borgerne", "enhedslisten", "enhedslistens", "regeringen", "regeringens",
                "ministeren", "alternativet", "danmark", "regionerne", "vikingeskibsmuseet", "grønlands", "venstres",
                "eus", "sverige", "norge", "kystdirektoratet", "eboks", "nemid", "ordførerens", "christiansborg", 
                "enhedslistens", "europa"]
MW_PROPER_NOUNS = ["liberal alliance", "liberal alliances", "dansk folkeparti", "ida auken", "folketingets talerstol",
                  "radikale venstre", "statens kunstfond", "pernille skipper", "mogens jensen", "jane heitmann", "isil"
                  "christian", "lisbeth bech poulsen", "jens joel", "joachim b. olsen", "dansk folkepartis", "karsten hønge",
                  "karina adsbøl"]
# necessary to deal with cases where punctuation is used for more than delimiting sentences
ABBREVIATIONS = ["kl.", "b.", "pct.", "..."]

EXPECTED_MINIMAL_PAIR_OUTCOMES = [("3237 ORIGINAL", "3237 PRONOUN-NP-P", LEFT), #kulegravningen -> han, becomes inconsistent with later sentences
                                  ("707 ORIGINAL", "707 PRONOUN-NP-P", LEFT), #de regler og vejledninger -> det, becomes more ambiguous but not that much
                                  ("2015 ORIGINAL", "2015 PRONOUN-NP-O", LEFT), #på finansloven -> Ø, slight increase in confusion due to missing word
                                  ("120 ORIGINAL", "120 PRONOUN-P-P", LEFT), #der -> hun (+verb agreement), the difference is ambiguous but RIGHT implies some unnamed actor
                                  ("131 ORIGINAL", "131 PRONOUN-P-NP", NULL), #vi -> ordføreren, probably no agreement, simply different sentence meanings
                                  ("3116 ORIGINAL", "3116 PRONOUN-NP-P", LEFT), #enhedslistens ordfører -> dem, large gap between pronoun and antecedent, likely less coherent
                                  ("1926 ORIGINAL", "1926 PRONOUN-NP-P", ),
                                  ("", "", ),
                                  ("", "", ),
                                  ("", "", ),
                                  ("", "", ),
                                  ("", "", ),
                                  ("", "", ),
                                  ("", "", ),
                                  ("", "", )]