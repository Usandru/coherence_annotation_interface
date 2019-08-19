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
PUNCTUATION = [",", ".", "?", "!"]
PURE_PRONOUNS = ["han", "hun", "jeg", "vi", "sig", "noget" "andre", "nogle", "dem", "mig", "vores", "deres", "mit", "sin"]
CONJUNCTIONS = []
DET_PRON_LIST = ["den", "de", "en", "det", "et"] #can't be used for simple pron-checking due to also working as DETs
PROPER_NOUNS = ["ordføreren", "kommunerne", "borgerne", "enhedslisten", "enhedslistens", "regeringen", "regeringens",
                "ministeren", "alternativet", "danmark", "regionerne", "vikingeskibsmuseet", "grønlands", "venstres",
                "eus", "sverige", "norge", "kystdirektoratet", "eboks", "nemid", "ordførerens"]
MULTI_WORD_PEOPLE = ["liberal alliance", "liberal alliances", "dansk folkeparti", "ida auken", "folketingets talerstol"]
ABBREVIATIONS = ["kl.", ]

#mogens, jensen, jane, heitmann, isil, christian