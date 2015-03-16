#!/usr/bin/env python
import fontforge
import json
import os, sys, getopt
import re

basepath = os.path.dirname(__file__)
def relPath(rpath):
    return os.path.abspath(os.path.join(basepath, rpath))
    
def getVersion(names):
    version = 0
    for i in range(len(names)):
        if os.path.isfile(names[i]):
            font = fontforge.open(names[i])
        else:
            font = fontforge.font()
        version = max(version, int(font.version.split(".")[1]))
    return version
        
def main():
    names = ["rau-utf.ttf"]
    data = json.load(open(relPath("../build_data.json"), 'r'))
    types = data["Rune Types"]
    runes = data["Basic Runes"]
    version = getVersion(names) + 1
    for i in range(len(names)):
        font = fontforge.font()
        font.version = str(i + 1) + "." + str(version)
        flag = False
        svgPath = relPath("../svgs")
        for svg in os.listdir(svgPath):
            base = svg[:-4]
            print(base)
            imod = 0
            if re.match(".+_p", svg.lower()):
                base = base[:-2]
                imod = 1
            if base in runes:
                rune = runes[base]
                index = rune["index"] + imod + types[rune["type"]][i]
                print("Adding rune " + svg + " with index " + str(index))
                glyph = font.createChar(index)
                glyph.importOutlines(os.path.join(svgPath, svg))
                flag = True
        if flag:
            print("Generating font with name: " + names[i] + " and version: " + font.version)
            font.generate(names[i])
                
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
