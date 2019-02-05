# -*- coding: utf-8 -*-
"""
Created on Sun Sep 10 14:38:23 2017
@author: Jaydeep
This script is compatible with python 2.7
"""

# for convert int division to deciaml value
from __future__ import division

# Counter is for word count dictionary
# OrderDict is for ordering dictionary value
from collections import Counter, OrderedDict

# for retrieve text and meta data from pdf file
from PyPDF2 import PdfFileReader

# beautiful shop for extracting content from html
from bs4 import BeautifulSoup

# docx library for document file manipulation
from docx import Document

# to remove non ascii charcs from input text
# clear texts
import re

# for json parsing
import json

################# dataParsing function start ##################
"""
This fundction is take extracted textData as String from inputFile 
and 
then it will convert it into structured data
in order to word, it's frequency and probability

@param1 textData: extracted text as String from file
@param2 outputFileName: export text data file Object
@return dictionaryObject: contains tokens and it's frequency
"""
def dataParsing(textData, outputFileName):
    # for case ignore convert whole string to lower case
    textData = textData.lower()
    # reading only wrords, non ascii and symbols are ignored
    allWords = re.sub('[^\w]', ' ', textData).split()
    # count each words and store in counter object
    dictWordCount = Counter(allWords)
    printDictToTextFile(dictWordCount,outputFileName)
    return dictWordCount
    
################# dataParsing function over ##################


################# printDictToTextFile function start ##################
"""
This function will take dictionary object as a args
and
export structured data into ouput text file as words, frequency and probability

@param1 dictObj: dictionary object that contains word and it's frequency
@param2 outputFileName: file name to extract structured data
"""
def printDictToTextFile(dictObj, outputFileName):
    # total word count for probability
    totalWord = len(dictObj)
    
    # descending order of their frequency
    dictObj = OrderedDict(dictObj.most_common())
    
    # assign file object from outfile file name in write mode
    outputFile = open(outputFileName,"w")
    
    # some decoration that looks like heading and title
    outputFile.write("Total Words are: "+totalWord.__str__())
    outputFile.write("\n")
    outputFile.write("----------------------------------------------")
    outputFile.write("\n")
    outputFile.write("{:<16}\t{}\t{}".format("Word","Freq.","Probability"))
    outputFile.write("\n")
    outputFile.write("----------------------------------------------")
    
    # print it in tabular form
    # where i is a word
    # and   j is a frequency of word in a file
    for i,j in dictObj.items() :
        outputFile.write("\n")
        outputFile.write("{:<16}\t{}\t{:.10f}".format(i, j, j/totalWord))
    
    # close open file for free up resources
    outputFile.close()
################# printDictToTextFile function over ##################


################# readFile function start ##################
"""
This readFile function is common function for reading below types of file
1. text file
2. html file
3. pdf file
4. doc file
5. json file
using various library and packages it will extract data from input file
based on their types
and then return dictionary object contains words and it's frequency

@param1 inputFileName: file name as a string to read contents
@param2 outputFileName: output file name to save extracted data
@return dictionaryObject: contains tokens and it's frequency
"""
def readFile(inputFileName,outputFileName):
    # try prevent exception like io error
    try:
        print "reading", inputFileName ,"file..."
        # string object that hold all text content
        inputString = ""
        
        if ".txt" in inputFileName:
            # code of reading text file
            # assign file object from input file name in reading mode
            inputFile = open(inputFileName,"r")
            # extract string data from file
            inputString = inputFile.read()
            
        elif ".htm" in inputFileName or ".html" in inputFileName:
            # code of reading html file
            # assign file object from input file name in reading mode
            inputFile = open(inputFileName,"r")
            # parse html file using BeautifulSoup
            soup = BeautifulSoup(inputFile,'html.parser')
            # extract data from file
            inputString = ''.join(soup.findAll(text=True))
        
        elif ".pdf" in inputFileName:
            # code of reading pdf file
            # assign file object from input file name in reading binary mode
            inputFile = open(inputFileName,"rb")
            # read pdf file using PdfFileReader class
            pdfFile = PdfFileReader(inputFile)
            # total number of pages in pdf file
            totalPages = pdfFile.getNumPages()
            
            # extract data from all the pages
            for index in range(totalPages) :
                inputString +=pdfFile.getPage(index).extractText()
        
        elif ".docx" in inputFileName or ".doc" in inputFileName:
            # code of reading doc file
            # assign file object from input file name in reading binary mode
            inputFile = open(inputFileName,"rb")
            # parse document file using Document class
            document = Document(inputFile)
            # extract data from all the paragraphs
            for para in document.paragraphs:
                inputString+=para.text
            
        elif ".json" in inputFileName:
            # code of reading tweets from json file
            # assign file object from input file name in reading mode
            inputFile = open(inputFileName,"r")
            # parse tweets file using json class
            jsonData = json.load(inputFile)
            # json structure ref: https://dev.twitter.com/rest/reference/get/statuses/user_timeline
            # extract data from each json object in an json array
            for i in range(len(jsonData)):
                # where text is key value of json object in an Array
                inputString+=jsonData[i]["text"]         
            
        else: 
            print "not recognize file type."
            # do nothing go back
            return
        
        # parse unstructed data and output file name
        # it will return dictionary object for future reference
        dictObj = dataParsing(inputString, outputFileName)
        print "index extracted in",outputFileName, "done."
        
        # close open input file for free up resources
        inputFile.close()
        # return dictionary object for future reference
        return dictObj
    except IOError:
        # gives error if file path is not available in loval machine
        print "Error: File not found."
    except Exception, e:
        # any way free resources
        inputFile.close()
        print "Error:", str(e)
    
