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
import os
import socket
import time

import media
import picture
import mediawindows as mw

from ampy import ampy as amp

def graphical_test(testcase):
    if '--all' in sys.argv:
        return testcase

class RawInspectorTestCase(unittest.TestCase):
    """
    Test the how the amp interface deals with closed windows behind the scenes
    """
    def setUp(self):
        # too lazy to do the setup code myself
        pict = picture.Picture(1, 1)
        self.image = pict.image
        self.inspector_id = 0
    
    def tearDown(self):
        try:
            self.stopInspect()
        except mw.exceptions.MediaWindowsError:
            pass

    def startInspect(self):
        res = mw.callRemote(mw.amp.StartInspect, img=self.image)
        self.inspector_id = res['inspector_id']
        return res
    
    def stopInspect(self):
        return mw.callRemote(mw.amp.StopInspect, inspector_id=self.inspector_id)

    def updateInspect(self):
        return mw.callRemote(mw.amp.UpdateInspect, 
            inspector_id=self.inspector_id,
            img=self.image)

    def pollInspect(self):
        return mw.callRemote(mw.amp.PollInspect,
            inspector_id=self.inspector_id)

    def test_closeUnopenedRaises(self):
        """Closing an unopened window raises an exception"""
        self.assertRaises(
            self.stopInspect)

    def test_closeUnopenedRaises(self):
        """Closing a closed window raises an exception"""
        self.startInspect()
        self.stopInspect()
        self.assertRaises(
            self.stopInspect)

    def test_updateUnopenedRaises(self):
        """Updating an unopened window raises an exception"""
        self.assertRaises(
            self.updateInspect)

    def test_updateUnopenedRaises(self):
        """Updating a closed window raises an exception"""
        self.startInspect()
        self.stopInspect()
        self.assertRaises(
            self.updateInspect)

    def test_pollUnopenedIsClosed(self):
        """The window starts off closed."""
        self.assertTrue(self.pollInspect()['is_closed'])

    def test_pollClosedIsClosed(self):
        """The window polls as closed after it's closed."""
        self.startInspect()
        self.stopInspect()
        self.assertTrue(self.pollInspect()['is_closed'])

    def test_shownIsNotClosed(self):
        """The window is open after being shown."""
        self.startInspect()
        self.assertFalse(self.pollInspect()['is_closed'])

    def test_show(self):
        """Showing assigns a nonzero inspector id"""
        self.startInspect()
        self.assertNotEqual(self.inspector_id, 0)

    def test_showTwice(self):
        """The same image can be shown multiple times."""
        self.startInspect()
        id = self.inspector_id
        self.startInspect()
        self.assertNotEqual(self.inspector_id, id)
        self.stopInspect()
        self.inspector_id = id

    def test_update(self):
        """Images can be updated

        This doesn't test whether they actually are, just that nothing breaks
        terribly.

        """
        self.startInspect()
        self.updateInspect()

def raisable(e):
    if isinstance(e, type) and issubclass(e, TypeError):
        return True
    try:
        raise e
    except TypeError:
        return False
    else:
        return True

