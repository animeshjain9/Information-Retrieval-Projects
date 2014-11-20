__author____ = 'animeshjain'
__contact___ = 'animeshjain9@gmail.com'
__License___ = 'Animesh License'

#!/usr/bin/env python

import os
import re
from stemming.porter2 import stem
import xml.etree.ElementTree as ET
from collections import Counter
from collections import OrderedDict
import sys
import math
from decimal import Decimal

if os.path.isfile('/jainani/pr2/python/run.txt'):
    os.remove("/jainani/pr2/python/run.txt")



if os.path.isfile('/jainani/pr2/python/Okapi-TF.txt'):
    os.remove("/jainani/pr2/python/Okapi-TF.txt")

if os.path.isfile('/jainani/pr2/python/TF-IDF.txt'):
    os.remove("/jainani/pr2/python/TF-IDF.txt")

if os.path.isfile('/jainani/pr2/python/Okapi-BM25.txt'):
    os.remove("/jainani/pr2/python/Okapi-BM25.txt")

if os.path.isfile('/jainani/pr2/python/Laplace.txt'):
    os.remove("/jainani/pr2/python/Laplace.txt")

if os.path.isfile('/jainani/pr2/python/Jelinek-Mercer.txt'):
    os.remove("/jainani/pr2/python/Jelinek-Mercer.txt")

#rooturl = '/Users/animeshjain/Documents/IRAssignments/corpus'


Okapi_TF_file = open('/jainani/pr2/python/Okapi-TF.txt', 'w')
TF_IDF_file = open('/jainani/pr2/python/TF-IDF.txt', 'w')
Okapi_BM25 = open('/jainani/pr2/python/Okapi-BM25.txt', 'w')
Laplace_file = open('/jainani/pr2/python/Laplace.txt', 'w')
Jelinek_Mercer_file = open('/jainani/pr2/python/Jelinek-Mercer.txt', 'w')





