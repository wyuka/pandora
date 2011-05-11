import abstractVCS
from PyQt4.QtCore import *
import os

class Git(abstractVCS.AbstractVCS):
    def currentHash(self):
        return self._currentHash
        
    def isSyncing(self):
        return self._isSyncing
        
    def isBuffering(self):
        return self._isBuffering
        
    def isPolling(self):
        return self._isPolling
        
    def isFetching(self):
        return self._isFetching
        
    def isPushing(self):
        return self._isPushing
        
    def hasUnsyncedChanges(self):
        return self._hasUnsyncedChanges
        
    def serverOnline(self):
        return self._serverOnline
        
    def runGit(self,args):
        for gitpath in self.paths:
            if os.path.exists(gitpath):
                break
        
        if os.path.exists(gitpath) == False:
            return
        
        arglist = [gitpath]
        arglist.extend(args.split(),cwd=self.localPath)
        
        try:
            toReturn = subprocess.check_output(arglist)
            if toReturn == None:
                return ""
            else:
                return toReturn
        except subprcoess.CalledProcessError:
            return None
        
    def __init__(self,path):
        abstractVCS.AbstractVCS.__init__(self)
        self.paths = ['/usr/bin/git','/usr/local/bin/git']
        self.name = "Git"
        
        self._currentHash = str()
        self._isSyncing = False
        self._isBuffering = False
        self._isPolling = True
        self._isFetching = False
        self._isPushing = False
        self._hasUnsyncedChanges = False
        self._serverOnline = True
        self.fetchQueue = 0
        self.announceQueue = 0
        
        self.repoName = os.path.basename(path)
        self.remoteOriginUrl = self.getRemoteOriginUrl()
        self.remoteRepoName = os.path.basename(self.remoteOriginUrl)
        self.domain = self.getDomain(self.remoteOriginUrl)
        self.description = self.getDescription()
        self.localPath = path
        self.userName = self.getUserName()
        self.userEmail = self.getUserEmail()
        
        if self.isEmpty():
            self._currentHash = None
        else:
            self._currentHash = self.getCurrentHash()
            
        if os.path.exists(os.join(self.localPath,".git","has_unsynced_changes")):
            self._hasUnsyncedChanges = True
        else:
            self._hasUnsyncedChanges = True
            
        if self._currentHash == None:
            self.createInitialCommit()
            
        self.watcher = QFileSystemWatcher(self)
        self.watcher.addPath(self.localPath)
        self.connect(self.watcher,SIGNAL("directoryChanged(const QString&)"),self.onFileActivity)
        
        #if self.usesNotificationCentre():
        #    self.listener = listener.Listener(self.domain, self.RemoteName, self.userEmail, centralServer = True)
        #else:
        #    self.listener = listener.Listener(self.domain, self.RemoteName, self.userEmail, centralServer = False)
            
        self.remote_timer = QTimer(self)
        self.remote_timer.setInterval(60000)
        self.connect(self.remote_timer, SIGNAL("timeout()"), self.onRemoteTimerElapsed)
        
        #self.connect(self.listener.Listener.Client,SIGNAL(),
        self.sizeBuffer = []
        
        self.local_timer = QTimer(self)
        self.local_timer.setInterval(1000)
        self.connect(self.local_timer, SIGNAL("timeout()"), self.handleLocalChanges)
        
        self.remote_timer.start()
                
        self.addCommitAndPush()
        
        if self._currentHash == None:
            self._currentHash = getCurrentHash()
        
    def checkForRemoteChanges():
        print "Git [{0}] Checking for remote changes ...".format(self.repoName)
        remoteHash = runGit("ls-remote origin master")
        
        if remoteHash == None:
            return
            
        if remoteHash.startswith(self._currentHash) == False:
            print "Git [{0}] Remote changes found. ({1})".format(self.repoName,self.remoteHash)
            self.fetch()
            
            self.disconnect(self.watcher,SIGNAL("directoryChanged(const QString&)"),self.onFileActivity)
            self.rebase()
            self.connect(self.watcher,SIGNAL("directoryChanged(const QString&)"),self.onFileActivity)
            
    #def checkForLocalChanges():
    #    self.local_timer.stop()
    #    self.local_timer.start()
                   
    def handleLocalChanges():
        print "Local [{0}] Changes have settled.".format(self.repoName)
        self.disconnect(self.watcher,SIGNAL("directoryChanged(const QString&)"),self.onFileActivity)
        while AnyDifferences():
            self.addCommitAndPush()
        self.connect(self.watcher,SIGNAL("directoryChanged(const QString&)"),self.onFileActivity)
        
    def onFileActivity():
        self.local_timer.stop()
        if self.AnyDifferences():
            print "Local [{0}] Changes found. Waiting for changes to settle ...".format(self.repoName)
            self.changesDetected()
            self.remote_timer.stop()
            self.local_timer.start()
        
    def addCommitAndPush():
        try:
            self.remote_timer.stop()
            self.local_timer.stop()
        
            if self.AnyDifferences():
                self.add()
                
                message = self.formatCommitMessage()
                self.commit(message)
                
                self.push()
            
            else:
                self.commitEndedUpEmpty()
                
        finally:
            self.remote_timer.start()
            
    def fetchRebaseAndPush():
        self.checkForRemoteChanges()
        self.push()
        
    def AnyDifferences():
        output = runGit("status --porcelain").rstrip()
        lines = output.split('\n')
        for line in lines:
            if len(line)>1 and line[1] != ' ':
                return True
        
        return False
    
    def isEmpty():
        output = runGit("log -1")
        if output == None:
            return True
        else:
            return False
            
    def getCurrentHash():
        # Remove stale rebase-apply files because it
        # makes the method return the wrong hashes.
        
        if os.path.exists(os.path.join(self.localPath,'.git','rebase-apply')):
            os.remove(os.path.join(self.localPath,'.git','rebase-apply'))
            
        output = runGit('log -1 --format=%H').strip()
        return output
        
    def add():
        print "Git [{0}] Staging changes ...".format(self.repoName)
        runGit("add --all")
        print "Git [{0}] Changes staged ...".format(self.repoName)

        self.added()

    def collectGarbage():
        print "Git [{0}] Collecting garbage ...".format(self.repoName)
        runGit("gc")
        print "Git [{0}] Garbage collected.".format(self.repoName)
        
    def commit():
        if self.AnyDifferences() == False:
            return
        
        runGit("commit -m \'{0}\'")
         
        if random.Random().randint(0,10) == 0:
            print collectGarbage()
             
    def fetch():
        self._isFetching = True
        self._isSyncing = True
        
        self.remote_timer.stop()
        
        print "Git [{0}] Fetching changes.".format(self.repoName)
        output = runGit('fetch -v origin master')
        print "Git [{0}] Changes fetched.".format(self.repoName)
        
        if output == None:
            self._serverOnline = False
            self.fetchingFailed()
            
        else:
            self._serverOnline = True
            self.fetchingFinished()
        
        self.remote_timer.start()
    
    def rebase():
        if self.AnyDifferences():
            self.add()
            
            commitMessage = formatCommitMessage()
            self.commit(commitMessage)
         
        print "Git [{0}] Rebasing changes ...".format(self.repoName)
        output = runGit("rebase -v FETCH_HEAD")
                  
        if output == None:
            print "Git [{0}] Conflicts detected. Trying to get out ...".format(self.repoName)
            self.disconnect(self.watcher,SIGNAL("directoryChanged(const QString&)"),self.onFileActivity)
             
            while self.AnyDifferences():
                resolveConflicts()
                 
            print "Git [{0}] Conflicts resolved.".format(self.repoName)
            self.connect(self.watcher,SIGNAL("directoryChanged(const QString&)"),self.onFileActivity)
             
            conflictDetected()
         
        self._currentHash = self.getCurentHash()
        
    def getDomain(self,url):
        if url == "" or url == None:
            return None
        
        domain = url.split('@')[1]
        
        if len(domain.split(':')) > 1:
            return domain.split(':')[0]
        else:
            return domain.split('/')[0]
    
    def getDescription(self):
        f = open(os.path.join(self.localPath,'.git','description')
        
        

g = Git('/home/tirtha/pandora-python')