#! /usr/bin/env python3

import os, sys, time, re

pid = os.getpid()
userIn = " "

#would i have to put everything inside this loop so the shell continues to repeat?
while (userIn == " " or userIn == "" and userIn != "exit"):
#while (userIn != "exit"):
  os.write(1, ("type>").encode())
  userIn = input('')
  #os.write(1, ("The user inputted %s \n" %userIn).encode())
  #so from here take in user input and seperate based on white space
  userArgs = userIn.split();
  print (userArgs)

  #conditional that looks for >,<,| and then appropriately does something
  #run through all directories for the first option and see if you find anything
  

os.write(1, ("ABOUT TO FORK (pid:%d)\n" % pid).encode())
rc = os.fork()

#Error for fork
if rc < 0:
  os.write(2, ("fork failed, returning %d\n" % rc).encode())
  sys.exit(1)

#execute what is asked for in the parent
elif rc == 0:                   # child

   #so inside here i get conditionals for >,<,| and then adjust accordingly
  #conditionals should be set before i start searching?
  
  #time.sleep(2)
  #for the sake of min requirements do i need to even find the index
  #or once found can I assume it is in the second position

  #store left's output to right's file
  ioType = -1
  if ">" in userArgs:
    #print(">, args 1 executes, arg2 stores")
    ioType = 0
    print("input file is ", userArgs[(userArgs.index(">"))-1])
    print("output file is ", userArgs[(userArgs.index(">"))+1])

  #use right file as input for the left's  
  if "<" in userArgs:
    ioType = 1
    print("< detected")
    print("index is", userArgs.index("<"))

   #use left file's output as the input for the right
   #for piping, you must have 2 children?? one to execute the left
   #and the other to take that output as input for the right
  if "|" in userArgs:
    ioType = 2
    print("| detected")
    print("index is", userArgs.index("|"))
          
  os.write(1, ("Child: My pid==%d.  Parent's pid=%d\n" % 
                 (os.getpid(), pid)).encode())

  args = ["wc", "declaration.txt"]

  #looks for built in command
  for dir in re.split(":", os.environ['PATH']): # try each directory in the path
    program = "%s/%s" % (dir, args[0])          #set to the directore+filename
    os.write(1, ("Child:  ...trying to exec %s\n" % program).encode())

    try:
      os.execve(program, args, os.environ) # try to exec program

    except FileNotFoundError:             # ...expected
      pass                              # ...fail quietly
    
 #for -1 ioType, do not do anything besides running proram
 #for 0 ioType, store output in righthand file
 if (ioType = 0):
    os.close(1)                 # redirect child's stdout

    #open the output file for writing
    sys.stdout = open(userArgs[(userArgs.index(">"))+1], "w")
    fd = sys.stdout.fileno() # os.open("p4-output.txt", os.O_CREAT)
    os.set_inheritable(fd, True)
    os.write(2, ("Child: opened fd=%d for writing\n" % fd).encode())

    for dir in re.split(":", os.environ['PATH']): # try each directory in path
        program = "%s/%s" % (dir, userArgs[(userArgs.index(">"))-1])
        try:
            os.execve(program, args, os.environ) # try to exec program
        except FileNotFoundError:             # ...expected
            pass                              # ...fail quietly 

    os.write(2, ("Child:    Error: Could not exec %s\n" % args[0]).encode())
    sys.exit(1)                 # terminate with error

 #for 1 ioType, use righthand file as input for lefthand file
 #for 2 ioType, use rightHand output as input for righthand file
    
 
  #if file not found, exit with error.
  os.write(1, ("Child:    Could not exec %s\n" % args[0]).encode())
  sys.exit(1)                 # terminate with error

else:                           # parent (forked ok)

  os.write(1, ("I am parent after forking.  My pid=%d.  Child's pid=%d\n" % (pid, rc)).encode())


