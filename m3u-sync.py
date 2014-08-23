#!/usr/bin/env python3

from os import listdir, getcwd
from os.path import join, relpath, dirname, exists
from shutil import copy2
import sys
from os import walk, makedirs, remove
import os
import hashlib

def getMD5(filename):
    return hashlib.md5(open(filename).read()).hexdigest()

def parseM3U(path):
    playlist = open(path,"r")
    files = []
    for line in playlist:
        if line.startswith("#"):
            continue
        files.append(relpath(line,sys.argv[2]).strip())
    return files


def removeEmptyFolders(path):
  if not os.path.isdir(path):
    return

  # remove empty subfolders
  files = os.listdir(path)
  if len(files):
    for f in files:
      fullpath = os.path.join(path, f)
      if os.path.isdir(fullpath):
        removeEmptyFolders(fullpath)

  # if folder empty, delete it
  files = os.listdir(path)
  if len(files) == 0:
    print("Removing empty folder:", path)
    os.rmdir(path)


def main():
	# Artist folders will be directly in dest folder
	# -> copies subtree from path-to-music on to path-to-dest
    if len(sys.argv) < 4:
        print("Usage: m3u-sync.py <path-to-dest> <path-to-music> <m3u-file> [--update]")
        return
    # update changed files
    shouldUpdate = False
    
    if len(sys.argv) == 5:
        if sys.argv[4] == "--update":
            shouldUpdate = True
    
    files = []
    for (dirpath, dirnames, filenames) in walk(sys.argv[1]):
        for file in filenames:    
            files.append(relpath(join(dirpath,file),sys.argv[1]))

    playlist = parseM3U(sys.argv[3])

    # delete files no longer wanted
    for f in files:
        if not f in playlist:
            path = join(sys.argv[1],f)
            print("Removing: ",path)
            remove(path)
            
    # clean empty dirs
    removeEmptyFolders(sys.argv[1])
    
    # copy new files
    for f in playlist:
        if f in files:
            if shouldUpdate:
                hashOrg = getMD5(join(sys.argv[1],f))
                hashNew = getMD5(join(sys.argv[2],f))
                if hashOrg == hashNew:
                    continue
            else:
                continue
        
        dirs = join(sys.argv[1],dirname(f))
        if not exists(dirs):
            makedirs(dirs)
            
        try:
            print("Copy: ",join(sys.argv[2],f)," -> "+dirs)
            copy2(join(sys.argv[2],f),dirs)
        except Exception:
            print("Not found! Skipping.")
            continue
        
if __name__ == "__main__":
    main()
    
