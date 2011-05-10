import backend
import git
import os
import time

class Git(backend.Backend):
    def __init__(self):
        backend.Backend.__init__(self)
        self.m_path = None
        self.m_repo = None
        
    def setRepo(self, path):
        assert os.path.isdir(path) == True
        self.m_path = path
        self.m_repo = git.Repo(self.m_path)
        
    def initRepo(self, path, url):
        assert os.path.isdir(path) == True
        self.m_path = path
        self.m_repo = git.Repo.init(self.m_path)
                
    def pushChanges(self,changeDict):
        index = self.m_repo.index
        addList = []
        removeList = []
        
        for path, change in changeDict.iteritems():
            if change == 'M':
                addList.append(path)
            elif change == 'A':
                addList.append(path)
            elif change == 'D':
                removeList.append(path)
        
        if len(addList) != 0:
            index.add(addList)
        if len(removeList) != 0:
            index.remove(removeList)
            
        commitMessage = time.asctime(time.localtime())
        latest_commit = index.commit(commitMessage)
        
        origin = self.m_repo.remotes.origin
        origin.push()
        
    def pullChanges(self):
        origin = m_repo.remotes.origin
        origin.push()
        
    def checkout(self,path,url):
        assert os.path.isdir(path) == True
        self.m_path = path
        self.m_repo.clone_from(url,self.m_path)
        