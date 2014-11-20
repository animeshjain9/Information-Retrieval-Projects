Kindly run the pip.sh file to install the external libraries used in the project.
Steps to execute the pip.sh
1) type the command "sh /jainani/pr1/pip.sh"

Overview of the project
1) Kindly run the part1 source code first to generate the docids.txt, termids.txt and doc_index.txt.
2) doc_index.txt file will be used by the part2 source code to generate term_index.txt and term_info.txt files
3) Once we will get the five files, these all files will be used by the part3 to search with the combination of term Name, document Name
and both.


Part1
1) docids.txt.zip present at the path /jainani/pr1
2) termids.txt.zip present at the path /jainani/pr1
3) doc_index.txt.zip present at the path /jainani/pr1
4) source code file name is part1.py which is present at the path /jainani/pr1/python

Steps to execute part1.py
1) Type the command "python /jainani/pr1/python/part1.py CorpusFilePath"
2) CorpusFilePath should be the path of the directory whose file need to be parsed
3) After parsing all the files present at the directory, three text files will be generated at the path
/jainani/pr1/python(file names are docids.txt, termids.txt and doc_index.txt)


Part2
1) term_index.txt.zip present at the path /jainani/pr1
2) term_info.txt.zip present at the path /jainani/pr1
3) source code file name is part2.py which is present at the path /jainani/pr1/python

Steps to execute part2.py
1) Type the command "python /jainani/pr1/python/part2.py"
2) This program read the file doc_index.txt and generate two new file whose names are term_index.txt and term_info.txt
3) These new files will be generated at /jainani/pr1/python

Part3
1) source code file name is part3.py

Steps to execute part3.py
1) We can do the three kind of search
2) Search the Term Name, which can be done using the command "python /jainani/pr1/python/part3.py --term TERM"
3) Search the Document Name, which can be done using the command "python /jainani/pr1/python/part3.py --doc DOCNAME"
4) Search the Term Name in the Particular Document, which can be done using the command
 "python /jainani/pr1/python/part3.py --term TERM --doc DOCNAME"


