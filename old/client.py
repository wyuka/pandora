import monitor
import proxy
#import backends.backend
from backends import gitBackend

class Client():
    def __init__(self):
        self.m_repo = gitBackend.Git()
        self.m_repo.setRepo('/home/tirtha/pandora/pandoratest')
        self.m_monitor = monitor.Monitor(self)
        self.m_monitor.addWatchLocation('/home/tirtha/pandora/pandoratest')
        self.m_monitor.startMonitoring()
                
    def pushChanges(self, changeQueue):
        print changeQueue.dictionary()
        self.m_repo.pushChanges(changeQueue.dictionary())
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
