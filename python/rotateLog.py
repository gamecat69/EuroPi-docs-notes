import os
try:
    import machine
except:
    pass

class Test():

    def __init__(self):
        self.logFilePrefix = 'cvecorder_debug'
        self.maxLogFiles = 5
        self.logFileList = []
        self.currentLogFile = ''
        self.maxLogFileName = self.logFilePrefix + str(self.maxLogFiles) + '.log'

        self.rotateLog()


    def writeToDebugLog(self, msg):

        try:
            rtc=machine.RTC()
            timestamp=rtc.datetime()
            timestring="%04d-%02d-%02d %02d:%02d:%02d"%(timestamp[0:3] + timestamp[4:7])
        except:
            timestring='0000-00-00 00:00:00'

        maxRetries = 6
        attempts = 0
        while attempts < maxRetries:
            try:
                attempts += 1
                with open(self.currentLogFile, 'a') as file:
                    # Attempt write data to state on disk, then break from while loop if the return (num bytes written) > 0
                    if file.write(timestring + ' ' + msg + '\n') > 0:
                        self.writeError = False
                        break
            except MemoryError as e:
                print(f'[{attempts}] Error: Memory allocation failed, retrying: {e}')
            except Exception as e:
                print(f'[{attempts}] Error writing to debug log. {e}')

    # Rotate log files to avoid filling up storage
    def rotateLog(self):
        
        self.logFileList = os.listdir() 

        # Delete the oldest allowed logfile if it exists
        if self.maxLogFileName in self.logFileList:
            os.remove(self.maxLogFileName)
            print(f"Deleting logfile {self.maxLogFileName}")
        
        # Rename other log files if they exist 4 becomes 5 etc
        # Note: when this while loop exits self.currentLogFile is the name of the log file used by writeToDebugLog
        self.logFileNum = self.maxLogFiles - 1
        while self.logFileNum > 0:
            self.currentLogFile = self.logFilePrefix + str(self.logFileNum) + '.log'
            if self.currentLogFile in self.logFileList:
                print(f"Renaming logfile {self.currentLogFile}")
                os.rename(self.currentLogFile, self.logFilePrefix + str(self.logFileNum + 1) + '.log')
            self.logFileNum -= 1


    def main(self):
        self.writeToDebugLog('starting')

if __name__ == '__main__':
    dm = Test()
    dm.main()