import sys
import unittest
import os.path
import sys
import os
import fnmatch
import nose
#import coverage
'''
Loads all the unit test files from the current directory and executes the test cases in each
file.
'''

# get current working directory
root_path = os.getcwd()    
# default resource paths, used by tests
defaultResourcePath = os.path.join(root_path, "resources")
defaultImagesPath = os.path.join(defaultResourcePath, "images")
defaultSoundsPath = os.path.join(defaultResourcePath, "sounds")

class DummyClass:
	''' A dummy object to pass into methods which check for class attributes '''
	def __init__(self):
		do = None

def resi(filename):
    '''Returns a image resource uri given the filename: resources/images/filename '''
    if not os.path.isabs(filename):
        file = os.path.join(defaultImagesPath, filename)
    else:
        file = filename
    return os.path.abspath(file);

def ress(filename):
    '''Returns a sound resource uri given the filename: resources/sounds/filename '''
    if not os.path.isabs(filename):
        file = os.path.join(defaultSoundsPath, filename)
    else:
        file = filename
    return os.path.abspath(file);

def find(search_root, patterns=None, recurse=0, return_dirs=1):
    '''Finds files/dirs rooted in a given directory that match a pattern.
    
    @param search_root: the root directory for the recursive search
    @param patterns: a list of shell-style patterns to search for
    @param recurse: whether to recurse into sub-directories of searchRoot
    @param return_dirs: whether to return directories that matched the pattern
    @return: a list of files(and possibly directories) rooted in searchRoot
                that match one of the supplied patterns or the empty list
                if no matches are found
    '''
    
    # default to match all files
    if patterns is None:
        patterns = ["*"]
    
    matches = []
    files = []
    dir_contents = os.listdir(search_root)
    # THIS isfile() only works in CWD
    for i in range(len(dir_contents)):
    	if(os.path.isfile(dir_contents[i])):
    		for pattern in patterns:
    			if(fnmatch.fnmatch(dir_contents[i], pattern)):
    				matches.append(dir_contents[i])
    
    return matches


def main():
	'''Collect all the paths to Test files and runs them.'''
	print root_path
	
	# filter for all [Tt]est_ python files
	test_case_paths = find(root_path, ["Test_*.py","test_*.py"],0,1)    
	print test_case_paths
	nose.run(test_case_paths)
	

if __name__ == "__main__":
    main()