__author__ = 'bencha'
import os
import re


class TESLog(object):
    def __init__(self, agentType, version, masterPath, agentPath):
        self.agentType = agentType
        self.version = version
        self.masterPath = os.path.normpath(masterPath)
        self.agentPath = os.path.normpath(agentPath)
        if self.agentType == 'Retail':
            self.agentPath = r'\\' + agentPath + r'srv02.thecreek.com\c$\Program Files\TIDAL\Agent\TIDAL_AGENT_1\logs\''
        else:
            self.agentPath = agentPath
        if not os.path.isdir(self.agentPath):
            print "Path", self.agentPath, "does not exist or cannot be accessed presently."
            exit(1)

    def getLogs(self, startDate, endDate):
        """
        Returns a tuple of log files based on start and end dates for local processing
        """
        self.startDate = startDate
        self.endDate = endDate
        self.files = next(os.walk(self.masterPath))[2], next(os.walk(self.agentPath))[2]
        #self.masterMatcher = re.compile('Master-[0-9]{8}')
        self.clientMatcher = re.compile('.+CDASRVTDLAPP01.+')
        self.masterMatcherStart = re.compile('Master-' + self.startDate + '.+\.log')
        self.masterMatcherEnd = re.compile('Master-' + self.endDate + '.+\.log')
        self.masterLogs = []
        self.clientLogs = []
        for m in self.files[0]:
            self.checkStart = self.masterMatcherStart.match(m)
            self.checkEnd = self.masterMatcherEnd.match(m)
            if self.checkStart:
                self.masterLogs.append(m)
            if self.checkEnd:
                self.masterLogs.append(m)
        for c in self.files[1]:
            self.checkClientLog = self.clientMatcher.match(c)
            if self.checkClientLog:
                self.clientLogs.append(c)
        if not self.masterLogs:
            print "No Master Logs found between", self.startDate, "and", self.endDate
            print "Aborting with exit code 1..."
            exit(1)
        if not self.clientLogs:
            print "Warning!  No client logs found."
            return (self.masterLogs,)
        return (self.masterLogs, self.clientLogs)

    def getJobEvents(self, jobID):
        """
        Searches through self.files to extract each event for the specified jobID.
        """
        pass



mLog = r'X:\Dropbox\Development\JobDetective\Logs\master'
aLog = r'X:\Dropbox\Development\JobDetective\Logs'
l = TESLog('Local', '5.3.1', mLog, aLog)
result = l.getLogs('20130723', '20130724')
print l.agentPath
print l.masterPath
print l.version
print result

