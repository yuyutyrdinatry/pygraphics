import unittest
from TestExecute import *
from media import *

# we MUST set the debug level to 1 to force errors to return
debugLevel = 1

class Test_Temp(unittest.TestCase):
    
    def setUp(self):
        setup = None;
        # No code needed here
        # Would run at the start of every individual test
        
    def tearDown(self):
        tearDown = None

    def testTemp(self):
        test = None;
        #uri = resi("white.bmp")
        #print resourcesPrefix
        #self.pict = Picture()
        # self.failUnless(self.pict.dispImage == None, 'New Picture contains display image')
        # self.failUnless(self.pict.winActive == 0, 'New Picture is active')
        #self.failUnless(self.pict.loadImage(uri), 1, 'white.bmp could not be loaded')
        #self.assertEqual(self.pict.load(tres("white.bmp")), 1, 'white.bmp could not be loaded')