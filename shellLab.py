#! /usr/bin/env python3

import os, sys, time, re
import stat #for changing file permissions

pid = os.getpid()
userIn = " "

while ( (userIn == " " or userIn == "") and userIn != "exit"):

#works but kinda glitchy
#while (userIn != "exit"):
  os.write(1, ("type>").encode())
  userIn = input('')
  #os.write(1, ("The user inputted %s \n" %userIn).encode())
  #so from here take in user input and seperate based on white space
  userArgs = userIn.split();
  print ("why is this not working %s", userArgs)

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
  
    #time.sleep(2) #but for what purpose
  
    #store left's output to right's file
    ioType = -1
    if ">" in userArgs:
      #print(">, args 1 executes, arg2 stores")
      ioType = 0
      print("input file is ", userArgs[(userArgs.index(">"))-1])
      print("output file is ", userArgs[(userArgs.index(">"))+1])

    #use right file as input for the left's  
    elif "<" in userArgs:
      ioType = 1
      print("< detected")
      print("index is", userArgs.index("<"))

    #use left file's output as the input for the right
    #for piping, you must have 2 children?? one to execute the left
    #and the other to take that output as input for the right
    elif "|" in userArgs:
      ioType = 2
      print("| detected")
      print("index is", userArgs.index("|"))

      
    os.write(1, ("Child: My pid==%d.  Parent's pid=%d\n" % 
                 (os.getpid(), pid)).encode())
    args2 = ["wc", "declaration.txt"]
    #can store everything in the lefthand side as args???
  
    #for >/0 ioType, store output in righthand file
    #store left's output to right's file
    #need to incorperate execution of python files
    if (ioType == 0):
      path = '.'
      hmm = os.listdir(path)
      print(hmm)
      args = userArgs[0:(userArgs.index(">"))]
      #print(args)
      os.close(1)                 # redirect child's stdout
      #open the output file for writing
    
      sys.stdout = open(userArgs[(userArgs.index(">"))+1], "w")
      fd = sys.stdout.fileno() # os.open("p4-output.txt", os.O_CREAT)
      os.set_inheritable(fd, True)
      os.write(2, ("Child: opened fd=%d for writing\n" % fd).encode())

      #finds lefthandfile to execute
      #NEED TO MAKE IT SO THAT THE ENTIRE LEF TIS ARGS AND THE RIGHT IS INPUT!!
      #if there is a slash it would exec directory ./ can work for it
      for dir in re.split(":", os.environ['PATH']): # try each directory in path
         program = "%s/%s" % (dir, userArgs[0])
         try:
           os.execve(program, args, os.environ) # try to exec program
         except FileNotFoundError:             # ...expected
           #try
             program = "./"+ userArgs[0]
             st = os.stat(program)
             os.chmod(program, st.st_mode | stat.S_IEXEC)
             os.execve(program,args,os.environ)
           #except:
            # pass                              # ...fail quietly 
             os.write(2, ("Child:    Error: Could not exec %s\n" % args[0]).encode())
      sys.exit(1)                 # terminate with error

    #for </1 ioType, use righthand file as input for lefthand file
    #use right file as input for the left's
    #need to incorperate execution of python files
    elif (ioType == 1):
      args = userArgs[0]+" "+userArgs[(userArgs.index("<")+1)]
      args = args.split()
      print(args)
      #args = [userArgs[(userArgs.index("<"))-1], userArgs[(userArgs.index("<"))+1]]
      for dir in re.split(":", os.environ['PATH']): # try each directory in the path
        program = "%s/%s" % (dir, userArgs[0])
        os.write(1, ("Child:  ...trying to exec %s\n" % program).encode())
        try:
          os.execve(program, args, os.environ) # try to exec program
        except FileNotFoundError:             # ...expected
          pass                              # ...fail quietly

      os.write(2, ("Child:    Could not exec %s\n" % args[0]).encode())
      sys.exit(1)                 # terminate with error

    #for |/2 ioType, use leftHand output as input for righthand file
    #use left file's output as the input for the right
    #for piping, you must have 2 children?? one to execute the left
    #and the other to take that output as input for the right
    #Os.fork inside of here and have a child of a child execute the second half
    elif (ioType == 2):
      print("in io2")
      
    #else:
      #print("no IO")
    
    
  else:                           # parent (forked ok)
    os.write(1, ("I am parent after forking.  My pid=%d.  Child's pid=%d\n" % (pid, rc)).encode())


