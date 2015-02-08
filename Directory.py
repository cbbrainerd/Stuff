#!/usr/bin/python
import operator
from optparse import OptionParser
import os

def human(siz):
    j = 0
    markers = ["B","kB","MB","GB","TB","PB", "EB", "ZB", "YB", "..."]
    if (siz < 1025):
        return(str(siz)+markers[0])
    siz = siz*10
    while (siz > 10240):
        siz = siz/1024
        j += 1
        if (j > 9):
            return("This file is way too big to actually exist.")
    return(str(siz/10)+"."+str(siz%10)+markers[j])    

def manual():
    #Manual
    print("Lists the contents of a selected directory. Note that the types only function properly on a Linux machine.")
    print("Available options:")
    print("-d[directory]: required. Both absolute paths and paths relative to the current working directory are acceptable.")
    print("-a: Sorts by size in ascending order. By default, this program sorts by size in descending order.")
    print("-t: Sorts by type. If both this and -a are selected, -a is ignored.")
    print("-r: Run as root. Requires root priveleges, of course.")
    quit()

def whatTypeAmI(path):
    if (os.path.isdir(path)):
        return("Directory")
    elif (os.access(path,os.X_OK)):
        return("Executable") #This really returns whether execution is permitted for the current user, but that's what matters anyway, right?
    else:
        return("File")


def printDir(direct):
    if(not (os.path.isdir(direct))):
        print "Requested directory \""+direct+"\" is not a valid directory. If you need help, run this command with no flags to see the help file."
        quit()
    #Print directory
    a= os.listdir(direct)
    if (options.typee):
        types = {}
        for i in a:
            types[i] = whatTypeAmI(i)
        for x in sorted(types, key=types.get):
            print x, human(os.path.getsize(direct+"/"+x)), types[x]
    else:
        size = {}
        for i in a:
            size[i] = os.path.getsize(direct+"/"+i)
        for x in sorted(size, key=size.get, reverse=options.descending):
            print x, human(size[x]), whatTypeAmI(x)
    quit()

p = OptionParser()
p.add_option("-d", type="string", action="store", dest="filename",default="/dev/null")
p.add_option("-a", action="store_false", dest="descending",default=True)
p.add_option("-t", action="store_true", dest="typee", default=False)
p.add_option("-r", action="store_false", dest="notroot", default=True)
(options, args) = p.parse_args()

if ((os.geteuid() == 0) and options.notroot):
    print "Why are you running this as root?"
    print "If you meant to do this as root, please run with the flag -r."
    quit()
if ((os.geteuid() != 0) and not options.notroot):
    print "This requires root priveleges."
    print "Please run as root or run without the -r flag."
    quit()
if ((options.filename == "/dev/null") or (len(options.filename) == 0)):
    manual()
if (options.filename[0] == "~"):
    if (len(options.filename) == 1):
        printDir(os.getenv("HOME"))
    elif (options.filename[1] == "/"):
        printDir(os.getenv("HOME"))
    else:
        userhome = (options.filename.split("~",1)[1].split("/",1))
        if ((len(userhome) == 2) and (len(userhome[1]) != 0)):
            printDir("/home/"+userhome[0]+"/"+options.filename.split("/",1)[1])
        else:
            printDir("/home/"+userhome[0])
printDir(options.filename)
