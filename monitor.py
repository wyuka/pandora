import pyinotify
import re
import os

class EventHandler(pyinotify.ProcessEvent):
    def __init__(self):
        pyinotify.ProcessEvent.__init__(self)
        self.m_filter = Filter()
        self.m_filter.addToBanList("^\..*$")
        self.m_filter.addToBanList("^.*~$")
        
    def process_IN_CREATE(self, event):
        if self.m_filter.check(event.pathname) == True:
            self.created(event.pathname)
    
    def process_IN_DELETE(self, event):
        if self.m_filter.check(event.pathname) == True:
            self.deleted(event.pathname)
    
    def process_IN_MODIFY(self, event):
        if self.m_filter.check(event.pathname) == True:
            self.modified(event.pathname)
    
    def process_IN_MOVED_TO(self, event):
        if self.m_filter.check(event.pathname) == True:
            self.movedTo(event.pathname)
    
    def process_IN_MOVED_FROM(self, event):
        if self.m_filter.check(event.pathname) == True:
            self.movedFrom(event.pathname)
            
    def created(self, path):
        print "created {0}".format(path)
        
    def deleted(self, path):
        print "deleted {0}".format(path)
        
    def modified(self, path):
        print "modified {0}".format(path)
        
    def movedTo(self, path):
        print "moved in to {0}".format(path)
        
    def movedFrom(self, path):
        print "moved out from {0}".format(path)

class Filter():
    def __init__(self):
        """
        constructor for Filter.
        """
        self.m_banList = []
        self.m_regex = ""
        
    def addToBanList(self, regex):
        self.m_banList.append(regex)
        
        if self.m_banList == []:
            self.m_regex = ""
        else:
            self.m_regex = "({0})".format(self.m_banList[0])
            for i in self.m_banList[1:]:
                self.m_regex += "|({0})".format(i)
        
    def check(self,path):
        filename = os.path.basename(path)
        if re.match(self.m_regex, filename) == None:
            return True
        else:
            return False

class Monitor():
    def __init__(self):
        self.m_watchManager = pyinotify.WatchManager()  # Watch Manager
        self.m_mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE | pyinotify.IN_MODIFY | pyinotify.IN_MOVED_TO | pyinotify.IN_MOVED_FROM # watched events
        self.m_handler = EventHandler()
        
        self.m_notifier = pyinotify.ThreadedNotifier(self.m_watchManager, self.m_handler)
        self.m_wdDict = None
     
    def startMonitoring(self):
        self.m_notifier.start()
    
    def stopMonitoring(self):
        self.m_notifier.stop()
    
    def addWatchLocation(self, path, recursive = False):
        self.m_wdDict = self.m_watchManager.add_watch(path, self.m_mask, rec = recursive)
    
    def removeWatchLocation(self, path, recursive = False):
        if self.m_wdDict != None and self.m_wdDict[path] != 0:
            self.m_watchManager.rm_watch(self.wdDict[path],rec=recursive)
            
def ChangeQueue():
    def __init__(self):
        self.m_list = []
        
    def add(self, path, event)

m = Monitor()
m.addWatchLocation('/home/tirtha')
m.startMonitoring()

