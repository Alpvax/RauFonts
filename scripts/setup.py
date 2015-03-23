#!/usr/bin/env python
import os, sys, argparse, shutil, subprocess, re, json
from distutils.util import strtobool
        
def getBoolChoice(prompt, default=False):
    choice = raw_input(prompt)
    if not (choice and len(choice) > 0):
        return default
    try:
        return bool(strtobool(choice))
    except ValueError:
        return default
        
def formatArg(match):
    res = match.group(0)
    key = match.group("key")
    if key and key[0] in ("st"):
        res = "{src}"
    if key and key[0] in ("dl"):
        res = "{dst}"
    return res

symlncmd = {"win": "mklink /d {src} {dst}"}#map of platformStrings to directory symlink commands

def symlink(src, dst):
    global symlncmd
    command = None
    os = sys.platform
    for platform in symlncmd:
        if os.startswith(platform):
            command = symlncmd[platform]
    if not command:
        if getBoolChoice("Symbolic linking not yet supported on your platform. Add support? [Yes]/no: ", True):
            platform = raw_input("Enter the string to match your platform. Leave blank to use detected platform [%s]: " % os) or os
            print("Platform string = " + platform)
            command = raw_input("Enter the command used to make a directory symbolic link:\n(use %t and %l as placeholders for target and link):")
            if command and len(command.split(" ")) > 1:
                command = re.sub("(%|\$)(?P<key>\w+)", formatArg, command, re.IGNORECASE)
                with open(__file__, 'r+') as f:
                    lines = f.readlines()
                    f.seek(0)
                    f.truncate()
                    for line in lines:
                        m = re.match("symlncmd = (?P<map>\{.*\})(?P<lineEnd>.*\r?\n?)", line)
                        if m:
                            symlncmd = json.loads(m.group("map"))
                            symlncmd[platform] = command
                            line = "symlncmd = %s%s" % (json.dumps(symlncmd), m.group("lineEnd"))
                        f.write(line)
    if command:
        print(command.format(src=src, dst=dst))
#        subprocess.call(command)

if __name__=="__main__":
    root = os.path.realpath(__file__ + "/../..")
    if not os.path.exists(os.path.join(root, "fonts")):
        os.mkdir(os.path.join(root, "fonts"))
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--force", action="store_true", help="Overwrite any existing fonts directory without asking")
    parser.add_argument("-r", "--rename", action="store_true", help="Make a copy of the existing fonts directory. Automatically applies -f")
    parser.add_argument("directory", help="The path to the local RauCore repository root")
    args = parser.parse_args()
    core = os.path.realpath(args.directory)
    f = os.path.join(core, "fonts")
    flag = True
    if os.path.exists(f):
        if args.rename:
            print("Renaming " + f + " to " + f + "_old")
            os.rename(f, f + "_old")
        else:
            flag = args.force or getBoolChoice(f + " already exists, do you wish to overwrite it? [y/N]")
            if flag:
                if os.path.islink(f):
                    os.unlink(f)
                elif os.path.isdir(f):
                    shutil.rmtree(f)
                else:
                    os.remove(f)
            else:
                print("Unable to finish setup: " + f + "already exists")
    if flag:
        src = os.path.join(root, "fonts")
        if not os.path.exists(src):
            os.mkdir(src)
        print("Creating symlink " + f + " -> " + src)
        symlink(src, f)
