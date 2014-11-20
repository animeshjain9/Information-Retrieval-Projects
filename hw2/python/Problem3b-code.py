__author__ = 'animeshjain'
from math import log

print "################After Executing the problem3b-code.py code ################################### "

lines = open("output.txt").readlines()
words = [ w for l in lines for w in l.rstrip().split()]
Vocabularywords = set()
getVocabularycount = 0
getwordcount = 0
Sqrx = 0
Mulxy = 0
getx = 0
gety = 0
for newword in words:
    getwordcount = getwordcount + 1
    if newword not in Vocabularywords:
        Vocabularywords.add(newword)
        getVocabularycount = getVocabularycount + 1
    Mulxy = Mulxy + log(getwordcount, 2) * log(getVocabularycount, 2)
    gety = gety + log(getVocabularycount, 2)
    Sqrx = Sqrx + pow(log(getwordcount, 2), 2)
    getx = getx + log(getwordcount, 2)
print "Vocabulary words Count:", getVocabularycount
print "Total Number of words Count:", getwordcount
getx = getx /getwordcount
gety = gety /getwordcount
getBeta = (Mulxy - getwordcount * getx * gety) / (Sqrx - getwordcount * getx * getx)
Beta = (gety * Sqrx - getx * Mulxy)/ (Sqrx - getwordcount * getx * getx)
Constantk = pow(2,Beta)

print "The Value of k:", Constantk
print "The Value of b:", getBeta






