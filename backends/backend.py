import proxy

class Repo(proxy.proxyable):
    
    def __init__(self):
        proxy.proxyable.__init__(self)
        
    def initRepo(self, path):
        pass
    
    def setRepo(self,path):
        pass
        
    def pullChanges(self):
        pass
    
    def pushChanges(self,changeDict):
        pass
    
