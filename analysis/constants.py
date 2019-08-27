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
MERGED = "merged"
LEFT = "left"
RIGHT = "right"
NULL = "null"
MODE = "mode"
WEIGHT = "weight"
WEIGHT_SUM = "weight_sum"
WEIGHT_INSTANCES = "weight_instances"
BINARY_INSTANCES = "binary_instances"
NUMBER_OF_SOURCE_TEXTS = "Number_of_Texts"

#keyvalue argument string constants
TEXT = "text"
WORD_COUNT = "word count"
SENTENCES = "sentences"

#EDGELITS KW ARGS STRING CONSTATNS
AGREEMENT = "agreement"
AGREEMENT_COMPONENTS = "agreement_components"
LEFT_AUTHOR = "left_author"
RIGHT_AUTHOR = "right_author"
DIRECTION = "direction"
SLIDER_WEIGHT = "slider_weight"
SLIDER_DIRECTION = "slider_direction"
EDGELIST_MODE = "edgelist_mode"

#text ID tag strings
TAG_ORIGINAL = "ORIGINAL"

#NUMBER CONSTANTS
NUMBER_OF_FILES = 15
NUM_OF_BLOCKS = 4 #the number of blocks in total for the source dataset
BLOCK_SIZE = 33

#edgelist tuple constants
EDGE_LEFT = 0
EDGE_RIGHT = 1
EDGE_KEYVALUE = 2

#sourcetext CSV file constants
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
                                  ("1926 ORIGINAL", "1926 PRONOUN-NP-P", LEFT), #kommunerne og regionerne -> vi, the pronoun does not match the natural antecedents, and brings the speaker into the equation with no warning
                                  ("1380 ORIGINAL", "1380 PRONOUN-NP-NP", LEFT), #kommunerne -> regionerne, the following sentences refers to "kommunerne" but the difference is hard to tell
                                  ("1184 ORIGINAL", "1184 PRONOUN-NP-ADJ", LEFT), #et glimrende initiativ -> glimrende, the adjective version is awkward compared to the NP version
                                  ("2473 ORIGINAL", "2473 PRONOUN-P-NP", LEFT), #de -> kommunerne, overly explicit, the pronoun's antecedent is immediately prior so changing to the correct NP doesn't help
                                  ("1627 ORIGINAL", "1627 PRONOUN-NP-NP", NULL), #ordføreren -> Kommunerne, who is speaking becomes ambiguous, there is a slight tend to the first but it might be a wash
                                  ("1249 ORIGINAL", "1249 PRONOUN-NP-NP", LEFT), #kommuner -> lande, while plausible the second NP is only loosely related and seems unlikely
                                  ("2638 ORIGINAL", "2638 PRONOUN-O-NP", RIGHT), #Ø -> af muligheder, makes it more explicit meaning the altered version should be most plausible
                                  ("600 ORIGINAL", "600 PRONOUN-NP-O", RIGHT), #som administrativ enhed -> Ø, the NP makes the topic more specific, but without being linked to the rest the removal simplifies without notable loss
                                  ("663 ORIGINAL", "663 PRONOUN-O-NP", RIGHT), #Ø -> for regeringen, the addition contextualizes the events, but perhaps quite weakly - moreso than the above however
                                  ("3173 ORIGINAL", "3173 PRONOUN-NP-O", LEFT), #om skærpelse -> Ø, the removal obscures the topic
                                  ("713 ORIGINAL", "713 PRONOUN-P-P", NULL), #vores -> deres, extremely difficult to spot difference, the meaning changes but not the coherence
                                  ("789 ORIGINAL", "789 PRONOUN-NP-P", LEFT), #lovforslaget -> det, pronoun with no clear antecedent, disruptive
                                  ("863 ORIGINAL", "863 PRONOUN-P-P", NULL), #vi -> de, hard to spot pronoun difference, which slightly favours the original but not to any great degree
                                  ("779 ORIGINAL", "779 PRONOUN-NP-P", LEFT), #tilsynets -> deres, pronoun with no antecedent, loss of coherence
                                  ("1977 ORIGINAL", "1977 PRONOUN-P-NP", RIGHT), #det her -> lovforslaget, ambiguous pronoun made explicit
                                  ("2635 ORIGINAL", "2635 PRONOUN-P-P", LEFT), #hun -> de, hard to spot pronoun difference that clearly favours the original given the context
                                  ("2133 ORIGINAL", "2133 PRONOUN-P-NP", NULL), #vi -> borgerne, neither make much if any sense due to the inherent lack of context
                                  ("874 ORIGINAL", "874 PRONOUN-NP-NP", RIGHT)] #spørgeren -> ministeren, arguably no difference, but due to the overall context of the textset, the altered should feel more natural