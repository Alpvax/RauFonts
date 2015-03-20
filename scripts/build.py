#!/usr/bin/env python
import fontforge
import json
import os, sys, getopt
import re
from datetime import date

basepath = os.path.dirname(__file__)
def relPath(rpath):
    return os.path.abspath(os.path.join(basepath, rpath))
    
def getVersion(names):
    version = -1
    for i in range(len(names)):
        if os.path.isfile(names[i]):
            version = max(version, int(fontforge.open(names[i]).version.split(".")[1]))
    return version
        
def main():
    names = ["rau-128.ttf","rau-utf.ttf"]
    data = json.load(open(relPath("../build_data.json"), 'r'))
    types = data["Rune Types"]
    runes = data["Basic Runes"]
    version = getVersion(names) + 1
    for i in range(len(names)):
        font = fontforge.font()
        font.familyname = "RAU (" + unichr(runes["rau"]["index"] + types[runes["rau"]["type"]][i]) + ")"
        font.fontname = font.fullname = names[i].replace("-","")
        print(font.fontname + "; " + font.fullname)
        font.version = str(i + 1) + "." + str(version)
        font.copyright = u"Copyright \u00a9 " + str(date.today()) + ", Automatically built."
        flag = False
        svgPath = relPath("../svgs")
        for svg in os.listdir(svgPath):
            base = name = svg[:-4]
            print(base)
            imod = 0
            if re.match(".+_p", svg.lower()):
                base = base[:-2]
                imod = 1
            if base in runes:
                rune = runes[base]
                index = rune["index"] + imod + types[rune["type"]][i]
                print("Adding rune " + name + " with index " + str(index))
                glyph = font.createChar(index, name)
                glyph.importOutlines(os.path.join(svgPath, svg))
                flag = True
        if flag:
            print("Generating font with name: " + names[i] + " and version: " + font.version)
            font.generate(names[i])
            font.close()
                
def printUsage(fileName):
    print("Usage:\t" + fileName + " [options]\n" +
        "Options:\n" +
        "-h\t--help\t\tShow this screen\n" +
        "-m\t--message\tThe message to use for committing. Ignored if -c is used\n" +
        "-c\t--no-commit\tDo not commit the repository\n" +
        "-p\t--no-push\tDo not push the repository. Automatically applied by -c\n" +
        "-r\t--no-rebase\tDo not rebase the repository first\n")

def readArgs(argv):
    message = "Updated font"
    commit = True
    push = True
    rebase = True
    try:
        opts, args = getopt.getopt(argv[1:],"hm:cpr",["help","message=","no-commit","no-push","no-rebase"])
    except getopt.GetoptError:
        printUsage(argv[0])
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            printUsage(argv[0])
            sys.exit()
        if opt in ("-m", "--message"):
            message = arg
        if opt in ("-c", "--no-commit"):
            commit = False
        if opt in ("-p", "--no-push", "-c", "--no-commit"):
            push = False
        if opt in ("-r", "--no-rebase"):
            rebase = False
    return message, commit, push, rebase
    
if __name__ == "__main__":
    #message, c,p,r = readArgs(sys.argv)
    main()
