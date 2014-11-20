__author__ = 'animeshjain'
import os
import re
import nltk
from stemming.porter2 import stem
import sys

root_url = sys.argv[1]
#path = '/Users/animeshjain/Documents/IRAssignments/corpus'
path = root_url
if os.path.isfile('/jainani/pr1/python/docids.txt'):
    os.remove("/jainani/pr1/python/docids.txt")

if os.path.isfile('/jainani/pr1/python/termids.txt'):
    os.remove("/jainani/pr1/python/termids.txt")

if os.path.isfile('/jainani/pr1/python/doc_index.txt'):
    os.remove("/jainani/pr1/python/doc_index.txt")

stop_words = {}
stop = []
join_string = ''
counter2 = 1

counter1 = 1
stop=open('/jainani/pr1/python/stoplist.txt','r')
for s in stop:
    line = s.strip()
    stop_words[line] = line

#print stop_words

infile = ''
file_id = {}
porter=nltk.PorterStemmer()
New_id = {}
tokenre = re.compile(r'\w+(\.?\w+)*')

avoidtags = set(["link","script","style"])

terms = {}
word2 = ''
tokens = []
New_file = open('/jainani/pr1/python/docids.txt', 'w')
New_file1 = open('/jainani/pr1/python/termids.txt','w')
New_file2 = open('/jainani/pr1/python/doc_index.txt', 'w')



def getinfile(data12):
     tokens = []

     global terms
     global counter2
     global counter1
     global word2
     terms = {}
     global infile
     file_id[infile] = counter2
     counter2 = counter2 + 1
     word = str(file_id.get(infile)) + '\t' + str(infile)
     New_file.write(word)
     New_file.write('\n')
     getlower = data12.lower()
     for t in tokenre.finditer(getlower):
          if t.group(0) is not None and t:
              tokens.append(t.group(0))
     Stem = [stem(t) for t in tokens]
     for position,t in enumerate(Stem):
            if not terms.has_key(t) and not stop_words.has_key(t):
                    if not New_id.has_key(t):
                        New_id[t]=counter1
                        counter1 = counter1 + 1
                        word1 = str(New_id.get(t)) + '\t' + t
                        New_file1.write(word1)
                        New_file1.write('\n')
                    terms[t] = [position + 1]
            elif terms.has_key(t):
                terms[t].append(position + 1)
     for keys, value in New_id.items():
         if not terms.get(keys):
             continue
         else:
             for d in terms.get(keys):
                word2 = word2 + '\t' + str(d)
             word2.rstrip()
         word3 = str(file_id.get(infile)) + '\t' + str(New_id.get(keys)) +  word2

         word2 = ''
         New_file2.write(word3)
         New_file2.write('\n')





def remove_headers(getdata):
    index = getdata.index('\r\n\r\n',0)
    index = getdata.index('\r\n\r\n',index+1)
    getdata = getdata[index:]
    getdata = getdata.lower()
    return getdata




for dir_entry in os.listdir(path):
    dir_entry_path = os.path.join(path, dir_entry)
    if os.path.isfile(dir_entry_path):
        with open(dir_entry_path, 'r') as my_file:
            try:
                infile = dir_entry
                getdata = my_file.read()
                gethtml_remove_headers = remove_headers(getdata)
                join_string = nltk.clean_html(gethtml_remove_headers)
                getinfile(join_string)
                join_string = ''
            except Exception as e:
                 e


New_file.close()
New_file1.close()
New_file2.close()