################# readFile function over ##################
    

################# selectFile function start ##################
"""
This selectFile function is get input from user and reading file and parsing data
@param1 index : user input as int
"""
def selectFile(index):
    if int(index) == 1:
        # start reading text file
        dict1 = readFile(inputTextFileName,outputTextFileName)
    elif int(index) ==2:
        # start reading html file
        dict2 = readFile(inputWikipediaFileName, outputWikipediaFileName)
    elif int(index) ==3:
        # start reading pdf file
        dict3 = readFile(inputPDFFileName, outputPDFFileName)
    elif int(index) ==4:
        # start reading document file
        dict4 = readFile(inputWordFileName,outputWordFileName)
    elif int(index) ==5:
        # start reading json file that contains tweets
        dict5 = readFile(inputTweetFileName,outputTweetFileName)
    elif int(index) ==6:
        # for combination of all the file read all file and combine dictionary
        dict1 = readFile(inputTextFileName,outputTextFileName)
        dict2 = readFile(inputWikipediaFileName, outputWikipediaFileName)
        dict3 = readFile(inputPDFFileName, outputPDFFileName)
        dict4 = readFile(inputWordFileName,outputWordFileName)
        dict5 = readFile(inputTweetFileName,outputTweetFileName)
        # combine all the indexes
        resultDictObj = Counter(dict1) + Counter(dict2) + Counter(dict3) + Counter(dict4) + Counter(dict5)

        # print into comman output file
        printDictToTextFile(resultDictObj,combineOutputFileName)
        print "index are merged in",combineOutputFileName,"file done."
    else:
        print "Seems like you are tired\n Hint: Enter 7"

################# selectFile function over ##################


#####################################################
###### Main Program starts from here
#####################################################

# file names are predefined
# in which input and outpur is directory
inputTextFileName = "input/inputTextFile.txt"
outputTextFileName = "output/outputofTextFile.txt"

inputWikipediaFileName = "input/inputWikipediaFile.htm"
outputWikipediaFileName = "output/outputofWikiFile.txt"

inputPDFFileName = "input/inputPDFFile.pdf"
outputPDFFileName = "output/outputofPDFFile.txt"

inputWordFileName = "input/inputWordFile.docx"
outputWordFileName = "output/outputofWordFile.txt"

inputTweetFileName = "input/inputTweetFile.json"
outputTweetFileName = "output/outputofTweetFile.txt"

combineOutputFileName = "output/combineOutFile.txt"

# run time user menu instruction
userInputString = """Please enter which file type of you want to create index.\nChoice is between of 1 to 7 
1. Text file
2. HTML file
3. PDF file
4. Doc File
5. Tweet file
6. Combine index of all files
7. Exit
Your input: """

# input mechanism
while True:
    choice = raw_input(userInputString)    
    if choice.isdigit():
        # if choice is 7 then terminate programm
        if int(choice) == 7:
            break
        else :
            # pass choice to file reading function
            selectFile(choice)
    else:
        # if user input is other than integer
        print "This program is recognize only integer input.\n try one more with integer value."
################### Main Program Over #################