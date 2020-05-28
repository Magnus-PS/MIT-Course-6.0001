# Problem Set 4A
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example: >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''


    if len(sequence) == 1: #if it's just a one character sequence, return that character
        return [sequence]

    perm_list = []  # to store permutations of given string
    for i, v in enumerate(sequence): #enumerate over sequence: i for index, v for value
        perm_list += [v + p for p in get_permutations(sequence[:i] + sequence[i + 1:])]
        #perm_list value is then current character plus permutations of remaining characters (those before/after current character)
        #pulled from: https://stackoverflow.com/questions/23116911/all-permutations-of-a-string-in-python-recursive/34620370
    return perm_list

if __name__ == '__main__':
#    #EXAMPLE
#    example_input = 'abc'
#    print('Input:', example_input)
#    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
#    print('Actual Output:', get_permutations(example_input))
    
#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a 
#    sequence of length n)

#TEST CASE 1
    test_input1 = 'a'
    print('Input: ', test_input1)
    print('Expected Output: ', ['a'])
    print('Actual Output: ', get_permutations(test_input1))

#TEST CASE 2
    test_input2 = 'to'
    print('Input: ', test_input2)
    print('Expected Output: ', ['to', 'ot'])
    print('Actual Output: ', get_permutations(test_input2))

#TEST CASE 3
    test_input3 = 'dog'
    print('Input: ', test_input3)
    print('Expected Output: ', ['dog', 'dgo', 'odg', 'ogd', 'gdo', 'god'])
    print('Actual Output: ', get_permutations(test_input3))

