#!/usr/bin/env python
import os, subprocess

if __name__=="__main__":
    root = os.path.realpath(__file__ + "/../..")
    #runes = "arr,bair,chair,duh,ee,eye,fee,go,na,oo,orr,sjuh,thorr".split(",")# runes with cutouts
    svgPath = os.path.join(root, "svgs")
    files = os.listdir(svgPath)
    total = len(files)
    count = 0
    for svg in files:
        count += 1
        print("Processing file " + str(count) + "/" + str(total))
        command = ["inkscape", os.path.join(svgPath, svg), "--select", "layer1", "--verb", "DialogFillStroke"]
        #subprocess.call(command)
