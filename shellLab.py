#! /usr/bin/env python3

import os, sys, time, re

pid = os.getpid()
#os.write(1, ("type>").encode())
userIn = " "

#would i have to put everything inside this loop so the shell continues to repeat?
#while (userIn == " " or userIn == ""):
while (userIn != "exit"):
  os.write(1, ("type>").encode())
  userIn = input('')
  os.write(1, ("The user inputted %s \n" %userIn).encode())
  #so from here take in a string and seperate based on white space

  os.write(1, ("ABOUT TO FORK (pid:%d)\n" % pid).encode())
rc = os.fork()

#Error for fork
if rc < 0:
    os.write(2, ("fork failed, returning %d\n" % rc).encode())
    sys.exit(1)

#inherits anything already taken in before this point
#so here I would execute whatever is typed and then after i would kill and return
elif rc == 0:                   # child

    os.write(1, ("I am in child and can see the input:%s \n" %userIn).encode())
    os.write(1, ("Child: My pid==%d.  Parent's pid=%d\n" % 
                 (os.getpid(), pid)).encode())

    args = ["wc", "p4-redirect.py"]
    for dir in re.split(":", os.environ['PATH']): # try each directory in the path
        program = "%s/%s" % (dir, args[0])
        os.write(1, ("Child:  ...trying to exec %s\n" % program).encode())
        try:
            os.execve(program, args, os.environ) # try to exec program
        except FileNotFoundError:             # ...expected
            pass                              # ...fail quietly

    #args2 = ["p1-fork.py" , "wordCount.txt"]
    #os.execve("wordCount" ,args2, os.environ)
    os.write(1, ("Child:    Could not exec %s\n" % args[0]).encode())
    sys.exit(1)                 # terminate with error

else:                           # parent (forked ok)

    os.write(1, ("I am parent after forking.  My pid=%d.  Child's pid=%d\n" % (pid, rc)).encode())


