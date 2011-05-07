import monitor

class Client:
    def __init__(self):
        self.m_monitor = monitor.Monitor(self)
        self.m_monitor.addWatchLocation('/home/tirtha',False)
        self.m_monitor.addWatchLocation('/home/tirtha/pandora',False)
        self.m_monitor.startMonitoring()
        
    def pushChanges(self, changeQueue):
        print changeQueue.dictionary()
        changeQueue.clear()
        
c = Client()