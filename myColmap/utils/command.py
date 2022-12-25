#!/usr/bin/env python
#! -*- encoding: utf-8 -*-

import subprocess
import os, sys
from utils.paths import getColmapPath

def runCommand(binary, command_args):
    print("Running process '%s'" % (' '.join([binary, *command_args])))
    sys.stdout.flush()
    completedProcess = subprocess.run([binary, *command_args])

    if completedProcess.returncode == 0:
        print("Process %s completed." % binary)
    else:
        sys.stdout.flush()
        sys.stderr.flush()
        print("Process %s failed with code %d." % (binary, completedProcess.returncode))

    return completedProcess

def getColmap(colmapPath = getColmapPath()):
    
    colmapBinary = os.path.join(colmapPath, "colmap")

    if os.path.isfile(colmapBinary):
        print("Program '%s' found in '%s'." % (colmapBinary, colmapPath))
        return colmapBinary
    else:
        print("Program '%s' not found in '%s'. Aborting." % (colmapBinary, colmapPath))
        return None
