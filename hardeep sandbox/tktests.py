from Tkinter import *
import threading

class TK_Thread(threading.Thread):
    '''Tkinter Mainloop Thread.'''
    
    root = 'def'
        
    def run(self):
        print 'a'
        self.root = Tk()
        print 'b'
        self.root.mainloop()
        print 'c'
        
print '1'
thread = TK_Thread()
print '2'
thread.start()
print '3'