#counts the number of times a word appears in a file and outputs it into a text file
#

#takes in a file and prints it to the terminal
#need to convert into an open ended input
inputFile = open(r"C:\Users\Seabass\Desktop\OSPython\nets-python-intro-master\declaration.txt")

#removes capitalizations from text file
inputPre = inputFile.read()
lowercaseInput = inputPre.lower()
#lowercaseInput is currently a STRING

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
print inputPost

testSplit = inputPost.split() #seperates words, by default .split is whitespace
#testSplit is currently a LIST

#convert to a set but then count the set item number of appearences in the list before you converted to a set?!?!?
sortedWords = sorted(testSplit)
#sortedWords is currently a LIST

singleSortedWords = set(sortedWords) #converts to a set to remove duplicates
singleSortedWords = sorted(singleSortedWords)
#singleSortedWords is currently a LIST

#print singleSortedWords
#need to convert into an open ended input
#creates an output text file
output = open("output.txt", "w+")

for word in singleSortedWords:
    #print word,inputPost.count(word)
    #numWords = inputPost.count(word)

    #count is experiencing an error but WHY
    #try to make a conditional that checks for whether its EOL or not
    wordBuff = word
    wordBlank = word + " "
    #word is not at the end of line
    #an issue is that it counts even words that end with a with a blank space!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
    #use another buffer for the actual count
    if inputPost.count(wordBlank) > 0:
       # wordBlank = word + " "
        word += " "
        word += str(inputPost.count(wordBlank))
        word += " "
        print word
        word +="\n"
    #word is at the end of line
    else:
        wordBuff += "\n"
        word += " "
        count = inputPost.count(wordBuff)+inputPost.count(word)
        print count," is count"
        word += str(count)
        word += " "
        word += "\n"
    output.write(word)

    # if inputPost.count(word) == 0:

    # reads every instance of a word occurance
    # if a is looked for it will return EACH A THAT APPEARS IN THE DOCUMENT
    # finalCount = str(inputPost.count(word))
    # finalWord = word+" "+finalCount
    # print finalWord
    # finalOutput = finalWord+'\n'
    # output.write(finalOutput)

#works except it prints EACH instance of an item instead of just one and the total
#for item in sorted(testSplit):
 #   print item,inputPost.count(item)
#counts how many times a word appears and then stores it into a counter
#str(result.count("sentence"))



#---------------------------------------------------------------------------------------------------------
#example of calculating the total number of words and the total number of occurance
#mystring = "This sentence is a simple sentence."
#result = mystring.split()
#print result
#print "The total number of words is: "  + str(len(result))
#print "The word 'sentence' occurs: " + str(result.count("sentence"))
#---------------------------------------------------------------------------------------------------------

inputFile.close()
output.close()
