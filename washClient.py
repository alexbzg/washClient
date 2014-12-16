#!/usr/bin/python
#coding=utf-8

from twisted.internet import gtk2reactor
gtk2reactor.install()

import gtk 
import webkit

from twisted.internet import reactor, defer
from twisted.spread import pb
from twisted.internet.protocol import Protocol, ReconnectingClientFactory

import os
import sys 

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)



#def load_finished(webview, frame):
#    print 'load finished'
#    connectServer()

def on_destroy(widget):
    gtk.main_quit()



window = gtk.Window()
window.connect("destroy", on_destroy)
window.maximize()
window.set_title('Мойка')

browser = webkit.WebView()
browser.props.settings.props.enable_default_context_menu = False

connected = False

def openStub():
    global connected
    connected = False
    browser.open( 'file:///' + application_path + '/stub.html' )



scroller = gtk.ScrolledWindow()
scroller.add(browser)

vbox = gtk.VBox()
vbox.pack_start(scroller, True, True, 0)

window.add(vbox)
window.show_all()

openStub()

class ClientSide( pb.Referenceable ):
    def remote_update( self, arg ):
        browser.execute_script( 'updater( ' + arg + ');' )

class RecPBClientFactory(pb.PBClientFactory, ReconnectingClientFactory):
    maxDelay = 15

    def __init__(self):
        pb.PBClientFactory.__init__(self)
        self.ipaddress = None

    def clientConnectionMade(self, broker):
        global connected
        print 'Started to connect.'
        connected = True
        pb.PBClientFactory.clientConnectionMade(self, broker)
        browser.open('http://192.168.0.1:8788')

    def connectServerSide( self, webview, frame ):
        if connected:
            d = self.getRootObject()
            d.addCallback( lambda object: object.callRemote( "connect", 
                    ClientSide(), 2 ) )
            d.addCallback( self.saveServerSide )

    def buildProtocol(self, addr):
        print 'Connected to %s' % addr
        return pb.PBClientFactory.buildProtocol(self, addr)

    def clientConnectionLost(self, connector, reason):
        print 'Lost connection.  Reason: ' + str( reason )
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)
        browser.disconnect( self.serverSignalHandlerId )
        openStub()

    def clientConnectionFailed(self, connector, reason):
        print 'Connection failed. Reason: ' + str( reason )
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)
        

    def saveServerSide( self, serverSide ):

        def title_changed(webview, frame, title):
            if title != 'null':
                if serverSide:
                    serverSide.callRemote( "data", title )
                else:
                    print "no server side"

        self.serverSignalHandlerId = \
            browser.connect('title-changed', title_changed)

factory = RecPBClientFactory()
browser.connect('load-finished', factory.connectServerSide )

def connectServer():

    try:
        reactor.connectTCP( '192.168.0.1', 8789, factory )
    except Exception:
        print 'connection failed'
        connectServer()

connectServer()
reactor.run()
