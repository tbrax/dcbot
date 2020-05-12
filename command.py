
from hero import Hero

class Command:
    def __init__(self):
        self.h = Hero()
        self.bCode = '#'
        self.cds = {
                    'superCode':'{0}power'.format(self.bCode),
                    }

        self.badchars = ['\\','&','$','^','*',"'",'"','..']


    def formatCmd(self,cm):
        return '>>> {0}'.format(cm)

    def badInput(self,cm):
        for x in self.badchars:
            if (x in cm):
                return True
        return False

    def cmdMatch(self,cm,cd):
        if (cm.startswith('{0} '.format(cd))):
            return True
        return False


    def combineLines(self,lineList):
        st = ''
        for idx,line in enumerate(lineList):
            st += line
            if (idx is not (len(lineList)-1)):
                st += '\n'
        return st

    def command(self,cm):
        if (self.badInput(cm)):
            return False
        if self.cmdMatch(cm,self.cds['superCode']):
            return self.h.command(cm[len(self.cds['superCode']):])
        return False


    def splitLong(self,cds):
        strs = []
        totalLen = 0
        tmpLen = 0
        lns = cds.splitlines()
        totalList = []
        tempList = []
        charLimit = 1500
        for x in lns:
            ln = len(x)
            totalLen += ln
            tmpLen += ln
            if (tmpLen > charLimit):
                totalList.append(tempList)
                tempList = []
                tmpLen = 0
            tempList.append(x)
        totalList.append(tempList)

        for x in totalList:
            lns = self.formatCmd(self.combineLines(x))
            strs.append(lns)
        return strs

    def commandFront(self,cmd):
        
        cds = self.command(cmd)
        if (not cds):
            return False
        sp = self.splitLong(cds)
        return sp

    

def main():
    c = Command()
    cs = c.commandFront('#power magic --u')
    for x in cs:
        print(x)

if __name__ == "__main__":
    main()

   