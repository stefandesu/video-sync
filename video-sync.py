#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import re

'''
Usage:
./video-sync SOURCE_FOLDER DESTINATION_FOLDER
'''

# regular expression to find folders in format yyyy-mm-something
yyyy_mm_regex = re.compile(r'\d{2}.*')

def get_volume_root(path: str) -> str:
    while not os.path.samefile(os.path.dirname(path), "/Volumes"):
        path = os.path.dirname(path)
    return path

def main(argv):
    # check command line parameters
    print(argv)
    if len(argv) != 2:
        print("I need exactly 2 parameters, the source path and the destination path.")
        exit()

    source_path = argv[0]
    destination_path = argv[1]

    # if source_path[-1] == "/":
    #     source_path = source_path[:-1]
    # if destination_path[-1] == "/":
    #     destination_path = destination_path[:-1]
    source_path = os.path.realpath(source_path)
    destination_path = os.path.realpath(destination_path)
    destination_root = get_volume_root(destination_path)
    backup_path = os.path.join(destination_root, "backups", "sync")

    print("### Synchronizing the following folders: ###")
    print("Source:", source_path)
    print("Destination:", destination_path)
    print("Destination root:", destination_root)
    print("Destination backup path:", backup_path)

    folders_destination = find_folders(destination_path)
    print("destination:", folders_destination)

    # create symlinks for all folders in destination which are not in source
    for folder in folders_destination:
        folder_source = folder.replace(destination_path, source_path)
        if not os.path.exists(folder_source):
            if not os.path.exists(os.path.dirname(folder_source)):
                os.makedirs(os.path.dirname(folder_source))
            try:
                os.symlink(folder, folder_source)
            except:
                print("Error creating symlink:")
                print(folder)
                print(folder_source)
                exit()
            print("created symlink:", folder, folder_source)

    print()
    existing_folders = list(map(lambda f: f.replace(destination_path, source_path),folders_destination))
    # print ("existing folders:", existing_folders)
    folders_source = find_folders(source_path, existing_folders)
    print("source:", folders_source)

    # synchronize all non-symlinks from source with destination
    for folder in folders_source:
        if os.path.islink(folder) or os.path.isfile(folder):
            continue
        folder_dest = folder.replace(source_path, destination_path)
        if not os.path.exists(folder_dest):
            os.makedirs(folder_dest)
        rsync_args = "-atu --exclude=\"Render Files\" --exclude=\"Transcoded Media\" --backup --backup-dir=\""+backup_path+"\""

        command = "rsync "+rsync_args+" \""+folder+"\" \""+os.path.dirname(folder_dest)+"\""
        # print(command)
        os.system(command)

        command = "rsync "+rsync_args+" \""+folder_dest+"\" \""+os.path.dirname(folder)+"\""
        # print(command)
        os.system(command)
    
    # Show tree for backup path
    print()
    print("### Tree for " + backup_path + " ###", flush=True)
    os.system("tree \"" + backup_path + "\"")

def find_folders(root, existing_folders = []):
    is_leaf = True
    folders = []
    if os.path.isfile(root):
        return [root]
    for item in os.listdir(root):
        if (yyyy_mm_regex.match(item) != None or item == "_inbox") and os.path.isdir(os.path.join(root, item)) and not item.endswith(".fcpbundle") and not item.endswith(".pxd") and (not os.path.islink(os.path.join(root, item)) or os.path.join(root, item) in existing_folders):
            is_leaf = False
            folders += find_folders(os.path.join(root, item), existing_folders)
    if is_leaf:
        return [root]
    else:
        return folders

if __name__ == "__main__":
   main(sys.argv[1:])
