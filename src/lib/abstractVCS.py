from PyQt4.QtCore import *

import os

class AbstractVCS(QObject):
    def __init__(self):
        QObject.__init__(self)
        self.paths = []
        self.name = "Abstract"

    #def sendToServer():
    #    pass
    
    #def getFromServer():
    #    pass
    
    def checkForRemoteChanges():
        pass
    
    def checkForLocalChanges():
        pass