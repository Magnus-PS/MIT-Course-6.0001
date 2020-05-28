# Problem Set 4C
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

### HELPER CODE ###
from ps4.ps4a import get_permutations


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

    Example: >>> is_word(word_list, 'bat') returns True >>> is_word(word_list, 'asdf') returns False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list


### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

# you may find these constants helpful
VOWELS_LOWER = 'aeiou'
VOWELS_UPPER = 'AEIOU'
CONSONANTS_LOWER = 'bcdfghjklmnpqrstvwxyz'
CONSONANTS_UPPER = 'BCDFGHJKLMNPQRSTVWXYZ'

class SubMessage(object):
    def __init__(self, text):
        '''
        Initializes a SubMessage object
                
        text (string): the message's text

        A SubMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)
    
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
                
    def build_transpose_dict(self, vowels_permutation):
        '''
        vowels_permutation (string): a string containing a permutation of vowels (a, e, i, o, u)
        
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to an
        uppercase and lowercase letter, respectively. Vowels are shuffled 
        according to vowels_permutation. The first letter in vowels_permutation 
        corresponds to a, the second to e, and so on in the order a, e, i, o, u.
        The consonants remain the same. The dictionary should have 52 
        keys of all the uppercase letters and all the lowercase letters.

        Example: When input "eaiuo":
        Mapping is a->e, e->a, i->i, o->u, u->o
        and "Hello World!" maps to "Hallu Wurld!"

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        d = {} #initialize dictionary

        for i in range (0,52):   #populate key-value pairing for lower case vowels
            if i < 5: #index 0 to 4: lowercase vowels
                d[VOWELS_LOWER[i]] = vowels_permutation[i] #populate d with lowercase vowel permutations

            elif i >= 5 and i < 26: #index 5 to 25: lowercase consonants
                d[CONSONANTS_LOWER[i-5]] = CONSONANTS_LOWER[i-5] #populate d with lowercase consonants

            elif i >= 26 and i < 31: #index 26 to 30: uppercase vowels
                d[VOWELS_UPPER[i-26]] = vowels_permutation[i-26].upper() #populate d with uppercase vowels

            else: #index 31 to 51: uppercase consonants
                d[CONSONANTS_UPPER[i-31]] = CONSONANTS_UPPER[i-31] #populate d with uppercase consonants

        return d #return mapped dictionary
    
    def apply_transpose(self, transpose_dict):
        '''
        transpose_dict (dict): a transpose dictionary
        
        Returns: an encrypted version of the message text, based 
        on the dictionary
        '''
        encrypted_message = ''

        for c in SubMessage.get_message_text(self): #for every character in the message
            if c.isalpha():
                encrypted_message += transpose_dict[c] #pass key (character in string) to dictionary for corresponding value
            else: #if it's not an alphabetic symbol, just add it as is to the string
                encrypted_message += c

        return encrypted_message
        
class EncryptedSubMessage(SubMessage):
    def __init__(self, text):
        '''
        Initializes an EncryptedSubMessage object

        text (string): the encrypted message text

        An EncryptedSubMessage object inherits from SubMessage and has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    def decrypt_message(self):
        '''
        Attempt to decrypt the encrypted message 
        
        Idea is to go through each permutation of the vowels and test it
        on the encrypted message. For each permutation, check how many
        words in the decrypted text are valid English words, and return
        the decrypted message with the most English words.
        
        If no good permutations are found (i.e. no permutations result in 
        at least 1 valid word), return the original string. If there are
        multiple permutations that yield the maximum number of words, return any
        one of them.

        Returns: the best decrypted message    
        
        Hint: use your function from Part 4A
        '''
        best_decryption = ''
        permutations = get_permutations('aeiou')  # list all permutations of vowels
        n = 0
        keep_going = True

        while n < len(permutations) and keep_going: #for each permutation
            tran_dict = SubMessage.build_transpose_dict(self, permutations[n])  # build dictionary
            message = SubMessage.apply_transpose(self, tran_dict)  # apply transpose
            words = message.split()  # split corresponding message into list of words
            word_count = 0  # initialize word counter variable

            for i in range (0,len(words)):  # check how many of these words are valid English words
                real_word = is_word(self.valid_words, words[i])

                if real_word:  # if the word at this index is a word, increment the word_count
                    word_count += 1

                if word_count == len(words):  # if the word count is equal to the length of the list, break
                    best_decryption += message #return the current message
                    keep_going = False
                '''elif word_count > len(words) / 2:  # created to handle the story case ;)
                    best_decryption += message  # return the current message
                    break'''
            n += 1

        return best_decryption
    

if __name__ == '__main__':

    # Test Case 1
    message = SubMessage("Hello World!")
    permutation = "eaiuo"
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "Hallu Wurld!")
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())
     
    # Test Case 2
    message = SubMessage("Who art thou?")
    permutation = "oiaue"
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "Whu ort thue?")
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())
