#!/usr/bin/env python
import fontforge
import json
import os
import re
basepath = os.path.dirname(__file__)
def relPath(rpath):
    return os.path.abspath(os.path.join(basepath, rpath))
    
names = [relPath("/../fonts/rau-utf.ttf")]
if __name__ == "__main__":
    fonts = []
    version = 0
    for i in range(len(names)):
        print(i)
        if os.path.isfile(names[i]):
            font = fontforge.open(names[i])
        else:
            font = fontforge.font()
        fonts.append(font)
        version = max(version, int(font.version.split(".")[1]))
    print("version: " + str(version))
    data = json.load(open(relPath("../setup_data.json"), 'r'))
    types = data["Rune Types"]
    runes = data["Basic Runes"]
    for file in os.listdir(relPath("../svgs")):
        print(file)
        base = file
        if re.match("(p(illared)?_?).+", file.lower()) or re.match(".+(_?p(illared)?)", file.lower()):
            base = re.sub("_?p(illared)?_?", "", file)
            print("pillared version of " + base)
            if base in runes:
                rune = runes[base]
                print(rune)
                print(rune['type'])
                print(types[rune['type']])
            
