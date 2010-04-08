import Tkinter as tk
from media import *
import cProfile

def testTest():
    i = 1
    while i < 1000:
        i += 5
    print i

def testCreate():
    i = 0    
    while i < 2000:
        pic = create_picture(500, 500)
        i = i + 1
    
cProfile.run("testTest()", sort=1)