import backend
import git
import os

class Git(backend.Repo):
    def __init__(self):
        backend.Repo.__init__(self)
        self.m_path = None
        self.m_repo = None
        
    def setRepo(self, path):
        assert os.isdir(path) == True
        self.m_repo = git.Repo(path)
        
    def initRepo(self, path):
        assert os.isdir(path) == True
        self.m_repo = git.Repo.init(path)
        
    def pushChanges(self,changeDict)