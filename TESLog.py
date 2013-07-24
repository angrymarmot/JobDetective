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
        print "Master Path: ", self.masterPath
        print "Agent Path: ", self.agentPath
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
            print "Warning!  No client logs found.  Only master logs will be captured."
            return (self.masterLogs,)
        return (self.masterLogs, self.clientLogs)  # Not sure this is necessary as we can just query the self-values

    def getJobEvents(self, jobID):
        """
        Searches through self.files to extract each event for the specified jobID.
        """
        self.jobID = jobID
        self.parsedLine = []
        self.jobIDMatch = re.compile('JobRun:\s{1}' + self.jobID + '\s{1}')
        self.jobIDMatchClient = re.compile('\s{1}' + self.jobID + '\s{1}')
        #re.split('(^[0-1][0-9]/[1-3][0-9]\s{1})([0-2][0-9]:[0-5][0-9]:[0-5][0-9]).+(\(mem=\d+/\d+\))')
        self.parsedFilename = self.masterPath+ "\\" + self.jobID + "-parsed.txt"  # Will need to control how this is implemented later
        with open(self.parsedFilename, 'w') as self.parsedFile:
            for self.l in self.masterLogs:
                with open(self.masterPath + "\\" + self.l) as self.fp:
                    for self.line in self.fp:
                        self.parsedLine = re.split('(^[0-1][0-9]/[1-3][0-9]\s{1})([0-2][0-9]:[0-5][0-9]:[0-5][0-9]).+(\(mem=\d+/\d+\))', self.line)
                        if len(self.parsedLine) >= 4:  # Disregard any header information
                            if self.jobIDMatch.search(self.parsedLine[4]):
                                self.parsedFile.write(self.parsedLine[1] + self.parsedLine[2] + self.parsedLine[4])
            for self.c in self.clientLogs:
                with open(self.agentPath + "\\" + self.c) as self.fpc:
                    for self.linec in self.fpc:
                        self.parsedLineC = re.split('^_(?P<year>\d{4})(?P<monthday>\d{4})(?P<time>\s\d{2}:\d{2}:\d{2})(?P<sysdata> <.+>)(?P<entry> .+)', self.linec)
                        if self.jobIDMatchClient.search(self.parsedLineC[3]):
                            print self.parsedLineC # Not working



mLog = r'C:\Pythontesting\master'
aLog = r'C:\Pythontesting'
l = TESLog('Local', '5.3.1', mLog, aLog)
result = l.getLogs('20130723', '20130724')
print l.agentPath
print l.masterPath
print l.version
l.getJobEvents('53108359')
#print result

