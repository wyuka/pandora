#from PyQt4.QtGui import *
#from PyQt4.QtCore import *

class proxyable:
    
    def __init__(self):
        """
        handles the constructor
        """
        self.m_proxyEnabled = bool()
        self.m_host = str()
        self.m_port = int()
        self.m_userName = str()
        self.m_password = str()
        self.m_proto = str()
    
    def proxyEnabled(self):
        """
        returns if proxy is enabled
        """
        return self.m_proxyEnabled
    
    def setProxyEnabled(self, enable=True):
        """
        sets if proxy is enabled.
        """
        self.m_proxyEnabled = enable
        
    def host(self):
        """
        returns proxy host address
        """
        return self.m_address
    
    def setHost(self, host):
        """
        sets proxy host address
        """
        self.m_host = host
    
    def port(self):
        """
        returns proxy port
        """
        return self.m_port
        
    def setPort(self, port):
        """
        sets proxy port
        """
        self.m_port = port
        
    def userName(self):
        """
        returns proxy username
        """
        return self.m_userName
    
    def setUserName(self, userName):
        """
        sets proxy port
        """
        self.m_userName = userName
        
    def password(self):
        """
        returns proxy password
        """
        return self.m_password
        
    def setPassword(self, password):
        """
        sets proxy password
        """
        self.m_password = password
    
    def proto(self):
        """
        returns proxy protocol
        """
        return self.m_proto
        
    def setProto(self, proto):
        """
        sets proxy protocol
        """
        self.m_proto = proto
        
    def address(self):
        """
        returns proxy address, if proxy is enabled
        """
        if self.m_proxyEnabled == False:
            return None
        
        auth = ""
        
        if self.m_userName != None and self.m_userName != "":
            auth = "{0}@".format(self.m_userName)
            if self.m_password != None and self.m_password != "":
                auth = "{0}:{1}@".format(self.m_userName, self.m_password)
        
        port = ""
        
        if self.m_port != None and self.m_port > 0:
            port = ":{0}".format(self.m_port)
        
        addr = "{0}://{1}{2}{3}/".format(self.m_proto,auth,self.m_host,port)
        
        return addr
