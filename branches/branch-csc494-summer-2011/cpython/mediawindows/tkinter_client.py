import Tkinter as tk

from twisted.internet import tksupport, reactor
from twisted.internet.protocol import ClientCreator

from pygraphics.mediawindows import amp

def main():
    root = tk.Tk()
    root.withdraw()
    tksupport.install(root) # this handles the mainloop in Twisted
    
    # now we connect to the server
    client = ClientCreator(reactor, amp.GooeyClient).connectTCP(
        '127.0.0.1', amp.PORT)
    
    reactor.run()

if __name__ == '__main__':
    main()
