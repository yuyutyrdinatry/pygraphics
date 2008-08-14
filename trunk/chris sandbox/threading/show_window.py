import threading
import wx

class show_window(threading.Thread):
    """Run the MainLoop as a thread. Access the frame with self.frame."""
    def __init__(self, autoStart=True):
        threading.Thread.__init__(self)
        self.setDaemon(1)
        self.start_orig = self.start
        self.start = self.start_local
        self.frame = None #to be defined in self.run
        self.lock = threading.Lock()
        self.lock.acquire() #lock until variables are set
        if autoStart:
            self.start() #automatically start thread on init
            
    def run(self):
        app = wx.PySimpleApp()
        frame = ImageFrame(None)
        frame.SetSize((800, 600))
        frame.Show(True)

        #define frame and release lock
        #The lock is used to make sure that SetData is defined.
        self.frame = frame
        self.lock.release()

        app.MainLoop()

    def start_local(self):
        self.start_orig()
        #After thread has started, wait until the lock is released
        #before returning so that functions get defined.
        self.lock.acquire()

if __name__ == '__main__':
    import picture
    import media
    pass