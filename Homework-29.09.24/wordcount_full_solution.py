#!/usr/bin/python -tt
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

"""Wordcount exercise
Google's Python class

The main() below is already defined and complete. It calls print_words()
and print_top() functions which you write.

1. For the --count flag, implement a print_words(text) function that counts
how often each word appears in the text and prints:
word1 count1
word2 count2
...

Print the above list in order sorted by word (python will sort punctuation to
come before letters -- that's fine). Store all the words as lowercase,
so 'The' and 'the' count as the same word.

2. For the --topcount flag, implement a print_top(text) which is similar
to print_words() but which prints just the top 20 most common words sorted
so the most common word is first, then the next most common, and so on.

Use str.split() (no arguments) to split on all whitespace.

Workflow: don't build the whole program at once. Get it to an intermediate
milestone and print your data structure and sys.exit(0).
When that's working, try for the next milestone.

Optional: define a helper function to avoid code duplication inside
print_words() and print_top().

"""

import sys


# +++your code here+++
# Define print_words(text) and print_top(text) functions.
# You could write a helper utility function that reads the text
# and builds and returns a word/count dict for it.
# Then print_words() and print_top() can just call the utility function.

def count_words(filename: str) -> dict:
    word_count: dict = dict()

    with open(filename, 'r') as file:
        text = file.read()

    for word in text.split():
        if word.lower() not in word_count:
            word_count[word.lower()] = 1
        else:
            word_count[word.lower()] += 1

    return word_count


def print_words(filename: str) -> None:
    word_count: dict = count_words(filename)
    sorted_word_count_list: list[tuple] = sorted(word_count.items(), key=lambda x: x[0], reverse=False)

    # print the sorted dict
    for (word, count) in sorted_word_count_list:
        print(f'{word}: {count}')


def print_top(filename: str) -> None:
    word_count: dict = count_words(filename)
    sorted_word_count_list: list[tuple] = sorted(word_count.items(), key=lambda x: x[1], reverse=True)

    # print the sorted dict up to 20 most common words
    i: int = 0
    for (word, count) in sorted_word_count_list:
        print(f'{word}: {count}')
        i += 1
        if i >= 20:
            break


# assume the words of a large text is writen hard-coded into this file
# get input from the user, what type of sort to perform:
#    count   or   topcount
# calls the print_words() and print_top() functions which you must define.

def main():
    if len(sys.argv) != 3:
        print('Usage: python wordcount_full_solution.py {--count | --topcount} <textfile>')
    else:
        filename = sys.argv[2]
        option = sys.argv[1]
        if option == '--count':
            print_words(filename)
        elif option == '--topcount':
            print_top(filename)
        else:
            print('Invalid option')
            sys.exit(1)


if __name__ == '__main__':
    main()
