#!/usr/bin/python
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
            return("This file is too big to exist.")
    return(str(siz/10)+"."+str(siz%10)+markers[j])    

def manual():
    #Manual
    print("Don't forget to write a manual...")
    quit()

def whatTypeAmI(path):
    if (os.path.isdir(path)):
        return("Directory")
    elif (os.access(path,os.X_OK)):
        return("Executable")
    else:
        return("File")


def printDir(direct):
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
p.add_option("-d", "--directory", type="string", action="store", dest="filename",default="/dev/null")
p.add_option("-a", "--ascending", action="store_false", dest="descending",default=True)
p.add_option("-t", "--type", action="store_true", dest="typee", default=False)
p.add_option("-r", action="store_false", dest="notroot", default=True)
(options, args) = p.parse_args()

if ((os.geteuid() == 0) and notroot):
    print("Why are you running this as root?")
    print("If you meant to do this as root, please run with the flag -r")
    quit()
if (options.filename == "/dev/null"):
    manual()
if (os.path.isdir(options.filename)):
    printDir(options.filename)
else:
    print("Directory does not exist.")