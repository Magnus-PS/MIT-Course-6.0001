# Problem Set 4B
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

import string

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example: >>> is_word(word_list, 'bat') returns True
    Example: >>> is_word(word_list, 'asdf') returns False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list

def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

class Message(object):
    def __init__(self, text):
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)
        '''
        Initializes a Message object
                
        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''

    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        vw_copy = self.valid_words.copy()
        return vw_copy

    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.        
        
        shift (integer): the amount by which to shift every letter of the 
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        d = {} #initialize shift dictionary
        alphabet = 'abcdefghijklmnopqrstuvwxyz' #lowercase letters in alphabet

        if shift >= 0 and shift < 26:

            #below loop built with reference to: https://www.youtube.com/watch?v=JhmKrIR-ciM

            for i in range (0,26) :   #populate values string via shifted indices of keys
                    letter = alphabet[i]
                    shiftedLetter = alphabet[(i + shift) % 26]
                    d[letter] = shiftedLetter #populated dictionary

        return d

    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift        
        
        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''

        new_string = ''
        shift_dict = Message.build_shift_dict(self, shift) #store returned dictionary

        for c in self.message_text: #for every character in the message
            if c.isalpha():
                if c.isupper():
                    new_string += shift_dict[c.lower()].upper() #handle the case of uppercase input
                else:
                    new_string += shift_dict[c] #access returned dictionary values using characters of message as keys
            else: #if it's not an alphabetic symbol, just add it as is to the string
                new_string += c

        return new_string

class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object        
        
        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encryption_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)
        self.shift = shift
        self.encryption_dict = Message.build_shift_dict(self, shift)
        self.message_text_encrypted = Message.apply_shift(self, shift)

    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class
        
        Returns: self.shift
        '''
        return self.shift

    def get_encryption_dict(self):
        '''
        Used to safely access a copy self.encryption_dict outside of the class
        
        Returns: a COPY of self.encryption_dict
        '''
        ed_copy = self.encryption_dict.copy()
        return ed_copy

    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class
        
        Returns: self.message_text_encrypted
        '''
        return self.message_text_encrypted

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other 
        attributes determined by shift.        
        
        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        self.shift = shift #change self.shift
        self.encryption_dict = build_shift_dict(self, shift) #update corresponding dict
        self.message_text_encrypted = apply_shift(self, shift) #update encrypted message

class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object
                
        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value 
        for decrypting it.

        Note: if multiple shifts are equally good such that they all create 
        the maximum number of valid words, you may choose any of those shifts 
        (and their corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''

        d_shift = 0 #initialize decryption shift variable

        while d_shift < 26:
            decrypted_message = Message.apply_shift(self, d_shift) #apply shift to message
            decrypted_words = decrypted_message.split() #split the decrypted message into list of separate words
            i = 0  # initialize index_counter variable
            word_count = 0 # initialize word counter variable

            while i < len(decrypted_words): #test out each word in the list
                real_word = is_word(self.valid_words, decrypted_words[i])

                if real_word: #if the word at this index is a word, increment the word_count
                    word_count += 1
                i += 1

            if word_count == len(decrypted_words): #if the word count is equal to the length of the list, break
                break
            elif word_count > len(decrypted_words) / 2: #created to handle the story case ;)
                break
            d_shift += 1

        shift_tuple = (d_shift, decrypted_message) #store shift and message values in tuple and return that tuple

        return shift_tuple

if __name__ == '__main__':

    #TODO: WRITE YOUR TEST CASES HERE

    #    #Test Case 1 (PlaintextMessage)
    plaintext = PlaintextMessage('hello', 3)
    print('Expected Output: khoor')
    print('Actual Output:', plaintext.get_message_text_encrypted())

    #    #Test Case 2 (PlaintextMessage)
    plaintext = PlaintextMessage('Yo Matt.', 6)
    print('Expected Output: Eu Sgzz.')
    print('Actual Output:', plaintext.get_message_text_encrypted())

    #    #Test Case 1 (CiphertextMessage)
    ciphertext = CiphertextMessage('jgnnq')
    print('Expected Output:', (24, 'hello'))
    print('Actual Output:', ciphertext.decrypt_message())

    #    #Test Case 2 (CiphertextMessage)
    ciphertext = CiphertextMessage('Ef hfa!')
    print('Expected Output:', (3, 'Hi kid!'))
    print('Actual Output:', ciphertext.decrypt_message())

    #TODO: best shift value and unencrypted story

#   #Decrypt story.txt (CiphertextMessage)
    ciphertext = CiphertextMessage(get_story_string())
    print('Actual Output:', ciphertext.decrypt_message())
    # shift value : 12
    # story : 'Jack Florey is a mythical character created on the spur of a moment to help cover an insufficiently planned hack. He has been registered for classes at MIT twice before, but has reportedly never passed aclass. It has been the tradition of the residents of East Campus to become Jack Florey for a few nights each year to educate incoming students in the ways, means, and ethics of hacking.'
