#!/usr/bin/python

import argparse
import os
import sys
import hashlib
import time

from tqdm import tqdm

#
__author__ = 'Pir00t'
__date__ = 20180828
__version__ = 0.1
__description__ = 'Tool to hash files in specified directory and remove duplicates'

#
'''
Built upon the script outlined here: https://www.pythoncentral.io/finding-duplicate-files-with-python/
'''

def find_dup(working_dir):
    # empty dictionary for duplicates: {hash:[list of paths]}
    duplicates = {}

    for topdir, subdirs, files in os.walk(working_dir):
        print ('Scanning {} ...'.format(topdir))
        paths = [os.path.join(topdir, fname) for fname in files]
        for path in paths:
            # Calculate hash
            file_hash = hashfile(path)
            # Add or append the file path
            if file_hash in duplicates:
                duplicates[file_hash].append(path)
            else:
                duplicates[file_hash] = [path]

    return duplicates

#
def joinDicts(dict1, dict2):
    for key in dict2.keys():
        if key in dict1:
            dict1[key] = dict1[key] + dict2[key]
        else:
            dict1[key] = dict2[key]

#
def hashfile(path, blocksize = 65536):
    with open(path, 'rb') as f:
        hasher = hashlib.sha256()
        buf = f.read(blocksize)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(blocksize)

    return hasher.hexdigest()

#
def dup_delete(dict1):
    results = dict1.values()
    with open("log.txt", "w") as logfile:
        for res in results:
            if len(res) > 1:
                print('\n[+] Duplicates found:\n\n{}'.format(" | ".join(res)))
                logfile.write(" | ".join(res) + '\n')

                for r in res:
                    delete = input('\t[!] Delete {} - y/n: '.format(r))
                    if delete == 'y' or delete == 'Y':
                        os.remove(r)
                        print ('\t[-] Deleted\n')
                    else:
                        continue
            else:
                print ('No duplicate file found: {}'.format("".join(res)))

#
def main():

    print ("\nPy_Clean")
    print ("\nScript by %s" % __author__)
    print ("Current version %s\n" % __version__)

    # Add in argument options
    parser = argparse.ArgumentParser(description="Specify folder(s) to scan")
    parser.add_argument("-f", "--folder", help="Folder(s) to parse", nargs='*')

    # check for arg and input
    if len(sys.argv) <=2:
        parser.print_help()

    args = parser.parse_args()

    if args.folder:
        dirs = args.folder

    # primary dictionary that will contain combined results from all folders provided 
    duplicates = {}

    for d in dirs:
        # check path valid
        if os.path.exists(d):
            dups = find_dup(d)
            joinDicts(duplicates,dups)

        else:
            print ('[!] Error. Invalid directory')

    dup_delete(duplicates)    
    
if __name__ == '__main__':
    main()
