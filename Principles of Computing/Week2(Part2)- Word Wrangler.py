"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    new_list = list1[:1]
    for item in list1:
        if item != new_list[-1]:
            new_list.append(item)    
    return new_list

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    new_list = []
    idx1 = 0
    idx2 = 0
    while idx1 < len(list1) and idx2 < len(list2):
        if list1[idx1] < list2[idx2]:
            idx1 += 1
        elif list1[idx1] > list2[idx2]:
            idx2 += 1
        else:
            new_list.append(list1[idx1])
            idx1 += 1
            idx2 += 1
            
    return new_list
    #return [value for value in list1 if value in list2]

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing those elements that are in
    either list1 or list2.

    This function can be iterative.
    """   
    new_list = []
    new_list1 = list(list1)
    new_list2 = list(list2)
    while len(new_list1) > 0 and len(new_list2) > 0:       
        if new_list1[0] < new_list2[0]:
            new_list.append(new_list1[0])
            new_list1.pop(0)
        else:
            new_list.append(new_list2[0])
            new_list2.pop(0)
                   
    if len(new_list1) == 0:
        return new_list + new_list2
    elif len(new_list2) == 0:
        return new_list + new_list1
        
                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    if list1 == []:
        return []
    elif len(list1) == 1:
        return list1
    else:
        mid = len(list1) / 2
        return merge(merge_sort(list1[:mid]),merge_sort(list1[mid:]))

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    if word == '':
        return ['']
    else:
        first = word[0]
        rest = word[1:]
        temp = []
        rest_strings = gen_all_strings(rest)
        for each_string in rest_strings:
            for idx in range(len(each_string)+1):
                #aaa = []
                temp.append(each_string[:idx]+first+each_string[idx:])
        #rest_strings += aaa
        return rest_strings + temp

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
   
    url = codeskulptor.file2url(filename)
    netfile = urllib2.urlopen(url)
    return netfile.read().split('\n')
    
def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
# run()
