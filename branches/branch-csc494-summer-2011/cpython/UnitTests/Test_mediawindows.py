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
import mediawindows as mw

class RawClosedInspectorTestCase(unittest.TestCase):
    """
    Test the how the amp interface deals with closed windows behind the scenes
    """
    def setUp(self):
        # too lazy to do the setup code myself
        pict = picture.Picture(1, 1)
        pict.show()
        self.image = pict.image
        self.inspector_id = pict.inspector_id
        pict.close()
    
    def test_closeRaises(self):
        """Test that closing a closed window raises an exception"""
        self.assertRaises(
            mw.exceptions.WindowDoesNotExistError,
            mw.threaded_callRemote,
            mw.amp.StopInspect,
            inspector_id=self.inspector_id)
    
    def test_updateRaises(self):
        """Test that closing a closed window raises an exception"""
        self.assertRaises(
            mw.exceptions.WindowDoesNotExistError,
            mw.threaded_callRemote,
            mw.amp.UpdateInspect,
            inspector_id=self.inspector_id,
            img=self.image)

class InspectorTestCase(unittest.TestCase):
    """
    Test the high level user of the proxied inspector through the Picture class
    """
    # TODO: use a mocked API for this!
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

class OutdatedInspectorHandleTestCase(unittest.TestCase):
    """
    Sometimes an inspector can be updated by someone else. e.g. the user
    can close the window, despite .close() never being called.
    These tests simulate that, and check that the right things happen.
    
    we should never rely on a local understanding of what the current state
    is.
    """
    def setUp(self):
        self.picture = picture.Picture(1, 1)
        self.picture.show()
        outdated_inspector_id = self.picture.inspector_id
        self.picture.close()
        self.picture.inspector_id = outdated_inspector_id # oh no!
    
    def test_update(self):
        self.picture.update() # should reopen
        self.assertFalse(self.picture.is_closed())
        self.picture.close()
    
    def test_update(self):
        self.picture.show() # should open new window
        self.assertFalse(self.picture.is_closed())
        self.picture.close()

if __name__ == '__main__':
    unittest.main()
