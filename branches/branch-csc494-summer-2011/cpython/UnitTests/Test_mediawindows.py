"""These are the tests for the mediawindows subpackage.

They test the production of graphical windows and so on. Some user interaction
may be required.

"""
# It may be worth looking into an automated GUI testing tool
# (like java.awt.Robot, but for CPython)

# These tests are written in the style of vanilla unittest, because the style
# with nose used elsewhere in the test suite requires more typing.

import unittest

import media
import picture

class InspectorTestCase(unittest.TestCase):
    def setUp(self):
        self.picture = picture.Picture(1, 1)
    
    def tearDown(self):
        self.picture.close()
    
    def test_openTwice(self):
        """
        Showing a picture twice should result in the window being closed and
        then reopened.
        """
        self.picture.show()
        self.picture.show() # any exception? no? good.
    
    def test_closeUnopened(self):
        """
        Nothing should happen at all, here.
        """
        self.picture.close()
    
    def test_closeTwice(self):
        """
        Nothing should happen here either.
        """
        self.picture.show()
        self.picture.close()
        self.picture.close()
    
    def test_update(self):
        """
        Should be able to update a picture (not testing whether it works, that's
        really hard).
        """
        self.picture.show()
        self.picture.update()
    
    def test_updateUnopened(self):
        """
        Updating an unopened/closed picture should show the inspector instead
        of updating a nonexistent one.
        """
        self.picture.update()

if __name__ == '__main__':
    unittest.main()
