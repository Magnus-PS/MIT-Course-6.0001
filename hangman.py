# Problem Set 2, hangman.py
# Name: 
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string
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
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"

    #initialize character_count variable to track how many times letters_guessed appears in secret_word
    character_count = 0
    #for each character in secret_word check the character v. letters_guessed
    #if the character appears, increment the counter
    #if not, do nothing
    for c in secret_word:
        if c in letters_guessed:
            character_count += 1

    #if character_count is equal to the length of the secret_word, we've guessed all the letters / return True
    #if not, we haven't guessed all the letters and return False
    if character_count == len(secret_word):
        return True
    else:
        return False

def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"

    #initialize empty string to track character guesses
    secret_word_guessed = ''
    #for each character in secret_word check the character v. letters_guessed
    #if the character appears in letters_guessed, it's added to secret word
    #if not, add an underscore with a space
    for c in secret_word:
        if c in letters_guessed:
            secret_word_guessed += c
        else:
            secret_word_guessed += '_ '
    #return the tracker String
    return secret_word_guessed


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    #initialize empty string to store all remaining letters
    available_letters = ''
    #for every letter in the alphabet, check whether that character has been guessed
    #if not, add it to available letters
    #if so, skip it
    for c in string.ascii_lowercase:
        if c not in letters_guessed:
            available_letters += c

    return available_letters

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.

    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    # initialize counter variables and empty list
    guess_number = 6
    warnings = 3
    letters_guessed = ['']

    #welcome the User to the game and make them aware of how long the word is and how many warnings they have.
    print('Welcome to the game Hangman!')
    print('I am thinking of a word that is ' + str(len(secret_word)) + ' letters long.')
    print('You have ' + str(warnings) + ' warnings left.')

    #as long as there are guesses remaining and the User has not guessed the word, keep looping
    while guess_number > 0:

        #provide a divider between text and flash the user with remaining guesses and letters
        print('---------------------')
        print('You have ' + str(guess_number) + ' guesses left.')
        print('Available letters: ' + get_available_letters(letters_guessed))

        #USER INPUT
        new_letter = input('Please guess a letter: \n')

        #if this input is alphabetical, make it lowercase and ...
        if new_letter.isalpha():
            new_letter = new_letter.lower()

            #if it's been guessed before, subtract and warning / guess and notify the User
            if new_letter in letters_guessed:
                if warnings > 0:
                    warnings -= 1
                    print("Oops! You've already guessed that letter. You now have " + str(warnings) + " warning(s): " + get_guessed_word(secret_word, letters_guessed))

                else:
                    guess_number -= 1
                    print("Oops! You've already guessed that letter. You now have " + str(
                        guess_number) + " guess(es): " + get_guessed_word(secret_word, letters_guessed))
            else:
                #otherwise, append the new letter to the letters_guessed list
                letters_guessed.append(new_letter)

                #if it's in our secret word, inform the User of their successful guess
                if new_letter in secret_word:
                    print('Good guess: ' + get_guessed_word(secret_word, letters_guessed))
                else:
                    #if a vowel was mis-guessed, subtract 2 guesses (1 is subtracted later)
                    if new_letter == 'a' or new_letter == 'e' or new_letter == 'i' or new_letter == 'o' or new_letter == 'u':
                        if guess_number > 1:
                            guess_number -= 1
                    #when the letter guessed is not in secret word, inform the User of their unsuccessful guess
                    print('Oops! That letter is not in my word: ' + get_guessed_word(secret_word, letters_guessed))

                #if the User's guessed the secret word, congratulate them, tell them their total score and break loop
                if is_word_guessed(secret_word, letters_guessed) == True:
                    #the total score is the number of remaining guesses multiplied by the number of unique characters
                    #hence the use of set() and then len() functions
                    total_score = guess_number * len(set(secret_word))
                    print('Congratulations! You won.')
                    print('Your total score for this game is: ' + str(total_score))
                    break

                #decrement the guess counter
                guess_number -= 1

        #entered character is not alpha, decrement guess / warning and notify User of invalid entry
        else:
            if warnings > 0:
                warnings -= 1
                print('Oops! That is not a valid letter. You have ' + str(warnings) + ' warning(s) left.: ' + get_guessed_word(secret_word, letters_guessed))

            else:
                guess_number -= 1
                print('Oops! That is not a valid letter. You have ' + str(guess_number) + ' guess(es) left.: ' + get_guessed_word(secret_word, letters_guessed))

    #if the User is out of guesses and they have not guessed the secret word, notify them that the game is over and flash the secret_word
    if guess_number == 0 and is_word_guessed(secret_word, letters_guessed) == False:
        print('Sorry, you have used all your guesses. Game over. The word was: ' + str(secret_word))

# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)

