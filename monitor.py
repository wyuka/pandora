import pyinotify
import re
import os
import time
import threading

WAIT_SINCE_LAST_UPDATE = 10.0

class EventHandler(pyinotify.ProcessEvent):
    def __init__(self,monitor):
        pyinotify.ProcessEvent.__init__(self)
        self.m_monitor = monitor
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
        self.m_monitor.enqueue(path,'A')
        
    def deleted(self, path):
        print "deleted {0}".format(path)
        self.m_monitor.enqueue(path,'D')
        
    def modified(self, path):
        print "modified {0}".format(path)
        self.m_monitor.enqueue(path,'M')
        
    def movedTo(self, path):
        print "moved in to {0}".format(path)
        self.m_monitor.enqueue(path,'A')
        
    def movedFrom(self, path):
        print "moved out from {0}".format(path)
        self.m_monitor.enqueue(path,'D')

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

class ChangeQueue():
    def __init__(self):
        self.m_dict = {}
        self.m_lastUpdatedTime = time.time()
        
    def add(self, path, event):
        if event == "A":
            if path in self.m_dict:
                ev = self.m_dict[path]
                
                if ev == "D":
                    self.m_dict[path] = "M"
                elif ev == "M":
                    pass
                elif ev == "A":
                    pass
                
            else:
                self.m_dict[path] = "A"
                
        elif event == "M":
            if path in self.m_dict:
                ev = self.m_dict[path]
                
                if ev == "D":
                    self.m_dict[path] = "M"
                elif ev == "M":
                    pass
                elif ev == "A":
                    pass
                    
            else:
                self.m_dict[path] = "M"
        
        elif event == "D":
            if path in self.m_dict:
                ev = self.m_dict[path]
                
                if ev == "D":
                    pass
                elif ev == "M":
                    self.m_dict[path] = "D"
                elif ev == "A":
                    self.m_dict.pop(path)
            
            else:
                self.m_dict[path] = "D"
        
        self.m_lastUpdatedTime = time.time()
        #print self.m_dict # TODO : to be removed from here
    
    def lastUpdatedTime(self):
        return self.m_lastUpdatedTime
        
    def dictionary(self):
        return self.m_dict
        
    def clear(self):
        self.m_dict.clear()

class Monitor():
    def __init__(self,client):
        self.m_client = client
        self.m_timer = None
        self.m_changeQueue = ChangeQueue()
        self.m_watchManager = pyinotify.WatchManager()  # Watch Manager
        self.m_mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE | pyinotify.IN_MODIFY | pyinotify.IN_MOVED_TO | pyinotify.IN_MOVED_FROM # watched events
        self.m_handler = EventHandler(self)
        
        self.m_notifier = pyinotify.ThreadedNotifier(self.m_watchManager, self.m_handler, timeout=10)
        self.m_wdDict = None
     
    def startMonitoring(self):
        self.m_notifier.start()
    
    def stopMonitoring(self):
        time.sleep(0.5)
        self.m_notifier.stop()
    
    def addWatchLocation(self, path, recursive = False):
        self.m_wdDict = self.m_watchManager.add_watch(path, self.m_mask, rec = recursive)
    
    def removeWatchLocation(self, path, recursive = False):
        if self.m_wdDict != None and self.m_wdDict[path] != 0:
            self.m_watchManager.rm_watch(self.wdDict[path],rec=recursive)
            
    def enqueue(self, path, event):
        #if time.time() - WAIT_SINCE_LAST_UPDATE > self.m_changeQueue.lastUpdatedTime():
        #    self.m_client.pushChanges(self.m_changeQueue)
        if self.m_timer != None:
            self.m_timer.cancel()
        self.m_changeQueue.add(path,event)
        
        self.m_timer = threading.Timer(10.0,self.pushChanges)
        self.m_timer.start()
    
    def pushChanges(self):
        #print "here"
        self.m_client.pushChanges(self.m_changeQueue)
        