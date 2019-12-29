# video-sync

A script to manage video files between an internal and external hard drive.

**Use on your own risk!**

## Usage

```bash
./video-sync.py SOURCE_FOLDER DESTINATION_FOLDER
```

## What does it do?
Imagine a file structure for files sorted by date. All organizational folders start with at least a two digit number. It's important to only have _either_ organization folders _or_ actual files / data folders in a specific folder, but not both. The objective of this script is to have two identical file structures, BUT only the destination folder necessarily contains all the data. If there is organizational folders in the destination which are not in the source, it will create a symlink. An example usage is when you use Final Cut Pro X for video editing, and you sometimes want to edit with files on the internal hard drive, sometimes with files on the external hard drive, and you want all old projects (where the files where moved to the external drive) to still work.

This is work in progress and it's hard to explain the actual functionality of the script. I will add an example to illustrate this later.
