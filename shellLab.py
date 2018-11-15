#! /usr/bin/env python3

import os, sys, time, re
import stat #for changing file permissions
import fileinput #for piping

pid = os.getpid()
userIn = " "

pr,pw = os.pipe()
for f in (pr, pw):
  os.set_inheritable(f, True)
print("pipe fds: pr=%d, pw=%d" % (pr, pw))

#while ( (userIn == " " or userIn == "") and userIn != "exit"):
while (userIn != "exit"):
  os.write(1, ("type>").encode())
  userIn = input('')
  
  userArgs = userIn.split();
  
  os.write(1, ("ABOUT TO FORK (pid:%d)\n" % pid).encode())
  rc = os.fork()

  #Error for fork
  if rc < 0:
    os.write(2, ("fork failed, returning %d\n" % rc).encode())
    sys.exit(1)

  elif rc == 0:                   # child
    ioType = -1
    #time.sleep(2) #but for what purpose
  
    #store left's output to right's file
    if ">" in userArgs:
      ioType = 0

    #use right file as input for the left's  
    elif "<" in userArgs:
      ioType = 1

    #use left file's output as the input for the right
    elif "|" in userArgs:
      ioType = 2
      
      os.write(1, ("Child: My pid==%d.  Parent's pid=%d\n" % 
                 (os.getpid(), pid)).encode())
    args2 = ["wc", "declaration.txt"]
    succesfulRun = 0
  
    #for >/0 ioType, store leftHandoutput in righthand file
    if (ioType == 0):
      args = userArgs[0:(userArgs.index(">"))]
      os.close(1)                 # redirect child's stdout
      sys.stdout = open(userArgs[(userArgs.index(">"))+1], "w") #open output file
      fd = sys.stdout.fileno() # os.open("p4-output.txt", os.O_CREAT)
      os.set_inheritable(fd, True)
      os.write(2, ("Child: opened fd=%d for writing\n" % fd).encode())

      #finds lefthandfile to execute
      for dir in re.split(":", os.environ['PATH']): # try each directory in path
         program = "%s/%s" % (dir, userArgs[0])
         try:
           os.execve(program, args, os.environ) # try to exec program
         except FileNotFoundError:             # ...expected
           pass

      if (succesfulRun == 0):
        try:
          program = "./"+ userArgs[0]
          st = os.stat(program)
          os.chmod(program, st.st_mode | stat.S_IEXEC)
          os.execve(program,args,os.environ) 
        except FileNotFoundError:
          print ("file nout found")
          pass
        
      os.write(2, ("Child:    Could not exec %s\n" % args[0]).encode())
      sys.exit(1)                 # terminate with error

      
    #for </1 ioType, use righthand file as input for lefthand file
    elif (ioType == 1):
      args = userArgs[0]+" "+userArgs[(userArgs.index("<")+1)]
      args = args.split()
      print(args)
      
      for dir in re.split(":", os.environ['PATH']): # try each directory in the path
        program = "%s/%s" % (dir, userArgs[0])
        os.write(1, ("Child:  ...trying to exec %s\n" % program).encode())
        try:
          os.execve(program, args, os.environ) # try to exec program
        except FileNotFoundError:             # ...expected
          pass 

      if (succesfulRun == 0):
        try:
          program = "./"+ userArgs[0]
          st = os.stat(program)
          os.chmod(program, st.st_mode | stat.S_IEXEC)
          os.execve(program,args,os.environ) 
        except FileNotFoundError:
          pass

      os.write(2, ("Child:    Error: Could not exec %s\n" % args[0]).encode())
      sys.exit(1)                 # terminate with error

    #for pipe '|' ioType, use leftHand output as input for righthand file
    elif (ioType == 2):
      os.close(1)                 # redirect child's stdout
      args = userArgs[0]+" "+userArgs[(userArgs.index("|")+1)]
      args = args.split()

      os.dup(pw)
      for fd in (pr, pw):
        os.close(fd)
      print("hello from child")
      

      for dir in re.split(":", os.environ['PATH']): # try each directory in the path
        program = "%s/%s" % (dir, userArgs[0])
        try:
          os.execve(program, args, os.environ) # try to exec program
        except FileNotFoundError:             # ...expected
             pass 

      if (succesfulRun == 0):
        try:
          program = "./"+ userArgs[0]
          st = os.stat(program)
          os.chmod(program, st.st_mode | stat.S_IEXEC)
          os.execve(program,args,os.environ) 
          #os.write(2, ("Child:    Error: Could not exec %s\n" % args[0]).encode())
        except FileNotFoundError:
          pass

    
      else:
        for dir in re.split(":", os.environ['PATH']): # try each directory in the path
          program = "%s/%s" % (dir, userArgs[0])
          #os.write(1, ("Child:  ...trying to exec %s\n" % program).encode())
          try:
            os.execve(program, args, os.environ) # try to exec program
          except FileNotFoundError:             # ...expected
            pass 

        if (succesfulRun == 0):
          try:
            program = "./"+ userArgs[0]
            st = os.stat(program)
            os.chmod(program, st.st_mode | stat.S_IEXEC)
            os.execve(program,args,os.environ) 
          
          except FileNotFoundError:
            pass
        print("program execution failed")
        sys.exit(1)
    
  else:                           # parent (forked ok)
    print("Parent: My pid==%d.  Child's pid=%d" % (os.getpid(), rc), file=sys.stderr)
    os.close(0)
    os.dup(pr)
    for fd in (pw, pr):
        os.close(fd)
