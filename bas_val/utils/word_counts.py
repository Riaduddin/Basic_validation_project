"""
    Here, what the code does is counting words (excluding punctuations)
    by performance on a sample document, WPS Office counts 98 words where this code counted 99 words.
""" 

import os                                     
import docx2txt
import re   
from bas_val.logger import logging

class FileOperation_word_count:
    def __init__(self, filepath):
        logging.info("Intialization of word count")
        self.filepath = filepath

    def file_process(self):
        logging.info("Starting the word count")
        try:
            text = docx2txt.process(self.filepath) #took the docs file as input
            with open("demo.txt", "w",encoding='utf-8') as text_file:  #opened a text file(if doesn't exist, will create one automatically)
                text_file.write(text) #write on that text file what was already written on that docs file file 

        except IOError:    #This means that the file does not exist (or some other IOError)
            print("Oops, no file by that name")

        try:
            file = open("demo.txt","r")   #open the text file in reading mode(no modify)
            
            count = 0

            try:
                for line in file:               # Loop through each line via file handler
                    line=re.sub(r'\n', '', line)
                    words = line.split(" ")         # take each line and split make into a list using spaces exm: Introduction to the Project -> ['Introduction', 'to', 'the', 'Project:\n']
                    #print(words)
                    words = [item for item in words if item != '']
                    # if len(words) > 1:
                    #     print("length greater than 1:")
                    #     print(words)
                        #print(len(words))
                    table = str.maketrans(", ! @ . # $ * ( ) - \ / ", 24*" ")   # replacing those characters with whitespaces
                        
                    st = [w.translate(table) for w in words]                           # making a list with each word from the file
                    
                    count += len(st)
                    # print("count :",count)
                file.close()
                os.remove("demo.txt")
                return count
                #print("total number of words count: ",count)

            except IOError:    #This means that the file does not exist (or some other IOError)
                return "Our function didn't work"
        
        except IOError:    #This means that the file does not exist (or some other IOError)
            print("Created file was unavailable")

