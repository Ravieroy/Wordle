import string
from collections import Counter

### So we start with a word list for most common english words. We can start with an inbuilt dictionary or some different word list as well.

#List of most common 5 letter words
word_list = open("words.txt").read().split()
word_length = 5 # length of words
allowed_attempts = 6 # number of allowed attempts
counts = Counter(letter for word in word_list for letter in word)

def get_weight(word_):
    """
    word_ : Takes the input word and gives it weight.
    Higher the number, more weight(not necessarily more common) it has.
    """
    weight = 0
    unique_word = "".join(set(word_)) #Avoids adding contribution from repeating characters.
    for char in unique_word:
        weight += counts[char]
        total = sum(counts.values())
    return weight/total


def sorted_word_list(list_):
    """
    list_ : Takes the input word list
    Sorts the words in the list_ in descending order(lowest to highest)
    """
    sorted_list=[]
    for item in list_:
        weight = get_weight(item)
        tmp_list = [item,weight]
        sorted_list.append(tmp_list)
    return sorted(sorted_list, key=lambda x:x[1],reverse=False)


def display_common_words(list_):
    """
    Displays most common words after each guesses.
    """
    
    sorted_list = sorted_word_list(list_)
    first_n_list = sorted_list
    for i in range(len(sorted_list)):
        word = first_n_list[i][0]
        weight = first_n_list[i][1]
        print(f"{word} : {weight:.3f}")

#Take input for first word
def input_word():
    """
    Takes the input from the user
    """
    while True:
        word = input("Enter Your Guess: ")
        if len(word) == word_length and word.lower() in word_list:
            break
    return word.lower()

def check_response(response):
    if response == "GGGGG":
        print("Congrats you got the word!!")
        exit()


def input_response():
    """
    Collects the response from the wordle.
    
    G: Green(Correct character at correct position)
    Y: Yellow(Correct character at wrong position)
    ?: Black (wrong character)
    
    """
    
    print(f"Type the color-coded response from Wordle for the last word (G,Y,?): ")
    while True:
        response = input("Response from Wordle: ")
        if len(response) == word_length and set(response) <= {"G", "Y", "?"}:
            break
        else:
            print(f"Error - invalid answer {response}")
    return response


def match_word(word, word_):
    """
    word: The word to be matched
    word_: The set of alphabets 
    
    This matches the characters of the word to the set of alphabets.
    """
    for word_char, alphabet in zip(word, word_):
        if word_char not in alphabet:
            return False
    return True


def match(alphabets_list, possible_words):
    """
    This function filters the new words from the word_list
    after response from wordle is given.
    """
    return [word for word in possible_words if match_word(word, alphabets_list)]

def solve_wordle():
    
    """
    Solves the wordle interactively
    """
    
    possible_words = word_list.copy()
    alphabets_list = [set(string.ascii_lowercase) for _ in range(word_length)]
    for attempt in range(1, allowed_attempts + 1):
        print(f"Attempt {attempt} with {len(possible_words)} possible words: ")
        display_common_words(possible_words) #displays the words
        word = input_word() #takes input from user
        response = input_response() #takes response
        check_response(response) #Terminates the program if GGGGG is achieved.
        for index, letter in enumerate(response):
            if letter == "G": #Fix the position to have that character
                alphabets_list[index] = {word[index]}
            elif letter == "Y":#Remove the char from that index(position)
                try:
                    alphabets_list[index].remove(word[index])
                except KeyError:
                        pass
            elif letter == "?": #Remove the char
                for vector in alphabets_list:
                    try:
                        vector.remove(word[index])
                    except KeyError:
                        pass
        possible_words = match(alphabets_list, possible_words)

solve_wordle()