import random
import math

letter_bag = sorted("..EEEEEEEEEEEEAAAAAAAAAIIIIIIIIIOOOOOOOONNNNNNRRRRRRTTTTTTLLLLSSSSUUUUDDDDGGGBBCCMMPPFFHHVVWWYYKJXQZ")
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def runSim(fn,number_of_players,runs):
    words = makeWordSet(fn)
    successes = 0
    for r in range(runs):
        letters = drawLetters(number_of_players)
        if doTheseLettersFormAWord(letters,words):
            successes += 1
    return makeConfidenceInterval(successes,runs)

def makeConfidenceInterval(successes,runs):
    p = successes/runs
    std = math.sqrt(p*(1-p)/runs)
    return (p-2*std,p+2*std)

def drawLetters(number_of_players):
    return ''.join(sorted(['E'] + random.sample(letter_bag,6)))#+number_of_players-1)
    #if all_letters[0] == '.' and all_letters[1] == '.':
        #return ''.join(all_letters)
    #else:
        #return drawLetters(number_of_players)
    #if ord(all_letters[0]) < min([ord('Z')] + list(map(ord,all_letters[8:]))):
    #    return ''.join(sorted(all_letters[0:7]))
    #else:
    #    return drawLetters(number_of_players)

def doTheseLettersFormAWord(letters,words):
    letters_sorted = sorted(letters)
    if letters_sorted[1] == ".":
        letterss = set()
        for l1 in alphabet:
            for l2 in alphabet:
                letterss.add(''.join(sorted([l1] + [l2] + letters_sorted[2:])))
    elif letters_sorted[0] == ".":
        letterss = set()
        for l1 in alphabet:
            letterss.add(''.join(sorted([l1] + letters_sorted[1:])))
    else:
        letterss = [''.join(letters_sorted)]
    return words.intersection(set(letterss))

def makeWordSet(fn):
    words = set()
    with open("wordlist") as f:
        for w in f:
            w = w.strip()
            if len(w) == 7:
                words.add(''.join(sorted(w)))
    return words
