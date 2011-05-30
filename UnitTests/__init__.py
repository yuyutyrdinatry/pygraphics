import os

# IGNORE_FILES is a list of strings, which describe the file names to be 
# ignored.
#    i.e. file.name
IGNORE_FILES = ['__init__.py', 'Test_Temp.py']

__all__ = []
for root, dirs, files in os.walk(os.getcwd()):
    for file in IGNORE_FILES:
        if ( file in files ):
            files.remove(file)
            
    for file in files:
        if ( file[-2:] == 'py' and root == os.getcwd()):
            __all__.append(file)
            
if __name__ == '__main__':
    print __all__