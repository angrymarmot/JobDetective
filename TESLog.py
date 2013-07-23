__author__ = 'bencha'
import os

class TESLog(object):
    def __init__(self, agentType, version):
        self.agentType = agentType
        self.version = version

    def getLogs(self, agentPath, startDate, endDate):
        """
        Gets a collection of logs based on start and end dates for local processing
        """
        if self.agentType == 'Retail':
            self.agentPath = r'\\' + agentPath + r'srv02.thecreek.com\c$\Program Files\TIDAL\Agent\TIDAL_AGENT_1\logs\''
        else:
            self.agentPath = agentPath
        self.startDate = startDate
        self.endDate = endDate
        if not os.path.exists(agentPath):
            print "Path", self.agentPath, "does not exist or cannot be accessed presently."
            exit(1)
l = TESLog('Retail', '5.3.1')
l.getLogs('80312', 2013723, 2013723)
print l.agentPath
print l.splitPath

