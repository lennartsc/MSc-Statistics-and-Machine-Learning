#!/usr/bin/env python3

## Importing modules.
import sys
import os
import string
import operator
import re
import collections

# Testing terminal arguments and opening files.
def open_files(command_args):
    # Printing error message if no file is provided.
    if len(command_args) - 1 == 0:
        raise ValueError(".txt-file from home directory has to be provided.")
    # Opening provided files.
    if command_args[0] == "text_stats.py":
        if len(command_args) - 1 == 1:
            data = open(command_args[1], encoding = "utf8") # If file not found, error will be returned.
            return data
        if len(command_args) - 1 == 2:
            data = open(command_args[1], encoding = "utf8") # If file not found, error will be returned.
            new_file = open(command_args[2], 'w')
            return data, new_file
    ## If used as import in "generate_text.py", always open sys.argv[0].
    elif command_args[0] == "generate_text.py":
        data = open(command_args[1], encoding = "utf8") # If file not found, error will be returned.
        return data
if __name__ == '__main__': # If-condition prevents running this code if file will be imported.
    opened_files = open_files(sys.argv)

# Setting print location for print-function.
## If second argument provided by user, printout should be saved in provided file.
## Otherwise, results are just printed in terminal itself.
def get_print_location(opened_files):
    if not isinstance(opened_files, tuple): # If only one file has been opened:
        return sys.stdout # Printout at terminal itself.
    else: # If two files have been opened:
        return opened_files[1] # Printout at second provided file.

if __name__ == '__main__': # If-condition prevents running this code if file will be imported.
    print_location = get_print_location(opened_files)

# Performing process of collecting information about characters and words.
def create_collection(opened_files, valid_chars_regex):
    # Setting up process of collecting information about characters and words.
    ## Extracting data from opened_files.
    if not isinstance(opened_files, tuple):
        data = opened_files
    else:
        data = opened_files[0]
    ## Creating empty dictionary for collection of characters.
    char_dict = {}
    ## Creating empty dictionary for collection of words.
    word_dict = {}
    ## Creating empty string to track previous word.
    previous_word = ""
    ## Specifying allowed characters.
    regex = re.compile(valid_chars_regex)
    # Looping over each line of data and storing collected word/char information.
    for line in data:
        words = line.split()
        for word in words:
            # Filtering out non-alphabetical elements. Emtpy strings will not be considered as a word.
            word = regex.sub("", word)
            if word == "":
                continue
            # Lowering all characters within the word.
            word = word.lower()
            # Filling word dictionary.
            # Increasing number of word occurence at first position of dictionary word entry.
            if not word in word_dict:
                word_dict[word] = [1]
            else:
                word_dict[word][0] += 1
            # Appending word to dictionary entry of previous occured word.
            if previous_word != "":
                word_dict[previous_word].append(word)
            # Saving word as last word.
            previous_word = word
            # Filling character dictionary.
            chars = list(word)
            for char in chars:
                if not char in char_dict:
                    char_dict[char] = 1
                else:
                    char_dict[char] += 1
    # Returning collections.
    return word_dict, char_dict

if __name__ == '__main__': # If-condition prevents running this code if file will be imported.
    dics = create_collection(opened_files, "[^a-zA-Z]")

# Aggregating collected information.
def print_results(dics, print_location):
    # Extracting word and chat dictionaries from dics.
    word_dict = dics[0]
    char_dict = dics[1]

    # Printing ordered frequency table for alphabetic letters.
    print("Frequences of alphabetic letters, ordered from the most common to the least:", file = print_location)
    for char in sorted(char_dict, key = char_dict.get, reverse = True):
        print(char, char_dict[char], file = print_location)

    # Printing number of words.
    print("", file = print_location)
    print("Number of words in total:", file = print_location)
    n_words = 0
    for word in word_dict.items():
        n_words += word[1][0]
    print(n_words, file = print_location)

    # Printing number of unique words.
    print("", file = print_location)
    print("Number of unique words in total:", file = print_location)
    print(len(word_dict), file = print_location)

    # Printing five most frequent words and their frequencies.
    print("", file = print_location)
    print("Five most frequent words with frequency and words that most commonly follow them:", file = print_location)
    most_frequent_names = []
    for key, items in word_dict.items():
        if len(most_frequent_names) < 5:
            most_frequent_names.append(key)
        elif word_dict[key][0] > word_dict[most_frequent_names[0]][0]:
            most_frequent_names[4] = most_frequent_names[3]
            most_frequent_names[3] = most_frequent_names[2]
            most_frequent_names[2] = most_frequent_names[1]
            most_frequent_names[1] = most_frequent_names[0]
            most_frequent_names[0] = key
        elif word_dict[key][0] > word_dict[most_frequent_names[1]][0]:
            most_frequent_names[4] = most_frequent_names[3]
            most_frequent_names[3] = most_frequent_names[2]
            most_frequent_names[2] = most_frequent_names[1]
            most_frequent_names[1] = key
        elif word_dict[key][0] > word_dict[most_frequent_names[2]][0]:
            most_frequent_names[4] = most_frequent_names[3]
            most_frequent_names[3] = most_frequent_names[2]
            most_frequent_names[2] = key
        elif word_dict[key][0] > word_dict[most_frequent_names[3]][0]:
            most_frequent_names[4] = most_frequent_names[3]
            most_frequent_names[3] = key
        elif word_dict[key][0] > word_dict[most_frequent_names[4]][0]:
            most_frequent_names[4] = key
    for word in most_frequent_names:
        words_followed = collections.Counter(word_dict[word]).most_common(3)
        print(word + " (" + str(word_dict[word][0]) + " occurences)", file = print_location)
        print("-- " + str(words_followed[0][0]) + ", " + str(words_followed[0][1]), file = print_location)
        print("-- " + str(words_followed[1][0]) + ", " + str(words_followed[1][1]), file = print_location)
        print("-- " + str(words_followed[2][0]) + ", " + str(words_followed[2][1]), file = print_location)

if __name__ == '__main__': # If-condition prevents running this code if file will be imported.
    print_results(dics, print_location)
