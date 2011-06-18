"""These are the tests for the mediawindows subpackage.

They test the production of graphical windows and so on. Some user interaction
may be required.

"""
# It may be worth looking into an automated GUI testing tool
# (like java.awt.Robot, but for CPython)

# These tests are often written in the style of vanilla unittest, because the
# style with nose used elsewhere in the test suite requires more typing.

import unittest
import subprocess
import sys
import socket

import media
import picture
import mediawindows as mw

from ampy import ampy as amp

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
            mw.callRemote,
            mw.amp.StopInspect,
            inspector_id=self.inspector_id)
    
    def test_updateRaises(self):
        """Test that closing a closed window raises an exception"""
        self.assertRaises(
            mw.exceptions.WindowDoesNotExistError,
            mw.callRemote,
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
    
    def test_isClosed(self):
        """
        The window should start off closed.
        """
        self.assertTrue(self.picture.is_closed())
    
    def test_shownIsNotClosed(self):
        """
        The window should be registered as open after you show it.
        """
        self.picture.show()
        self.assertFalse(self.picture.is_closed())
    
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

class AsymmetricalPictureTestCase(unittest.TestCase):
    """Sometimes, silly bugs happen.
    
    Uses a picture of size (2, 1)"""
    def setUp(self):
        self.picture = picture.Picture(2, 1)
    
    def tearDown(self):
        self.picture.close()
    
    def testShow(self):
        self.picture.show()
    
    def testUpdate(self):
        self.picture.show()
        self.picture.update()

class OtherAsymmetricalPictureTestCase(AsymmetricalPictureTestCase):
    """Uses picture of size (1, 2)"""
    def setUp(self):
        self.picture = picture.Picture(1, 2)
    

class LargePictureTestCase(unittest.TestCase):
    def setUp(self):
        self.picture = picture.Picture(1000, 1000)
    
    def tearDown(self):
        self.picture.close()
    
    def test_pictureIsTooLarge(self):
        """If this fails, none of the other tests in this suite make sense.
        
        The picture's PIL tostring should have a length not representable
        in two bytes, making it imcompatible with amp as a single value.
        """
        self.assertTrue(len(self.picture.image.tostring()) > 0xFFFF)
    
    def test_showLargePicture(self):
        """
        AMP only permits up to 64 kilobyte values. Pictures can be larger than
        that. To compensate, we use the BigString recipe from the amp wiki.
        This test ensures that it's being used correctly.
        """
        self.picture.show()

class OutdatedInspectorHandleTestCase(unittest.TestCase):
    """
    Sometimes an inspector can be updated by someone else. e.g. the user
    can close the window, despite .close() never being called.
    These tests simulate that, and check that the right things happen.
    
    We should never rely on a local understanding of what the current state
    is.
    """
    def setUp(self):
        self.picture = picture.Picture(1, 1)
        self.picture.show()
        outdated_inspector_id = self.picture.inspector_id
        self.picture.close()
        self.picture.inspector_id = outdated_inspector_id # oh no!
        
    def test_isOpen(self):
        self.assertTrue(self.picture.is_closed())
    
    def test_update(self):
        self.picture.update() # should reopen
        self.assertFalse(self.picture.is_closed())
        self.picture.close()
    
    def test_update(self):
        self.picture.show() # should open new window
        self.assertFalse(self.picture.is_closed())
        self.picture.close()

class MultipleAmpClientsTestCase(unittest.TestCase):
    """
    Because servers aren't safe for multiple clients (they might block at the
    whim of the client, etc.), they shouldn't accept multiple clients. This
    test case tests that.
    """
    def setUp(self):
        self.proxy = amp.Proxy('127.0.0.1', mw.amp.PORT, socketTimeout=None)
    
    def test_cantConnect(self):
        self.assertRaises(socket.error, self.proxy.connect)

class MultipleAmpServersTestCase(unittest.TestCase):
    """
    Because Windows doesn't have sensible support for anonymous pipes,
    a socket is used for communicating between processes. Sockets use ports
    from a global namespace, there can only be up to 65535 (0xffff) ports
    in use at any time, and the same port can't be used by independent
    processes.
    
    What this means is that if two processes import media, they need to both
    start a mediawindows process each, but they can't use the same process*.
    These tests confirm that they each create different processes and
    (presumably) work.
    
    [*] Note: it was mentioned that they can't use the same process. That isn't
    obvious, however. Perhaps they could cooperate and use the same process?
    Here are the reasons why that would be a bad idea:
    
    - **The processes are created as *sub*processes.** Unfortunately, due to
      the Windows OS lacking a daemonization mechanism (double-fork), the
      lifetime of a subprocess is inextricably linked to the lifetime of a
      process. So if they share a server, if the host dies, the other process
      loses all its open windows and has to start a new server.
    - **Some calls on the server might block.** In particular, the ask* dialogs
      are most likely blocking calls that will lock up the server entirely.
      It just can't be used by multiple clients.
    
    """
    
    def setUp(self):
        self.proc = subprocess.Popen([sys.executable, "-c",
            """if 1:
            import media, picture
            x = picture.Picture(1, 1)
            x.show()
            print x.inspector_id
            # need to make sure we ended up using the subprocess
            # (otherwise we might exit before showing its spectacular failure!)
            media.mw.client._CONNECTION_SINGLETON.proc.wait()
            """],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        
        self.stdout, self.stderr = self.proc.communicate()
    
    def test_canShowPictureWithoutCrashing(self):
        try:
            int(self.stdout) # succeeds past the print, no extra data
        except ValueError:
            self.fail("stdout had non-int: %r" % (self.stdout,)) 
        self.assertEqual(self.stderr, '') # no error messages
        self.assertEqual(self.proc.returncode, 0) # exited with status 0
    
    def test_doesntUseOurServer(self):
        """
        It's possible that the subprocess's server crashes because the port is
        taken, but the client succeeds in connecting to our server in the
        current process. Let's check that this isn't true.
        """
        x = picture.Picture(1, 1)
        x.inspector_id = int(self.stdout) # ewww !
        self.assertTrue(x.is_closed())

if __name__ == '__main__':
    unittest.main()
