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
        
def buildFont(version, name, src=None):
    if src:
        font = fontforge.open(src)
    else:
        font = fontforge.font()
    font.familyname = "RAU"
    font.fontname = font.fullname = name.replace("-","_")
    font.version = str(version + 1) + "." + str(version)
    font.copyright = u"Copyright \u00a9 " + str(date.today()) + ", Automatically built."
    if src:
        font.copyright += "Based upon " + src.split("/")[-1] + ". Do not distribute."
    flag = False
    svgPath = relPath("../svgs")
    for svg in os.listdir(svgPath):
        base = rname = svg[:-4]
        print(base)
        imod = 0
        if re.match(".+_p", svg.lower()):
            base = base[:-2]
            imod = 1
        if base in runes:
            rune = runes[base]
            index = rune["index"] + imod + types[rune["type"]][version]
            print("Adding rune " + rname + " with index " + str(index))
            glyph = font.createChar(index, rname)
            glyph.importOutlines(os.path.join(svgPath, svg))
            flag = True
    if flag:
        print("Generating font with name: " + name + " and version: " + font.version)
        font.generate(name)
        font.close()
        
def main():
    names = ["rau-128.ttf","rau-utf.ttf"]
    version = getVersion(names) + 1
    for i in range(len(names)):
        buildFont(i, names[i])
    
if __name__ == "__main__":
    data = json.load(open(relPath("../build_data.json"), 'r'))
    types = data["Rune Types"]
    runes = data["Basic Runes"]
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            buildFont(1, "rau_" + arg.split("/")[-1], src=arg)
    else:
        main()
