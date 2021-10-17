# README

Ever used a Hobonichi Journal? Ever wished you can slap some photos to the calendar pages but it was too much of a chore to shrink photos, and then print them? Well, this is a series of python scripts might be the solution you're looking for

What this project does is it take a series of photos in a directory, shrinks them to the appropriate thumbnail which makes the hobonichi calendar size, and then combines all the thumbnails into one image that you can then print on a 8.5"X11" paper (or whatever size)

# Requirements:

- Python3 (tested with python 3.9.7)
- PIL
- Photos that you want to turn into thumbnails. Preferably in a separate directory.
- A photo printer (alternatively, go to a photo printing service)

# How to Use

- open up a command prompt with either powershell (windows) or bash (Mac, Linux)
- execute the hobonichi calendar script via "python hobonichi_calendar.py"
- when prompted to, copy and paste the directory path to the photos (ie /Users/Alex/Photos/ or C:\Users\Document\Photos\)
- If the work has been completed successfully, a Final_print.jpg will be generated that contains all the thumbnails. You can then print this out on a printer.
