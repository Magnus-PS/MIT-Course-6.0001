# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : <your name>
# Collaborators : <your collaborators>
# Time spent    : <total time>

import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10, '*': 0
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters, 
    or the empty string "". You may not assume that the string will only contain 
    lowercase letters, so you will have to handle uppercase and mixed case strings 
    appropriately. 

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """
    #initialize variables for word score, lower case word, and word length
    word_score_c1 = 0 #variable for tracking first component of word score
    word_score_c2 = 0 #variable for tracking second component of word score
    word_score = 0 #variable for tracking total word score

    i = 0 #counter for iterating through word

    word = word.lower() #convert word to lowercase version of itself

    #first off: calculate scrabble letter values for each character in word
    #access values of SCRABBLE_LETTER_VALUES dictionary by using the character of word[i] as the key
    #iterate the counter to go through each character of word

    for c in word:
            word_score_c1 += SCRABBLE_LETTER_VALUES[c] #access Dictionary value using character as key

    #once we exit this loop word_score_c1 should carry the sum of the points for the letters in word
    #now we compute the second component word_score_c2

    word_score_c2 += 7 * len(word) - 3 * (n - len(word))

    #if word_score_c2 is less than one, set the value to 1
    if word_score_c2 < 1:
        word_score_c2 = 1

    #add the components together and return this value
    word_score = word_score_c1 * word_score_c2
    return word_score

#
# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    
    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter, end=' ')      # print all on the same line
    print()                              # print an empty line

#
# Make sure you understand how this function works and what it does!
# You will need to modify this for Problem #4.
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    
    hand={}
    num_vowels = int(math.ceil(n / 3))

    for i in range(num_vowels):
        if i == 0:
            x = '*'
        else:
            x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    
    for i in range(num_vowels, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
    
    return hand

#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured). 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    new_hand = hand.copy()   #create shallow copy of dictionary
    word = word.lower()     #make word lowercase

    #modify this new hand based on the characters in word
    for x in word:
        if x in new_hand:
            new_hand[x] -= 1

            if new_hand[x] == -1:   #handle the case of 'going negative'
                new_hand[x] = 0

    return new_hand

#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
   
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """

    valid_word = False  #initialize boolean variable
    valid_counter = 0
    new_hand = hand.copy()  # create shallow copy of dictionary
    word = word.lower()  # make word lowercase
    new_word = word #create another string instance for replacability
    i = word.find('*') #index of '*'

    if i > 0: #if the word guessed contains a '*'
        for v in VOWELS: #cycle through each vowel
            new_word = word.replace('*', v) #replace said letter with the vowel
            if new_word in word_list: #check whether the result is a word in word_list
                new_word = word.replace(v, '*')
                for x in new_word:
                    if x in new_hand and new_hand[x] >= 1:

                        new_hand[x] -= 1
                        valid_counter += 1

                        if valid_counter == len(word):
                            valid_word = True

    elif word in word_list: #if the word guessed does not contain a '*' and is a valid word

        for x in word:
            if x in new_hand and new_hand[x] >= 1:

                new_hand[x] -= 1
                valid_counter += 1

                if valid_counter == len(word):
                    valid_word = True

    return valid_word

#
# Problem #5: Playing a hand
#
def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    hand_length = 0

    for value in hand.values():     #add up the values within the hand --> number of letters
        hand_length += value

    return hand_length


def play_hand(hand, word_list):

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two 
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
      
    """
    word_score = 0 # Keep track of the score for each word
    total_score = 0 # Keep track of the total score

    while calculate_handlen(hand) > 0: #
        print('Current hand :', end = ' ')
        display_hand(hand)
        word = input('Enter word or "!!" to indicate that you are finished: \n') # Ask user for input

        if word == '!!': # If the input is two exclamation points:
            break # End the game (break out of the loop)

        else: # Otherwise (the input is not two exclamation points):

            if is_valid_word(word, hand, word_list): # If the word is valid:
                word_score = get_word_score(word, 7) #update word score and total score
                total_score += word_score
                # Tell the user how many points the word earned, and the updated total score
                print(word + ' earned ' + str(word_score) + ' points. Total: ' + str(total_score) + ' points')
                print()

            else: # Otherwise (the word is not valid):
                print('That is not a valid word. Please choose another word.') # Reject invalid word (print a message)
                print()
            # update the user's hand by removing the letters of their inputted word
            hand = update_hand(hand,word)

    # Game is over (user entered '!!' or ran out of letters),
    # so tell user the total score
    print('Game is over. User entered "!!" or ran out of letters.')
    print('Total score : ' + str(total_score) + ' points')

    # Return the total score as result of function
    return total_score


#
# Problem #6: Playing a game
# 


#
# procedure you will use to substitute a letter in a hand
#

def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.
    
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """

    new_hand = hand.copy()  # create shallow copy of dictionary
    ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
    new_letter = ''

    if letter in hand.keys(): #if letter is in hand, mutate the hand

        for x in hand.keys():
            ALPHABET.replace(x, '') #remove letters in hand from possible replacements

        new_letter = random.choice(ALPHABET) #randomly generate new letter from remaining field of letters
        new_hand[new_letter] = new_hand.pop(letter) #replace the old letter with the new letter in the hand

    return new_hand
       
    
def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand.  This can only be done once 
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """
    series_score = 0 #track score for series
    HAND_SIZE = 6
    hand_number = input('Enter total number of hands: \n')  # Ask user to play a series of hands
    sub_count = 0 #counter to limit substitutions to 1
    replay_count = 0 #counter to limit replays to 1
    score1 = 0 #initial score count variable for if we don't replay hand
    score2 = 0 #initial score count variable for if we do replay hand
    x = 0

    while x < int(hand_number):

        hand = deal_hand(HAND_SIZE) #make call to deal_hand(n) to generate hand for user
        print('Current hand :', end=' ')
        display_hand(hand)

        if sub_count == 0: #if the user hasn't substituted a letter before
            response = input('Would you like to substitute a letter? \n')  # Ask user for input
            letter = input('Which letter would you like to replace: \n') #ask user to input sub letter
            new_hand = substitute_hand(hand, letter) #make call to substitute hand and update play hand
            sub_count += 1
        else: #otherwise just copy the hand over so that I'm using the same dictionary variable
            new_hand = hand.copy()

        score1 = play_hand(new_hand, word_list) #play out the hand and store the total score in series_score

        if replay_count == 0:
            replay = input('Would you like to replay the hand? \n') #ask user whether they'd like to replay the hand

            if replay == 'yes':
                score2 = play_hand(new_hand, word_list)
                replay_count += 1

        if score1 >= score2: #accumulate total score for hands played
            series_score += score1
        else:
            series_score += score2

        x += 1 #increment the counter after playing each hand

    print('Total score over all hands: ' + str(series_score))

    return series_score

#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
