#FILE OPEN TESTS ---------------------------------------

#change current working directory 
import os
filepath = "C:\\Users\\Till\\Desktop"
os.chdir(filepath)

#check current working directory: with os.getcwd()
import os 
cwd = os.getcwd()
#returns "C:\\Users\\Till\\desktop"

#pyrevit Script to check current working dir
import os 
cwd = os.getcwd()
with open(cwd + "\\test.txt', 'w') as f:
    f.write(cwd + "\\test")
# return: ...C..Autodesk\Revit, Error : Not allowed to write to path. 

print(cwd + "\\test.txt")

#creates the file hello.txt and opens it, https://automatetheboringstuff.com/chapter8/
helloFile = open('C:\\Users\\Till\\Desktop\\hello.txt', "w")
close(helloFile)


#PICKL TEST ------------------------------------------

#PYREVIT return script Path of current script 
from pyrevit import script 
import pickle

favorite_color = { "lion": "yellow", "kitty": "red" }

scriptpath = script.get_script_path()
print(scriptpath)

scriptpathtxt = scriptpath + '\\dic_ps.txt'
with open('dic_ps.txt', 'wb') as f:
    pickle.dump(favorite_color, f)

pickle.dump( favorite_color, open( "save.p", "wb" ) )

#Load it back
favorite_color = pickle.load( open( "save.p", "rb" ) )

# favorite_color is now { "lion": "yellow", "kitty": "red" }

#Tests

import pickle
favorite_color = { "lion": "yellow", "kitty": "red" }

with open('dic.txt', 'wb') as f:
    pickle.dump(favorite_color, f)

#Test End, works!!

#Now check: when script is run what the cwd is. Is it the scriptpath? 

import cPickle as pickle
with open('scriptpath\\dic_ps.txt', 'wb') as f:
    pickle.dump(object, f)

#PYREVIT return script Path of current script 
from pyrevit import script 
scriptpath = script.get_script_path()


#---------------------------------------------------------
# What does r, r+, w, w+, a, a+ mean? StackOverflow

# Same info, just in table form

                  # | r   r+   w   w+   a   a+
# ------------------|--------------------------
# read              | +   +        +        +
# write             |     +    +   +    +   +
# write after seek  |     +    +   +
# create            |          +   +    +   +
# truncate          |          +   +			abschneiden, kürzen 
# position at start | +   +    +   +
# position at end   |                   +   +

# where meanings are: (just to avoid any misinterpretation)

    # read - reading from file is allowed
    # write - writing to file is allowed
    # create - file is created if it does not exist yet
    # trunctate - during opening of the file it is made empty (all content of the file is erased)
    # position at start - after file is opened, initial position is set to the start of the file
    # position at end - after file is opened, initial position is set to the end of the file

# Note: a and a+ always append to the end of file - ignores any seek movements.
# BTW. interesting behavior at least on my win7 / python2.7, for new file opened in a+ mode:
# write('aa'); seek(0, 0); read(1); write('b') - second write is ignored
# write('aa'); seek(0, 0); read(2); write('b') - second write raises IOError

# The options are the same as for the fopen function in the C standard library:

# w truncates the file, overwriting whatever was already there
# a appends to the file, adding onto whatever was already there
# w+ opens for reading and writing, truncating the file but also allowing you 
# to read back what's been written to the file

# a+ opens for appending and reading, allowing you both to append to the 
# file and also read its contents

# I hit upon this trying to figure out why you would use mode 'w+' versus 'w'. 
# In the end, I just did some testing. I don't see much purpose for mode 'w+', 
# as in both cases, the file is truncated to begin with. However, with the 'w+',
# you could read after writing by seeking back. If you tried any reading with 'w', 
# it would throw an IOError. Reading without using seek with mode 'w+' isn't
# going to yield anything, since the file pointer will be after where you have written.


# On Windows, 'b' appended to the mode opens the file in binary mode, 
# so there are also modes like 'rb', 'wb', and 'r+b'. 

# Python on Windows makes a distinction between text and binary files; 
# the end-of-line characters in text files are automatically altered slightly 
# when data is read or written. 
# This behind-the-scenes modification to file data is fine for ASCII text files,
# but it’ll corrupt binary data like that in JPEG or EXE files. Be very careful 
# to use binary mode when reading and writing such files. 
# On Unix, it doesn’t hurt
# to append a 'b' to the mode, so you can use it platform-independently for 
# all binary files.



