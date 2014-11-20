__author__ = 'animeshjain'
from collections import Counter
from prettytable import PrettyTable

print "################After Executing the problem2a-code.py code ################################### "

lines = open("output.txt").readlines()

words = [ w for l in lines for w in l.rstrip().split()]
totalWord = len(words)

#Get the Count of Total Words
print 'Total Words in text:', totalWord
counts = Counter( words )
Totalvoacbularywords = len(counts)

#Get the Count of Vocabulary Words
print 'Distinct Word in the text:', Totalvoacbularywords
k = 25
print 'List of words with Frequency, Rank, Probability and Product(c):'
a = 1
c = 1
Listof25VocabularyWords = list(counts.most_common(k))
ListofALLVocabularyWords = list(counts.most_common(Totalvoacbularywords))
x = PrettyTable(["Word", "Occurrence", "Rank(r)", "Probability(Pr%)", "Product(c) = Rank(r) * Probability(Pr)"])
x.padding_width = 1
x.align["Word"] = "l"

#Get the List of first 25 words Having the Highest frequency in the Text
for getatre in Listof25VocabularyWords:
    x.add_row([getatre[0], getatre[1],  c,   ((float(getatre[1])/totalWord) * 100), c * (float(getatre[1])/totalWord)])
    c += 1

#Get the List of first 25 words starting with "F"
b = 1
for wordstartsf in ListofALLVocabularyWords:
    if wordstartsf[0].startswith('f') and b >= 25:
        if a <= 25:
            x.add_row([wordstartsf[0], wordstartsf[1], b, ((float(wordstartsf[1])/totalWord) * 100), b * (float(wordstartsf[1])/totalWord) ])
            a += 1
        else :
            break
    b += 1
print x





