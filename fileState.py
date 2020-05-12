import re

from statemachine import StateMachine, State
import os
from os import path

class FileMachine(StateMachine):
    beg = State('Beg', initial=True)
    summ = State('Summ')
    sec = State('Sec')
    users = State('User')
    gallery = State('Gallery')
    cate = State('Category')


    finishbeg = beg.to(summ)
    startsec = summ.to(sec)
    startuser = sec.to(users)
    startgallery = users.to(gallery)

    startcate0 = users.to(cate)
    startcate1 = gallery.to(cate)
    #def on_finishbeg(self):
    #    pront('Calma, lá!')
    #slowdown = green.to(yellow)
    #stop = yellow.to(red)
    #go = red.to(green)

class ParseText():
    def __init__(self, hero):
        self.hero = hero
        self.heroLocation = hero.heroLocation
        self.machine = FileMachine()
        #self.powerName = powerName
        #self.fullFile = fullFile
        self.section = 'none'
        self.formatReplace = [['[[',''],[']]','']]
        #self.opts = []
        
        #for x in opts:
        #    self.opts.append(x.lower())


    def getTitle(self,line):
        tx = '|Box title = '
        if (line.startswith(tx)):
            line = line[len(tx):]
        return line

    def _removeNonAscii(self,s): 
        return "".join(i for i in s if ord(i)<128)

    def formatText(self,txt):
        #txt = self._removeNonAscii(txt)
        txt = re.sub(r'{{scroll box|', '', txt)
        txt = re.sub(r'https?:\/\/([^\s\\])* ', '', txt)
        txt = re.sub(r'\[\[.*\|', ' ', txt)
        txt = re.sub(r'\]\]', '', txt)
        txt = re.sub(r'\[\[', '', txt)
        txt = re.sub(r'&quot;', '', txt)
        
        #txt = re.sub(r'â\xa0', '', txt)

        
        return txt

    def changeSec(self,s):
        s = s.replace('==','')
        s = s.lower()
        self.section = s

    def parseFile(self,fileData,opts):
        op = []
        for x in opts:
            op.append(x.lower())
        lines = self.parseLines(fileData,op)
        if (len(lines) == 2) and (lines[0] == '#REDIRECT'):
            return lines

        return self.hero.combineLines(lines)

    def loadFile(self,filePath):
        if (path.exists(filePath)):
            with open(filePath,'r',encoding='utf8') as f:
                readData = f.read()
                return readData
        return False

    def loadPower(self,inputData,opts):
        nameData = self.hero.correctName(inputData)
        if (nameData):
            p = self.loadPowerName(inputData,opts)
            return p
        return False

    def loadFileCaseIns(self,powerName):
        for fileName in os.listdir(self.heroLocation):
            p = self.hero.removeTxt(fileName)
            if (p.lower() == powerName.lower()):
                filePath = '{0}\\{1}'.format(self.heroLocation,fileName)
                loadedFile = self.loadFile(filePath)
                return loadedFile
        return False


    def redir(self,line):
        name = ''
        #p = ParseText(self.hero, self.powerName,self.opts)
        lines = 0

    def loadPowerName(self,powerName,opts):      
        loadedFile = self.loadFileCaseIns(powerName)
        if (loadedFile):
            data = self.parseFile(loadedFile,opts)
            if (data):
                if (data[0] == '#REDIRECT'):
                    p1 = ParseText(self.hero)
                    return p1.loadPowerName(data[1],opts)
                else:
                    return data  
        return False

    def getRedName(self,line):
        s0 = '#REDIRECT [['
        s1 = ']]<'
        beg = line.find(s0)
        end = line.find(s1)
        line = line[beg+len(s0):end]

        return line

    def parseLines(self,fileData,opts):
        lines = []
        section = 'none'
        for line in fileData.splitlines():
            if (self.machine.is_beg):

                if ('#REDIRECT' in line and '[[' in line):
                    return ['#REDIRECT', self.getRedName(line)]

                if ('|Box title' in line):
                    lines.append(self.getTitle(line))
                if ('}}' in line):
                    self.machine.finishbeg()
            elif (self.machine.is_summ):
                if ('==' in line):
                    self.changeSec(line)
                    self.machine.startsec()
                else:
                    if ('quote' not in line.lower()):
                        lines.append(self.formatText(line))
            elif (self.machine.is_sec):
                if ('==' in line):
                    self.changeSec('other')
                
                for x in self.hero.cOptsNames['known'][1]:
                    if (x in line):
                        self.machine.startuser()
                        self.changeSec(line)
                
                if 'known' in line.lower():
                    if (not self.machine.is_users):
                        self.machine.startuser()
                        self.changeSec('known')

                if (('allopts' in opts) or (self.section in opts)):
                    lines.append(self.formatText(line))

            elif (self.machine.is_users):               
                for x in self.hero.cOptsNames['gallery'][1]:
                    if (x in line):
                        self.machine.startgallery()
                        self.changeSec(line)
                if ('[[Category:' in line):
                    self.machine.startcate0()
                    self.changeSec('category')
                
                if (('allopts' in opts) or (self.section in opts)):
                    lines.append(self.formatText(line))

            elif (self.machine.is_gallery): 
                if ('[[Category:' in line):
                    self.machine.startcate1()
                    self.changeSec('category') 



                

        return lines