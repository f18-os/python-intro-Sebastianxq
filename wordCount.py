#! /usr/bin/env python3
import sys              #cmd line args
import re               #regex tools
import os               #for checking if file is found
import subprocess       # for executions

# set input and output files
if len(sys.argv) is not 3:
    print("Correct usage: wordCountTest.py <input text file> <output file> <solution key file>")
    exit()

#takes in a file and prints it to the terminal
#need to convert into an open ended input
inputFile = sys.argv[1] 
outputFile = sys.argv[2]
filename = str(inputFile)
outputName = str(outputFile)
print (filename,outputName)

inputSource = open(filename, 'r')
outputSource = open(outputName, 'w')

#with open(inputSource, 'r') as preInfo:
   
#removes capitalizations from text file

inputPre = inputSource.read()
lowercaseInput = inputPre.lower()

    #debugging
    #print (lowercaseInput)


#removes all punctuation in the text file
punctuations = '''!-;:'",.?&_~'''
inputPost = ""
for char in lowercaseInput:
   #print char
   if char not in punctuations:
       inputPost = inputPost + char
#inputPost is currently a STRING

#debugging
print (inputPost)

testSplit = inputPost.split() #seperates words, by default .split is whitespace
#testSplit is currently a LIST

sortedWords = sorted(testSplit)
#sortedWords is currently a LIST

singleSortedWords = set(sortedWords) 
singleSortedWords = sorted(singleSortedWords)
#singleSortedWords is currently a LIST

#print singleSortedWords
#need to convert into an open ended input
#creates an output text file
output = open("output.txt", "w+")

for word in singleSortedWords:
    
    wordBuff = word
    wordBlank = word + " "
    #if word is not at the end of the line
    if inputPost.count(wordBlank) > 0:
        word += " "
        word += str(inputPost.count(wordBlank))
        word += " "
        print (word)
        word +="\n"
        
    #word is at the end of line
    else:
        wordBuff += "\n"
        word += " "
        count = inputPost.count(wordBuff)+inputPost.count(word)
        print (count," is count")
        word += str(count)
        word += " "
        word += "\n"
    outputSource.write(word)

inputSource.close()
outputSource.close()