class InspectorTestCase(unittest.TestCase):
    """
    Test the high level user of the proxied inspector through the Picture class
    """
    # TODO: use a mocked API for this!
    def setUp(self):
        self.picture = picture.Picture(1, 1)
        self.old_callRemote = mw.callRemote
        mw.callRemote = self.mocked_callRemote
        # tuples: (expected_cls, expected_kwargs return/raise value) ...
        self.mock_actions = [] 

    def tearDown(self):
        mw.callRemote = self.old_callRemote
        if self.mock_actions:
            # this will be a test error, we probably don't really care...
            # arguably it should be an error _and_ we should do the check
            # in the test methods, but laziness trumps all
            self.fail("mock actions were not all taken: %s" % self.mock_actions)

    def mocked_callRemote(self, command, **kwargs):
        if not self.mock_actions:
            self.fail("Ran out of mock actions for callRemote(%s, **%s)" % 
                (command, kwargs))

        (expected_Command, expected_kwargs, action) = self.mock_actions.pop(0)
        self.assert_(issubclass(command, expected_Command))
        self.assertEqual(expected_kwargs, kwargs)

        if raisable(action):
            raise action
        else:
            return action

    def test_openCleanly(self):
        """Images assign their inspector_id when they open a new window."""
        self.mock_actions = [
            (mw.amp.StopInspect,
                {"inspector_id": 0},
                {}),
            (mw.amp.StartInspect, 
                {"img": self.picture.image}, 
                {"inspector_id": 1})]
        self.picture.show()
        self.assertEqual(self.picture.inspector_id, 1)

    def test_openDirty(self):
        """
        Images ignore errors when closing a window as part of opening a new
        inspector window.
        """
        self.mock_actions = [
            (mw.amp.StopInspect,
                {"inspector_id": 0},
                mw.exceptions.WindowDoesNotExistError),
            (mw.amp.StartInspect, 
                {"img": self.picture.image}, 
                {"inspector_id": 1})]

        self.picture.show()
        self.assertEqual(self.picture.inspector_id, 1)

    def test_closeCleanly(self):
        """Images forward close requests"""
        self.mock_actions = [
            (mw.amp.StopInspect,
                {"inspector_id": 0},
                {})]

        self.picture.close()

    def test_closeUnopened(self):
        """Images ignore errors when closing a window."""
        self.mock_actions = [
            (mw.amp.StopInspect,
                {"inspector_id": 0},
                mw.exceptions.WindowDoesNotExistError)]

        self.picture.close()

    def test_updateCleanly(self):
        """Images forward update requests"""
        self.mock_actions = [
            (mw.amp.UpdateInspect,
                {"inspector_id": 0, "img": self.picture.image},
                {})]

        self.picture.update()

    def test_updateDirty(self):
        """
        Images turn update requests into show requests if there is no inspector
        window running.
        """
        self.mock_actions = [
            (mw.amp.UpdateInspect,
                {"inspector_id": 0, "img": self.picture.image},
                mw.exceptions.WindowDoesNotExistError),
            (mw.amp.StopInspect,
                {"inspector_id": 0},
                {}),
            (mw.amp.StartInspect, 
                {"img": self.picture.image}, 
                {"inspector_id": 1})]

        self.picture.update()

    def test_isClosedYes(self):
        """is_losed forwards the request"""
        self.mock_actions = [
            (mw.amp.PollInspect,
                {"inspector_id": 0},
                {"is_closed": True})]

        self.assertTrue(self.picture.is_closed())

    def test_isClosedNo(self):
        """is_losed forwards the request"""
        self.mock_actions = [
            (mw.amp.PollInspect,
                {"inspector_id": 0},
                {"is_closed": False})]

        self.assertFalse(self.picture.is_closed())

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
        # oh no!
        self.picture.inspector_id = outdated_inspector_id

    def test_isOpen(self):
        self.assertTrue(self.picture.is_closed())

    def test_update(self):
        # should reopen
        self.picture.update()
        self.assertFalse(self.picture.is_closed())
        self.picture.close()

    def test_update(self):
        # should open new window
        self.picture.show()
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


def _print_loud(msg):
    underscores = "#" * min(len(msg), 80)
    print
    print underscores
    print msg
    print underscores


@graphical_test
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
            """],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

        _print_loud("Please close the window to proceed with the tests.")
        self.stdout, self.stderr = self.proc.communicate()

    def test_canShowPictureWithoutCrashing(self):
        try:
            # succeeds past the print, no extra data
            int(self.stdout)
        except ValueError:
            self.fail("stdout had non-int: %r" % (self.stdout,))

        # no error messages
        self.assertEqual(self.stderr, '')
        # exited with status 0
        self.assertEqual(self.proc.returncode, 0)

    def test_doesntUseOurServer(self):
        """
        It's possible that the subprocess's server crashes because the port is
        taken, but the client succeeds in connecting to our server in the
        current process. Let's check that this isn't true.
        """
        x = picture.Picture(1, 1)
        # ewww !
        x.inspector_id = int(self.stdout)
        self.assertTrue(x.is_closed())

@graphical_test
class AmpAskTestCase(unittest.TestCase):
    """Tests for user interaction with Ask* Commands

    Because of the nature of these tests, they require user input. They are not
    automated, and can only be run directly. Run this test file with "--all"
    to include AmpAskTestCase.

    In the future it may be desirable to automate these tests.

    """
    # because, seriously, if we don't automate them, nobody will eeeeever run
    # them. ~Devin

    def setUp(self):
        self.workdir = os.path.abspath(os.path.dirname(__file__))

    def test_askCancel(self):
        _print_loud("Please press Cancel.")
        self.assertRaises(mw.exceptions.DialogCanceledException,
            mw.callRemote,
            mw.amp.AskDirectory,
            initialdir=self.workdir)

    def test_askInitialDir(self):
        _print_loud("Please press OK")
        self.assertEqual(
            mw.callRemote(mw.amp.AskDirectory, initialdir=self.workdir)['path'],
            self.workdir)

    def test_askInitialDir2(self):
        _print_loud("Please press OK")
        self.assertEqual(
            mw.callRemote(mw.amp.AskDirectory, initialdir='/')['path'],
            '/')

if '--all' in sys.argv:
    sys.argv.remove('--all')
else:
    pass # relevant test cases have already been deleted.

class ProcessClosesCleanlyTestCase(unittest.TestCase):
    """
    While programs like 'import media; media.show(...)' shouldn't close until
    all the windows are closed, programs that don't open windows should close
    right away. This tests that.
    """
    def test_closesAfterOneSecond(self):
        proc = subprocess.Popen([sys.executable, '-c', 'import media'])
        time.sleep(1)
        if proc.poll() is None:
            self.fail("python -c 'import media' did not close in 1 second")

if __name__ == '__main__':
    unittest.main()
