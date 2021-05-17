# virus.sh

`virus.sh` is a terminal-style game in which you have to remove a virus* from the filesystem
and restore the files that the virus deleted.

***_The virus is not a real virus and is not messing with your computer in any way whatsoever._**

## The Filesystem
The filesystem you see is merely a randomly generated filesystem where the names of directories
and files are obfuscated, on purpose, which makes it more difficult to find the virus.
There is no exact amount of files that are on the system as it is randomly generated
so you could be dealing with a fake filesystem of between 16,000 and 28,000 files in total.

## The Virus
The virus is split up into however many files you have divided by 1000:
* 16,000 files = 16 virus files
* 27,905 files = 27 virus files
* 20,999 files = 20 virus files

## The Goal
Your goal is to delete all the virus files in sequential order before the virus
deletes all the files on the system.

To start off, each file of the virus takes a turn deleting a random file, every 60 seconds, on the system
but not in any particular order. For example, here's how it could happen:
* Virus file 5 deletes a file
* Virus file 20 deletes a file
* Virus file 17 deletes a file

and so on...

### The Difficult Part
If you delete a virus file that wasn't supposed to be deleted yet, (let's say you deleted
virus file 4 last, and then you delete virus file 6, but not 5), then that virus file will be 
randomly relocated somewhere else on the system, and a new virus file will be added for you to delete.

In addition, every time you make this mistake, the virus deletes files quicker by 3 seconds.
Don't worry though, the quickest time the virus ends up deleting a file is 3 seconds.
Once you reach that, you have very limited time as this time will never increase again.

### After the Virus is gone
Once you have successfully removed all the virus files from the system,
you must also restore the files to where they originally came from.

## Commands
The commands that you can use include some actual commands that are used in 
`zsh` and `bash` but there are a few custom commands that don't actually exist in them
which will all be described below:

* `ls` - Lists the directory you are currently in, or a directory that you specify
* `cd` - Changes the current directory to one you specify
* `rm` - Removes a file or directory from the filesystem (This should only be used with virus files but can also be used on regular files)
* `cat` - Prints out a files contents. (Note: This version of the `cat` command will only print out confusing-looking HEX bytes instead of actual text \[Use the `tutorial` command if you're confused])
* `restore` - Restores a file that was deleted by the virus to its original location
* `trace` - Traces a deleted file to show what the source of its deletion was. If it was by a virus file, it will show the second-level parent directory that is above it)
    * For example, if a virus exists like this `/root/usr/bin/temp/virus_file.py`, then it will only return `/root/usr/bin`
    * This just makes it a little more difficult rather than giving you the folder that it came in
* `mntr` - This will display the last deleted file, and it will show how quickly files are being deleted from the system. 
  In addition, information about the deleted/remaining virus files and restored/deleted files will appear.
* `track` - You can use this to manually keep track of the virus files and where they exist, if you've already found one before that you can't delete yet.
* `exit` - If you run this command while in a game, it will save your progress and return you to the main menu. If you run this from the main menu, you will exit the game overall.

## Feedback and Suggestions
Any feedback and suggestions can be reported directly to their proper issues on this GitHub.

Here are links to make it easier: **(Links coming soon)**
* Report Bug
* Make a Suggestion