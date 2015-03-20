#!/usr/bin/env python
import os, sys, argparse, shutil, subprocess
from distutils.util import strtobool
        
def getBoolChoice(prompt):
    try:
        return strtobool(raw_input(prompt))
    except ValueError:
        return 0
        
if __name__=="__main__":
    root = os.path.realpath(__file__ + "/../..")
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--force", action="store_true", help="Overwrite any existing fonts directory without asking")
    parser.add_argument("-r", "--rename", action="store_true", help="Make a copy of the existing fonts directory. Automatically applies -y")
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
        subprocess.call(["ln", "-s", src, f])