def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    # first check that the length of these words is the same
    truth_tracker = False
    # remove spaces from my_word to ensure lengths are consistent
    new_my_word = my_word.translate({ord(c): None for c in string.whitespace})
    # if my_word and other_word line up, change the value of truth_tracker, otherwise return False
    # first check the length
    if len(new_my_word) == len(other_word):
        i = 0
        # then iterate over the entire length of the word
        while i < len(new_my_word):
            # if the characters of my_word and other_word in the i position match, or it's a '_'
            #for some reason, it doesn't seem to catch the last letter
            # increment the counter, otherwise break the loop
            if new_my_word[i] == other_word[i] or new_my_word[i] == '_':
                i += 1
            # if these characters do not line up, break the loop
            else:
                break
            # if the last characters in each word lined up, update truth_tracker to reflect True and increment counter to exit loop
            if i == len(new_my_word):
                truth_tracker = True

    return truth_tracker

def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    #initialize empty string
    s = ''
    i = 0
    while i < len(wordlist):
        #if my_word matches the string in wordlist, add the word to the end of the empty string
        if match_with_gaps(my_word, wordlist[i]) :
            s += wordlist[i] + ' '
        #if we're on the last entry, increment the counter so we can exit the loop
        if i == len(wordlist) - 1:
            i += 1
        i += 1
    #if s is an empty string / no matches were found, let the User know
    if s == '':
        s = 'No matches found.'
    #once we've iterated over the list, print what we've found
    print(s)



def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    # initialize counter variables and empty list
    guess_number = 6
    warnings = 3
    letters_guessed = ['']

    # welcome the User to the game and make them aware of how long the word is and how many warnings they have.
    print('Welcome to the game Hangman!')
    print('I am thinking of a word that is ' + str(len(secret_word)) + ' letters long.')
    print('You have ' + str(warnings) + ' warnings left.')

    # as long as there are guesses remaining and the User has not guessed the word, keep looping
    while guess_number > 0:

        # provide a divider between text and flash the user with remaining guesses and letters
        print('---------------------')
        print('You have ' + str(guess_number) + ' guesses left.')
        print('Available letters: ' + get_available_letters(letters_guessed))

        # USER INPUT
        new_letter = input('Please guess a letter: \n')

        # if this input is alphabetical, make it lowercase and ...
        if new_letter.isalpha():
            new_letter = new_letter.lower()

            # if it's been guessed before, subtract and warning / guess and notify the User
            if new_letter in letters_guessed:
                if warnings > 0:
                    warnings -= 1
                    print("Oops! You've already guessed that letter. You now have " + str(
                        warnings) + " warning(s): " + get_guessed_word(secret_word, letters_guessed))

                else:
                    guess_number -= 1
                    print("Oops! You've already guessed that letter. You now have " + str(
                        guess_number) + " guess(es): " + get_guessed_word(secret_word, letters_guessed))
            else:
                # otherwise, append the new letter to the letters_guessed list
                letters_guessed.append(new_letter)

                # if it's in our secret word, inform the User of their successful guess
                if new_letter in secret_word:
                    print('Good guess: ' + get_guessed_word(secret_word, letters_guessed))
                else:
                    # if a vowel was mis-guessed, subtract 2 guesses (1 is subtracted later)
                    if new_letter == 'a' or new_letter == 'e' or new_letter == 'i' or new_letter == 'o' or new_letter == 'u':
                        if guess_number > 1:
                            guess_number -= 1
                    # when the letter guessed is not in secret word, inform the User of their unsuccessful guess
                    print('Oops! That letter is not in my word: ' + get_guessed_word(secret_word, letters_guessed))

                # if the User's guessed the secret word, congratulate them, tell them their total score and break loop
                if is_word_guessed(secret_word, letters_guessed) == True:
                    # the total score is the number of remaining guesses multiplied by the number of unique characters
                    # hence the use of set() and then len() functions
                    total_score = guess_number * len(set(secret_word))
                    print('Congratulations! You won.')
                    print('Your total score for this game is: ' + str(total_score))
                    break

                # decrement the guess counter
                guess_number -= 1

        #handle the special case where the user enters asterisk
        elif new_letter == '*':
            show_possible_matches(get_guessed_word(secret_word, letters_guessed))

        # entered character is not alpha, decrement guess / warning and notify User of invalid entry
        else:
            if warnings > 0:
                warnings -= 1
                print('Oops! That is not a valid letter. You have ' + str(
                    warnings) + ' warning(s) left.: ' + get_guessed_word(secret_word, letters_guessed))

            else:
                guess_number -= 1
                print('Oops! That is not a valid letter. You have ' + str(
                    guess_number) + ' guess(es) left.: ' + get_guessed_word(secret_word, letters_guessed))

    # if the User is out of guesses and they have not guessed the secret word, notify them that the game is over and flash the secret_word
    if guess_number == 0 and is_word_guessed(secret_word, letters_guessed) == False:
        print('Sorry, you have used all your guesses. Game over. The word was: ' + str(secret_word))



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.

    #secret_word = 'doorjam'  # manual setting of secret_word for testing purposes. REMOVE once ready.
    #secret_word = choose_word(wordlist)
    #hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines.
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