class query:

    # global variable declaration that are used in the query class
    def __init__(self):
        self.getIndex = {}
        self.docidIndex = {}
        self.termFrequency = {}
        self.inverseDocumentFrequency = {}
        self.stopWords = {}
        self.tfquery = {}
        self.tfdocument = {}
        self.query_mapping = {}
        self.docname_and_id = {}
        self.term_in_number_of_documents = {}
        self.term_id_and_occurence_corpus = {}
        self.term = {}
        self.doc_id_to_position = {}
        self.term_D = {}
        self.term_and_term_id = {}
        self.term_id_and_term_offset = {}
        self.document_name_and_score = {}
        self.first_term = {}
        self.second_term = {}
        self.third_term = {}
        self.K_Value = {}
        self.Probability_of_term = {}
        self.list_of_queries = []
        self.tokens = []
        self.term_frequency = []
        self.tokenre = re.compile(r'\w+(\.?\w+)*')
        self.total_Words_Corpus = 0
        self.total_words_in_query = 0
        self.Number_of_Terms = 0
        self.counter = 0
        self.listOfFileId = []
        self.New_list_Of_Terms = []
        self.average_Number_Of_Queries = 0
        self.average_Number_Of_Words_Document = 0
        self.Total_score = 0
        self.score = 0
        self.query_counter = 0


    # This below function get the stop words from stoplist.txt file and store in a dictionary w
    def getStopWords(self):
        s = open('/jainani/pr2/python/supporting_files/stoplist.txt','r')
        listOfWords = [line.rstrip() for line in s]
        self.w = dict.fromkeys(listOfWords)
        s.close()

    # This below function gives the list of terms after checking whether the query term is present in stop words, if it
    # is not then apply stemming on it.
    def listOfTerms(self, query):
        query = query.lower()
        self.tokens = []
        for t in self.tokenre.finditer(query):
            if t.group(0) is not None and t:
                if t not in self.w:
                    self.tokens.append(t.group(0))
        Stem = [stem(t) for t in self.tokens]
        self.total_words_in_query = len(Stem)
        return Stem

    # This function reads the document DocElements.txt and map the Document Name to its Corresponding Document ID, and Document Name
    # to its corresponding Document Size.
    def readalldocument(self):
        file_id = 1
        docElement = open('/jainani/pr2/python/supporting_files/docElements.txt','r')
        for docname_and_size in docElement:
                docname_and_size_trim = docname_and_size.rstrip()
                docname_and_size_list = docname_and_size_trim.split('\t')
                self.counter = self.counter + 1
                self.docidIndex[file_id] = int (docname_and_size_list[1])
                self.docname_and_id[file_id] = docname_and_size_list[0]
                self.total_Words_Corpus = self.total_Words_Corpus + int(docname_and_size_list[1])
                self.listOfFileId.append(file_id)
                file_id = file_id + 1

        self.average_Number_Of_Words_Document = self.total_Words_Corpus / float (self.counter)
        #print self.average_Number_Of_Words_Document
        docElement.close()

    # parse the xml file which contains all the queries and map queries with their corresponding ids.
    def readallqueries(self):
        tree = ET.parse('/jainani/pr2/python/supporting_files/topics.xml')
        root = tree.getroot()
        for child in root:
            for child1 in child:
                if(child1.tag == 'query'):
                    self.query_mapping[child1.text] = child.attrib.get('number')
                    self.list_of_queries.append(child1.text)
                    self.query_counter = self.query_counter + 1
                    get_list_Of_Terms = self.listOfTerms(child1.text)
                    self.New_list_Of_Terms.extend(get_list_Of_Terms)
        self.average_Number_Of_Queries = len(self.New_list_Of_Terms) / float(self.query_counter)

    # Read the Termid.txt and maps term_id with their corresponding Term_name
    # Read the Term_info.txt and maps term_id with their offset position present in term_index.txt
    def readtermids(self):
        Read_termids = open('/jainani/pr2/python/supporting_files/termids.txt', 'r')
        term_info = open('/jainani/pr2/python/supporting_files/term_info.txt', 'r')
        for line_termid in Read_termids:
                term_and_ids = line_termid.rstrip()
                term_and_ids_list = term_and_ids.split('\t')
                self.term_and_term_id[term_and_ids_list[1]] = term_and_ids_list[0]
                self.Number_of_Terms = self.Number_of_Terms + 1
        for line_terminfo in term_info:
                term_info_string = line_terminfo.rstrip()
                term_info_list = term_info_string.split('\t')
                self.term_id_and_term_offset[term_info_list[0]] = term_info_list[1]
                self.term_id_and_occurence_corpus[term_info_list[0]] = term_info_list[2]

        term_info.close()
        Read_termids.close()

    # This below function counts the frequency of a term in a document
    def count_frequency(self, term, doc_id):
        if self.term_D.has_key(term):
            if (self.doc_id_to_position.has_key(str(doc_id) + term)):
                    value = self.doc_id_to_position[str(doc_id) + term]
                    self.termFrequency[term] = value
            else:
                    self.termFrequency[term] = 0

        else:
            term_index= open('/jainani/pr2/python/supporting_files/term_index.txt', 'r')
            self.term_frequency = []
            if self.term_and_term_id.has_key(term):
                                    term_id = self.term_and_term_id[term]
                                    self.term_D[term] = term_id
                                    offset_position = int(self.term_id_and_term_offset[term_id])
                                    term_index.seek(offset_position, 0)
                                    new_line8 = term_index.readline()
                                    self.term[term_id] = new_line8
                                    Modifiedstring7 = new_line8.rstrip()
                                    line_seven = Modifiedstring7.split('\t')
                                    c = 0
                                    var = ''
                                    arraylst = []
                                    for pos in line_seven[1:]:
                                        arraylst = []
                                        new_index = line_seven[line_seven.index(pos)]
                                        get_new = new_index.index(":")
                                        c = c + int(new_index[:get_new])
                                        if not self.doc_id_to_position.has_key(str(c) + term):
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
                                            self.term_frequency.append(c)
                                            self.doc_id_to_position[str(c) + term] = len(arraylst)
                                        else:
                                            continue
                                    self.term_in_number_of_documents[term] = len(self.term_frequency)
                                    if (self.doc_id_to_position.has_key(str(doc_id) + term)):
                                        value = self.doc_id_to_position[str(doc_id) + term]
                                        self.termFrequency[term] = value
                                    else:
                                        self.termFrequency[term] = 0
            else:
                self.term_D[term] = 'not found'
                self.term_in_number_of_documents[term] = 0
                self.termFrequency[term] = 0
            term_index.close()

    # This below function calculate the query score for the each document as per Okapi-TF Scoring Function.
    def calculate_tfdocument(self, doc_id, query):
        Total_score = 0.0
        square_of_tfdocument = 0.0
        square_of_tfquery = 0.0

        list_Of_Terms = self.listOfTerms(query)
        for term in list_Of_Terms:
            self.count_frequency(term, doc_id)
        cnt = Counter()
        for word in list_Of_Terms:
            cnt[word] += 1
        for word in list_Of_Terms:
            if not self.inverseDocumentFrequency.has_key(word):
                self.inverseDocumentFrequency[word] = cnt[word]
                str(cnt[word])
        for New_terms in list_Of_Terms:
            self.tfdocument[New_terms] = Decimal(self.termFrequency[New_terms]) / Decimal(Decimal(self.termFrequency[New_terms]) + Decimal(0.5) + Decimal(Decimal(1.5) * Decimal(Decimal(self.docidIndex[doc_id]) / Decimal(self.average_Number_Of_Words_Document))))
            self.tfquery[New_terms] = Decimal(self.inverseDocumentFrequency[New_terms]) / Decimal(Decimal(self.inverseDocumentFrequency[New_terms]) + Decimal(0.5) + Decimal(Decimal(1.5) * Decimal(Decimal(len(list_Of_Terms)) / Decimal(self.average_Number_Of_Queries))))
            Total_score = Decimal(Decimal(Total_score) + Decimal(Decimal(self.tfdocument[New_terms]) * Decimal(self.tfquery[New_terms])))
            square_of_tfdocument = Decimal(Decimal(square_of_tfdocument) + Decimal(Decimal(self.tfdocument[New_terms]) * Decimal(self.tfdocument[New_terms])))
            square_of_tfquery = Decimal(Decimal(square_of_tfquery) + Decimal(Decimal( self.tfquery[New_terms]) * Decimal(self.tfquery[New_terms])))

        if (square_of_tfdocument == 0.0) or (square_of_tfquery == 0.0):
            score = 0
        else:
            score = Decimal (Decimal(Total_score) / Decimal(Decimal(math.sqrt(square_of_tfdocument)) * Decimal(math.sqrt(square_of_tfquery))))


        if score > 1.0:
            score = 1.0
        else:
            score

        self.document_name_and_score[self.docname_and_id.get(doc_id)] = score
        self.tfdocument = {}
        self.tfquery = {}
        self.termFrequency = {}

    # This below function calculate the query score for the each document as per TF-IDF Scoring Function.
    def calculate_tf_idf_document(self, doc_id, query):
        Total_score = 0.0
        square_of_tfdocument = 0.0
        square_of_tfquery = 0.0
        list_Of_Terms = self.listOfTerms(query)
        for term in list_Of_Terms:
            self.count_frequency(term, doc_id)
        cnt = Counter()
        for word in list_Of_Terms:
            cnt[word] += 1
        for word in list_Of_Terms:
            if not self.inverseDocumentFrequency.has_key(word):
                self.inverseDocumentFrequency[word] = cnt[word]
                str(cnt[word])
        for New_terms in list_Of_Terms:
            if self.term_in_number_of_documents[New_terms] == 0:
                self.tfdocument[New_terms] = 0
            else:
                self.tfdocument[New_terms] = Decimal(Decimal(self.termFrequency[New_terms]) / Decimal(Decimal(self.termFrequency[New_terms]) + Decimal(0.5) + Decimal(Decimal(1.5) * Decimal(Decimal(self.docidIndex[doc_id]) / Decimal(self.average_Number_Of_Words_Document))))) * Decimal(math.log(Decimal(self.counter)/Decimal(self.term_in_number_of_documents[New_terms])))
            self.tfquery[New_terms] = Decimal(Decimal(self.inverseDocumentFrequency[New_terms]) / Decimal(Decimal(self.inverseDocumentFrequency[New_terms]) + Decimal(0.5) + Decimal(Decimal(1.5) * Decimal(Decimal(len(list_Of_Terms)) / Decimal(self.average_Number_Of_Queries))))) * Decimal(math.log(Decimal(self.query_counter)/Decimal(1.0)))
            Total_score = Decimal(Decimal(Total_score) + Decimal(Decimal(self.tfdocument[New_terms]) * Decimal(self.tfquery[New_terms])))
            square_of_tfdocument = Decimal(Decimal(square_of_tfdocument) + Decimal(Decimal(self.tfdocument[New_terms]) * Decimal(self.tfdocument[New_terms])))
            square_of_tfquery = Decimal(Decimal(square_of_tfquery) + Decimal(Decimal( self.tfquery[New_terms]) * Decimal(self.tfquery[New_terms])))

        if (square_of_tfdocument == 0.0) or (square_of_tfquery == 0.0):
            score = 0
        else:
            score = Decimal (Decimal(Total_score) / Decimal(Decimal(math.sqrt(square_of_tfdocument)) * Decimal(math.sqrt(square_of_tfquery))))
        if score > 1.0:
            score = 1.0
        else:
            score
        self.document_name_and_score[self.docname_and_id.get(doc_id)] = score
        self.tfdocument = {}
        self.tfquery = {}
        self.termFrequency = {}


    # This below function calculate the query score for the each document as per Okapi-BM25 Scoring Function.
    def calculate_bm_25_document(self, doc_id, query):
        score = Decimal(0)
        list_Of_Terms = self.listOfTerms(query)
        for term in list_Of_Terms:
            self.count_frequency(term, doc_id)
        cnt = Counter()
        for word in list_Of_Terms:
            cnt[word] += 1
        for word in list_Of_Terms:
            if not self.inverseDocumentFrequency.has_key(word):
                self.inverseDocumentFrequency[word] = cnt[word]
                str(cnt[word])
        for New_terms in list_Of_Terms:
            self.K_Value[New_terms] = Decimal(1.2) * ((Decimal(1 - 0.75)) + (Decimal(0.75) * Decimal(Decimal(self.docidIndex[doc_id]) / Decimal(self.average_Number_Of_Words_Document))))
            self.first_term[New_terms] = Decimal(math.log ((Decimal(self.counter) + Decimal(0.5)) / (Decimal(self.term_in_number_of_documents[New_terms]) + Decimal(0.5))))
            self.second_term[New_terms] = Decimal((Decimal(1) + Decimal(1.2)) * Decimal(self.termFrequency[New_terms])) / Decimal(self.K_Value[New_terms] + Decimal(self.termFrequency[New_terms]))
            self.third_term[New_terms] = Decimal((Decimal(1)  + Decimal(100)) * Decimal(self.inverseDocumentFrequency[New_terms])) / (Decimal(100) + Decimal(self.inverseDocumentFrequency[New_terms]))
            score = Decimal(Decimal(score) + Decimal(self.first_term[New_terms] * self.second_term[New_terms] * self.third_term[New_terms]))
        if score ==  0E-51 or score == 0E-52 or score == 0E-50:
            score = 0.0
        self.document_name_and_score[self.docname_and_id.get(doc_id)] = score
        self.tfdocument = {}
        self.tfquery = {}
        self.termFrequency = {}
        self.first_term = {}
        self.second_term = {}
        self.third_term = {}

    # This below function calculate the query score for the each document as per Laplace Smoothing Scoring Function.
    def calculate_laplace_document(self, doc_id, query):
        score = 0.0
        list_Of_Terms = self.listOfTerms(query)
        for term in list_Of_Terms:
            self.count_frequency(term, doc_id)
        cnt = Counter()
        for word in list_Of_Terms:
            cnt[word] += 1
        for word in list_Of_Terms:
            if not self.inverseDocumentFrequency.has_key(word):
                self.inverseDocumentFrequency[word] = cnt[word]
                str(cnt[word])
        for New_terms in list_Of_Terms:
            self.Probability_of_term[New_terms] = Decimal(Decimal(self.termFrequency[New_terms]) + 1) / Decimal(Decimal(self.docidIndex[doc_id]) + Decimal(self.Number_of_Terms))
            score = Decimal(score) + Decimal(math.log (self.Probability_of_term[New_terms]))
        self.document_name_and_score[self.docname_and_id.get(doc_id)] = score
        self.tfdocument = {}
        self.tfquery = {}
        self.termFrequency = {}
        self.Probability_of_term = {}

     # This below function calculate the query score for the each document as per Jelinek-Mercer Smoothing Scoring Function.
    def calculate_Jelinek_Mercer_document(self, doc_id, query):
        score = 0.0
        list_Of_Terms = self.listOfTerms(query)
        for term in list_Of_Terms:
            self.count_frequency(term, doc_id)
        cnt = Counter()
        for word in list_Of_Terms:
            cnt[word] += 1
        for word in list_Of_Terms:
            if not self.inverseDocumentFrequency.has_key(word):
                self.inverseDocumentFrequency[word] = cnt[word]
                str(cnt[word])
        for New_terms in list_Of_Terms:
            if self.term_and_term_id.has_key(New_terms):
                term_id = self.term_and_term_id[New_terms]
                occurrence = self.term_id_and_occurence_corpus[term_id]
                if self.docidIndex[doc_id] is not 0:
                    self.Probability_of_term[New_terms] = Decimal(Decimal(0.2) * (Decimal(self.termFrequency[New_terms]) / Decimal(self.docidIndex[doc_id]))) + Decimal(Decimal(1 - 0.2) * Decimal(Decimal(occurrence) / Decimal(self.total_Words_Corpus)))
                    score = Decimal(score) + Decimal(math.log (self.Probability_of_term[New_terms]))
        if self.docidIndex[doc_id] is not 0:
            self.document_name_and_score[self.docname_and_id.get(doc_id)] = score
        self.tfdocument = {}
        self.tfquery = {}
        self.termFrequency = {}
        self.Probability_of_term  = {}

    def queryIndex(self):
        self.getStopWords()
        self.readallqueries()
        self.readalldocument()
        self.readtermids()
        if sys.argv[1] == '--score' and sys.argv[2] == 'TF' and len(sys.argv) == 3:
            for search_query in self.list_of_queries:
                    for id in self.listOfFileId:

                        self.calculate_tfdocument(id, search_query)
                    d_sorted_by_value = OrderedDict(sorted(self.document_name_and_score.items(), key=lambda x: x[1], reverse=True))
                    counter = 1
                    for k, v in d_sorted_by_value.items():
                        word = str(self.query_mapping.get(search_query)) + '\t' + str(0) + '\t' + str(k) + '\t' + str(counter) + '\t' + str(v) + '\t' + 'run1'
                        counter = counter + 1
                        Okapi_TF_file.write(word)
                        Okapi_TF_file.write('\n')
            Okapi_TF_file.close()

        elif sys.argv[1] == '--score' and sys.argv[2] == 'TF-IDF' and len(sys.argv) == 3:
            for search_query in self.list_of_queries:
                    for id in self.listOfFileId:
                        self.calculate_tf_idf_document(id, search_query)
                    d_sorted_by_value = OrderedDict(sorted(self.document_name_and_score.items(), key=lambda x: x[1], reverse=True))
                    counter = 1
                    for k, v in d_sorted_by_value.items():
                        word = str(self.query_mapping.get(search_query)) + '\t' + str(0) + '\t' + str(k) + '\t' + str(counter) + '\t' + str(v) + '\t' + 'run1'
                        counter = counter + 1
                        TF_IDF_file.write(word)
                        TF_IDF_file.write('\n')



            TF_IDF_file.close()

        elif sys.argv[1] == '--score' and sys.argv[2] == 'BM25' and len(sys.argv) == 3:
            for search_query in self.list_of_queries:
                    for id in self.listOfFileId:
                        self.calculate_bm_25_document(id, search_query)
                    d_sorted_by_value = OrderedDict(sorted(self.document_name_and_score.items(), key=lambda x: x[1], reverse=True))
                    counter = 1
                    for k, v in d_sorted_by_value.items():
                        word = str(self.query_mapping.get(search_query)) + '\t' + str(0) + '\t' + str(k) + '\t' + str(counter) + '\t' + str(v) + '\t' + 'run1'
                        counter = counter + 1
                        Okapi_BM25.write(word)
                        Okapi_BM25.write('\n')



            Okapi_BM25.close()

        elif sys.argv[1] == '--score' and sys.argv[2] == 'Laplace' and len(sys.argv) == 3:
            for search_query in self.list_of_queries:
                    for id in self.listOfFileId:
                        self.calculate_laplace_document(id, search_query)
                    d_sorted_by_value = OrderedDict(sorted(self.document_name_and_score.items(), key=lambda x: x[1], reverse=True))
                    counter = 1
                    for k, v in d_sorted_by_value.items():
                        word = str(self.query_mapping.get(search_query)) + '\t' + str(0) + '\t' + str(k) + '\t' + str(counter) + '\t' + str(v) + '\t' + 'run1'
                        counter = counter + 1
                        Laplace_file.write(word)
                        Laplace_file.write('\n')



            Laplace_file.close()

        elif sys.argv[1] == '--score' and sys.argv[2] == 'JM' and len(sys.argv) == 3:
            for search_query in self.list_of_queries:
                    for id in self.listOfFileId:
                        self.calculate_Jelinek_Mercer_document(id, search_query)
                    d_sorted_by_value = OrderedDict(sorted(self.document_name_and_score.items(), key=lambda x: x[1], reverse=True))
                    counter = 1
                    for k, v in d_sorted_by_value.items():
                        word = str(self.query_mapping.get(search_query)) + '\t' + str(0) + '\t' + str(k) + '\t' + str(counter) + '\t' + str(v) + '\t' + 'run1'
                        counter = counter + 1
                        Jelinek_Mercer_file.write(word)
                        Jelinek_Mercer_file.write('\n')



            Jelinek_Mercer_file.close()

        else:
            print "invalid arguments"








q = query()
q.queryIndex()




