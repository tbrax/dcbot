
import os
from os import path
from fileState import ParseText
import random
import distance

class Hero:
    def __init__(self):

        self.heroList = []
        self.heroLocation = 'C:\\Users\\trace\\projects\\python\\testread\\pages\\powers\\seperate'
        
        self.makeHeroList(self.heroLocation,self.heroList)
        self.cOptsNames = {
                            'basic':['--b',['Capabilities','Limitations','Applications','other']],
                            'known':['--u',['Known Users','Known Locations','Known Objects','known']],
                            'also:':['--n',['Also Called','Associations']],
                            'gallery':['--g',['Gallery']],
        }
        self.maxTerms = 15
        self.dis = 4


    
    def combineLines(self,lineList):
        st = ''
        for idx,line in enumerate(lineList):
            st += line
            if (idx is not (len(lineList)-1)):
                st += '\n'
        return st

    def matchName(self,n0,n1):
        if (n0.lower() == n1.lower()):
            return True
        return False

    def correctName(self,inputData):
        for x in self.heroList:
            if (self.matchName(x,inputData)):
                return True
        return False

    def removeTxt(self,f):
        rm = '.txt'
        if f.endswith(rm):
            f = f[:-len(rm)]
        return f

    def nameToList(self,fileName,hList):
        if '.txt' in fileName:
            fName = self.removeTxt(fileName)
            hList.append(fName)

    def makeHeroList(self,dirName,hList):
        for filename in os.listdir(dirName):
            self.nameToList(filename,hList)
        
    def powerNear(self,n0,n1):
        w0 = n0.split()
        w1 = n1.split()
        lim = min(self.dis,max(len(n0)-(self.dis-1),0))
        score = 0
        for x0 in w0:
            for x1 in w1:            
                ld = distance.levenshtein(x0, x1)
                if ld < lim:
                    score += (lim-ld)

        return score

    def nearNames(self,inputData):
        lines = []
        
        

        for x in self.heroList:
            n = self.powerNear(inputData,x)
            if n > 0:
                lines.append([n,x])

        sl = sorted(lines,key=lambda l:l[0],reverse=True)


        m = min(len(sl), self.maxTerms) 

        colsl = sorted([val[1] for val in sl[:m]],reverse=True)

        return self.combineLines(colsl)

    def findNear(self,inputData):
        sug = self.nearNames(inputData)
        st = ''
        if (len(sug) > 0):
            st = ', suggested \n{0}'.format(sug)
        
        return st

    def randomPower(self):
        return random.choice(self.heroList)

    def createOptions(self,opts):
        convertOpts = []

        for x in self.cOptsNames['basic'][1]:
            convertOpts.append(x)

        for x in opts:
            for key in self.cOptsNames:
                if x in self.cOptsNames[key][0]:
                    for z in self.cOptsNames[key][1]:
                        convertOpts.append(z)
        return convertOpts

    def seperateCmds(self,cmd):
        name = []
        opts = []
        sp = cmd.split()
        for x in sp:
            if (x.startswith('--')):
                opts.append(x)
            else:
                name.append(x)       
        fname = ''
        for idx,x in enumerate(name):
            fname += x
            if (idx < len(name)-1):
                fname += ' '
        
        ls = [fname,opts]
        return ls

    def classLoadPower(self,inputData,opts = []):
        p = ParseText(self)
        return p.loadPower(inputData,opts)

    def command(self,cmd):
        c = self.seperateCmds(cmd)
        if (c[0].lower() == 'random'):
            p = self.randomPower()
        else:
            p = c[0]
        if (self.correctName(p)):
            opts = c[1]
            l = self.classLoadPower(p,self.createOptions(opts))
            if (l):
                return l
            else:
                return 'Could not load {0}'.format(p)
        return 'Could not find "{0}" {1}'.format(p,self.findNear(p))


        

def main():
    h = Hero()
    print(h.ClassLoadPower('World Merging'))

if __name__ == "__main__":
    # execute only if run as a script
    main()
