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

def count_words(text) -> dict:
    word_count: dict = dict()
    for word in text.split():
        if word.lower() not in word_count:
            word_count[word.lower()] = 1
        else:
            word_count[word.lower()] += 1

    return word_count


def print_words(text) -> None:
    word_count: dict = count_words(text)
    words: list = list(word_count.keys())
    words.sort()
    sorted_word_count: dict = {word: word_count[word] for word in words}

    # print the sorted dict
    for (word, count) in sorted_word_count.items():
        print(f'{word}: {count}')


def print_top(text) -> None:
    word_count: dict = count_words(text)
    sorted_word_count_list: list[tuple] = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
    sorted_word_count: dict = {}
    for (word, count) in sorted_word_count_list:
        sorted_word_count[word] = count

    # print the sorted dict up to 20 most common words
    i: int = 0
    for (word, count) in sorted_word_count.items():
        print(f'{word}: {count}')
        i += 1
        if i >= 20:
            break


# assume the words of a large text is writen hard-coded into this file
# get input from the user, what type of sort to perform:
#    count   or   topcount
# calls the print_words() and print_top() functions which you must define.

def main():
    global some_text
  
    option = input("Enter sort type [count | topcount]:")
  
    if option == 'count':
        print_words(some_text)
    elif option == 'topcount':
        print_top(some_text)
    else:
        print('unknown option: ' + option)
        sys.exit(1)


some_text = """
Alice's Adventures in Wonderland

                ALICE'S ADVENTURES IN WONDERLAND

                          Lewis Carroll

               THE MILLENNIUM FULCRUM EDITION 3.0




                            CHAPTER I

                      Down the Rabbit-Hole


  Alice was beginning to get very tired of sitting by her sister
on the bank, and of having nothing to do:  once or twice she had
peeped into the book her sister was reading, but it had no
pictures or conversations in it, `and what is the use of a book,'
thought Alice `without pictures or conversation?'

  So she was considering in her own mind (as well as she could,
for the hot day made her feel very sleepy and stupid), whether
the pleasure of making a daisy-chain would be worth the trouble
of getting up and picking the daisies, when suddenly a White
Rabbit with pink eyes ran close by her.

  There was nothing so VERY remarkable in that; nor did Alice
think it so VERY much out of the way to hear the Rabbit say to
itself, `Oh dear!  Oh dear!  I shall be late!'  (when she thought
it over afterwards, it occurred to her that she ought to have
wondered at this, but at the time it all seemed quite natural);
but when the Rabbit actually TOOK A WATCH OUT OF ITS WAISTCOAT-
POCKET, and looked at it, and then hurried on, Alice started to
her feet, for it flashed across her mind that she had never
before seen a rabbit with either a waistcoat-pocket, or a watch to
take out of it, and burning with curiosity, she ran across the
field after it, and fortunately was just in time to see it pop
down a large rabbit-hole under the hedge.
"""


if __name__ == '__main__':
    main()
