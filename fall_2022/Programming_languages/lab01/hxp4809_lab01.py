'''
name: Hoang Anh Kiet Pham
Id: 1001904809
language version: python 3.8.10
OS: Ubuntu (UTA virtual machine)
'''

import os
'''
this function is to calculate the size of the current working directory
'''
def get_total_size_of_dir(dir):
    os.chdir(dir) #cd to sub directory
    entries = os.listdir() #get the list of all entry
    sum = 0
    for entry in entries:
        if os.path.isfile(entry):
            # print("file: " + entry) #for debug
            sum += os.path.getsize(entry)
        else:
            # print("dir: " + entry) #for debug
            sum += get_total_size_of_dir(entry) #recursively call this function
            os.chdir("..")
    return sum


#main function
total = get_total_size_of_dir(".")
print(total)

'''
extra question
1) was one language easier or faster to write the code for this?
if so, describe in detail why, as in what about the language made that the case
- for me, python and java aare easier and faster to work on this assignment
because they only require 1 library/class (File in java, os in python)
that provide every tools I need for this. Meanwhile, C is a little trickier.
It requires me to know more library (stat, file) and syntax than the others two.
Python is actually a little easier than java because it's a interpreted language
and very closed to human language.

2)Even though a langauge may not (e.g. FORTRAN) support recursion,
describe how you could write a program to produce the same results without using recursion.
Would that approach have any limitations and if so, what would they be?
- if the language don't support recursion, I would need to build a data structure (either stack or queue)
and process iteratively the file tree.
- This apprack would require us to write more complicated code
and need to handle the data passing around very carefully
- for some problem, figured the based case (conditon to stop the loop) is very difficult.
'''