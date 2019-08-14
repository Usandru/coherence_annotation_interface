#PATH CONSTANTS
SOURCE = "./annotation_source_data/" #the location of the text files used to generate the tasks
ORIGINALS = SOURCE + "originals/" #the location of the original text files
DATA = "./annotation_user_data/" #the location of the tasks generated for each user
DATA_META = DATA + "meta/" #the location of the meta-data associated with each user
DATA_ANNOTATIONS = DATA + "annotations/" #the location of the annotations given by each user
OUTPUT = "./output/" #location of analysis output

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

#NUMBER CONSTANTS
NUMBER_OF_FILES = 15
NUM_OF_BLOCKS = 4 #the number of blocks in total for the source dataset
BLOCK_SIZE = 33