__author__ = 'animeshjain'


import os
getcharac = []
inverted_index = {}
term_index = {}
term_occupancey = {}
number_document = {}
term_info = {}
if os.path.isfile('/jainani/pr1/python/term_index.txt'):
    os.remove("/jainani/pr1/python/term_index.txt")

if os.path.isfile('/jainani/pr1/python/term_info.txt'):
    os.remove("/jainani/pr1/python/term_info.txt")

Read_file = open('/jainani/pr1/python/doc_index.txt', 'r')
New_file4 = open('/jainani/pr1/python/term_index.txt', 'w')
New_file5 = open('/jainani/pr1/python/term_info.txt', 'w')
for s in Read_file:

    Modifiedstring = s.rstrip()
    line = Modifiedstring.split('\t')
    len(line)
    term_id = int(line[1])
    doc_id = int(line[0])
    min_term = int(line[2])
    if not inverted_index.has_key(term_id):
        term_index[term_id] = doc_id
        every_file = "\t"+str(doc_id)+":"+str(min_term)
        for i in line[3:]:
            position = (line[line.index(i)])
            new_count = int(position) - int(line[line.index(i) - 1])

            every_file = every_file+"\t"+"0:"+str(new_count)

        inverted_index[term_id] = every_file
        term_occupancey[term_id] = str(len(line) - 2)
        number_document[term_id] = str(1)
        every_file = ''

    elif inverted_index.has_key(term_id):
          prev = term_index.get(term_id)
          New_file = inverted_index.get(term_id)
          New_file = New_file+"\t"+str(int(doc_id) - int(prev))+":"+str(min_term)
          inverted_index.pop(term_id, None)
          for i in line[3:]:
              position1 = (line[line.index(i)])
              new_count1 = int(position1) - int(line[line.index(i) - 1])
              New_file = New_file+"\t"+"0:"+str(new_count1)
          term_index[term_id] = doc_id
          inverted_index[term_id] = New_file
          occupancy = int(term_occupancey.get(term_id))
          occupancy = occupancy + int(len(line) - 2)
          term_occupancey[term_id] = str(occupancy)
          TotalDocs = int(number_document.get(term_id))
          TotalDocs = TotalDocs + 1
          number_document[term_id] = str(TotalDocs)
          New_file = ''
offset = 0
for keys, value in inverted_index.items():
    id = int(keys)
    occur = int(term_occupancey.get(keys))
    Document_number = int(number_document.get(keys))
    get_output = str(keys) + value + "\n"
    New_file4.write(get_output)
    New_file5.write(str(id)+"\t"+str(offset)+"\t"+str(occur)+"\t"+str(Document_number)+"\n")
    offset = New_file4.tell()

New_file4.close()
New_file5.close()


















