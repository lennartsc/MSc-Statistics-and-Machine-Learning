import text_stats
import random
import sys

# Testing terminal arguments and opening files.
if len(sys.argv) - 1 != 3:
    raise ValueError("Three arguments (file_name, starting_word, n_words) have to be provided.")
opened_files = open(sys.argv[1], encoding = "utf8") # If file not found, error will be returned.

# Setting print location for print-function.
print_location = text_stats.get_print_location(opened_files)

# Performing process of collecting information about characters and words.
dics = text_stats.create_collection(opened_files, "[^a-zA-Z]")
word_dict = dics[0]

# Initializing starting_word, number of words and text.
current_word = sys.argv[2]
n_words = sys.argv[3]
text = current_word

# Creating message.
'''word_dict stores for every key (therefore for every word) the number of appearences
in the first position and all followed words appended in the other positions
(in all other positions except the first position). Consequently, if the word
'am' follows the word 'I' 20 times within the text, then the string 'am' is
appended 20 times to the dictionary-entry for key 'I'. Ignoring the first position
of the values of every key, the next word will be chosen with its probability by
just randomly choosing one of the appended words. If for example there are in total
100 words appended to the dictionary-entry of the key 'I', then, just randomly choosing
one of the values(appended words), the word 'am' will be chosen with a probability of 20%.'''

## Iterating "number of words - times".
for i in range(int(n_words)-1):
    # If no successors of current_word: printing message.
    if len(word_dict[current_word]) == 1:
        print("")
        print("Result of Text generator: ")
        print(text)
        break
    # Generating random number which will be the index of dictionary-entry for current_word.
        # Random number will be >= 1 (Because first element of dictionary-entry is not a word but number of appearences.).
        # Random number will be < length(dictionary-entry).
    random_number = (random.randint(1, len(word_dict[current_word])-1))
    # The value belonging to the identied index will be chosen as next current_word.
    current_word = word_dict[current_word][random_number]
    # Current_word will be added to message.
    text = text + " " + current_word

# Printing generated text.
print("")
print("Result of text generator for " + sys.argv[1] + " (" + n_words + " words): ")
print(text)
