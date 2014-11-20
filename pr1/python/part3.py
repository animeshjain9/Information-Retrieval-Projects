__author__ = 'animeshjain'
from stemming.porter2 import stem
import sys


if sys.argv[1] == '--doc' and len(sys.argv) == 3:
     getDocument = sys.argv[2]
     getTerm = ''
elif sys.argv[1] == '--term' and len(sys.argv) == 3:
     getTerm = sys.argv[2]
     getDocument = ''
elif sys.argv[1] == '--term' and sys.argv[3] == '--doc' and len(sys.argv) == 5:
    getTerm = sys.argv[2]
    getDocument = sys.argv[4]

elif sys.argv[1] == '--doc' and sys.argv[3] == '--term' and len(sys.argv) == 5:
    getTerm = sys.argv[4]
    getDocument = sys.argv[2]
else:
    print "invalid arguments"
    getTerm = ''
    getDocument = ''


flag = 'false'
flag_new = 'false'


if getDocument is '' and getTerm is not '':
    Stemming_word = stem(getTerm.lower())
    Read_termids = open('/jainani/pr1/python/termids.txt', 'r')
    Read_term_info = open('/jainani/pr1/python/term_info.txt', 'r')
    for s in Read_termids:
        if Stemming_word in s:
            Modifiedstring = s.rstrip()
            line = Modifiedstring.split('\t')
            if Stemming_word == line[1]:
                get_id = line[0]
                flag = 'true'
                new_line = ''
                for new_line in Read_term_info:
                    Modifiedstring1 = new_line.rstrip()
                    line1 = Modifiedstring1.split('\t')
                    if line1[0] == get_id:
                        offset = line1[1]
                        occ = line1[2]
                        docs = line1[3]
                        print "Listing for term::"+ getTerm
                        print "TERMID::"+ get_id
                        print "Number of documents containing term::"+ docs
                        print "Term frequency in corpus::"+ occ
                        print "Inverted list Offset ::"+ offset
                    else:
                        continue
            else:
                continue
    if flag == 'false':
        print "Term is not found"

    Read_termids.close()
    Read_term_info.close()

elif getDocument is not '' and getTerm is '':
    Read_docids = open('/jainani/pr1/python/docids.txt', 'r')
    Read_doc_index = open('/jainani/pr1/python/doc_index.txt', 'r')
    for new_line3 in Read_docids:
        Modifiedstring2 = new_line3.rstrip()
        line2 = Modifiedstring2.split('\t')
        if line2[1] == getDocument:
            Doc_id = line2[0]
            number = 0
            total = 0
            flag = 'true'
            for new_line4 in Read_doc_index:
                Modifiedstring3 = new_line4.rstrip()
                line3 = Modifiedstring3.split('\t')
                if line3[0] == Doc_id:
                    number = number + 1
                    total = total + int(len(line3) - 2)
                else:
                    continue
            print "Listing for document::" + getDocument
            print "DOCID::" + Doc_id
            print "Distinct Terms::" + str(number)
            print "Total terms ::" + str(total)
            break
        else:
            continue
    if flag == 'false':
        print "Document is  not found"

    Read_docids.close()
    Read_doc_index.close()

elif getDocument is not '' and getTerm is not '':
    Stemming_word2 = stem(getTerm.lower())
    print Stemming_word2
    Read_docids = open('/jainani/pr1/python/docids.txt', 'r')
    Read_termids = open('/jainani/pr1/python/termids.txt', 'r')
    Read_term_info = open('/jainani/pr1/python/term_info.txt', 'r')
    print "Inverted list for terms::" + getTerm
    print "In document::" + getDocument
    for new_line5 in Read_docids:
        Modifiedstring4 = new_line5.rstrip()
        line4 = Modifiedstring4.split('\t')
        if line4[1] == getDocument:
            doc_id = line4[0]
            flag_new = 'true'
            break
        else:
            continue

    if flag_new is 'false':
        print "Document not found"
    else:
        get_doc_id = int(doc_id)
        for new_line6 in Read_termids:
            if Stemming_word2 in new_line6:
                Modifiedstring5 = new_line6.rstrip()
                line5 = Modifiedstring5.split('\t')
                if line5[1] == Stemming_word2:
                    term_id = line5[0]
                    flag = 'true'
                    print "TERMID ::"+ term_id
                    print "DOCID::" + doc_id
                    for new_line7 in Read_term_info:
                        Modifiedstring6 = new_line7.rstrip()
                        line6 = Modifiedstring6.split('\t')
                        if line6[0] ==  term_id:
                            Modifiedstring6 = new_line7.rstrip()
                            line6 = Modifiedstring6.split('\t')

                            offset_position = int(line6[1])
                            Read_term_index = open('/jainani/pr1/python/term_index.txt', 'r')
                            Read_term_index.seek(offset_position, 0)

                            new_line8 = Read_term_index.readline()

                            Modifiedstring7 = new_line8.rstrip()
                            line_seven = Modifiedstring7.split('\t')

                            c = 0
                            var = ''
                            arraylst = []
                            for pos in line_seven[1:]:
                                new_index = line_seven[line_seven.index(pos)]

                                get_new = new_index.index(":")
                                c = c + int(new_index[:get_new])
                                if c == get_doc_id:

                                    First_position = int(new_index[get_new + 1:])
                                    arraylst.append(str(First_position))
                                    for pos1 in line_seven[line_seven.index(pos) + 1:]:
                                        if pos1.startswith("0"):
                                            get_new1 = pos1.index(":")
                                            Next_position = int(pos1[get_new1 + 1:])
                                            First_position = First_position + Next_position
                                            arraylst.append(str(First_position))
                                        else:
                                            break
                                    break
                            print "Term frequency in document::" + str(len(arraylst))
                            if not arraylst:
                                print "Position:: 0"

                            else:
                                print "Position::" + ','.join(arraylst)

                            Read_term_index.close()


                        else:
                            continue

            else:
                continue
        if flag == 'false':
            print "Term-Id not found"

    Read_docids.close()
    Read_termids.close()
    Read_term_info.close()



else:
    print "Document Name and Term Name is not entered and both are empty"





























