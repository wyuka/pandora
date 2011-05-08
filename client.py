import monitor
import proxy
import backend

class Client():
    def __init__(self):
        self.m_monitor = monitor.Monitor(self)
        self.m_monitor.addWatchLocation('/home/tirtha')
        self.m_monitor.addWatchLocation('/home/tirtha/pandora')
        self.m_monitor.startMonitoring()
                
    def pushChanges(self, changeQueue):
        print changeQueue.dictionary()
        changeQueue.clear()
        
    def destroy(self):
        self.m_monitor.stopMonitoring()
        
c = Client()
a = 0
while True:
    try:
        a = a + 1
    except KeyboardInterrupt:
        c.destroy()
        break
    except:
        raise
