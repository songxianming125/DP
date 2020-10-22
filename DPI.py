# "DP by Dr. SONG"
# mode 0=hl2a, 1=localdas, 2=exl50, 3=east, 4=hl2m
# manual mode, 1=set mode, 2 =run

from MDSplus import *
import InfDasN
import DataDasN
import InfChnl
import os
import re
import sys
import struct as st
import scipy.io as sio
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

__all__ = ["exl50db", "hl2adb", "eastdb", "getChannelsInTree", "sct", "sctAD", "mode", "getDateTime"]

# the DP subroutine
# the default value for DP

mode = 2  # 0=driver mode   0=hl2a,1=local, 2=exl50,3=east,4=hl2m
myStart = 0  # time window start
myEnd = 10000  # time window end in second
myFrq = 1  # interpolation or frequency
isLocalData = 0

# for local reading, you need  to set environment variable :
# exl50_path = 192.168.0.100::/home/ennfusion/TREES/exl50
#


def getIpTree4Machine(machine):
    if machine=='exl50':
        IpAddress = '192.168.20.11'
        strTreeName = ['exl50']
    elif machine=='east':
        IpAddress = 'mds.ipp.ac.cn'  # 202.127.204.12
        strTreeName = ['pcs_east', 'east', 'efitrt_east']

    return IpAddress, strTreeName

def getDateTime(machine,shotNumber):
    IpAddress, strTreeName = getIpTree4Machine(machine)
    conn = Connection(IpAddress)
    CurrentChannel = 'ip'
    tree = conn.openTree(strTreeName[0], shotNumber)

    # strCMD = 'getnci("\\\\' + strTreeName[0] +  '::TOP:FBC:' + CurrentChannel + '","TIME_INSERTED")'
    strCMD = 'DATE_TIME(getnci("\\\\' + strTreeName[0] + '::TOP:FBC:' + CurrentChannel + '","TIME_INSERTED"))'
    strTime = conn.get(strCMD)
    conn.closeAllTrees()
    conn.disconnect()
    return strTime

def getChannelsInTree(conn, tree, shotNumber, isSpecial):
    # isSpecial=1, with AD data and layer 3
    # after connect
    myChnlString = ';'

    # storage of all mds path names below TOP
    Level_0 = '\\' + tree + '::TOP'  # Top tree name
    Level_1 = 'getnci("\\' + Level_0 + '.*","FULLPATH")'
    # Level_1 = 'getnci("\\' + Level_0 + '.*","NODE_NAME")'




    try:
        Level_1s = conn.get(Level_1)
        Level_2s = []   # use for layer 4
        Levels = np.append(Level_1s, Level_0)
        if isSpecial == 1:
            for i in range(len(Level_1s)):
                L1=Level_1s[i]
                L1 = re.sub(r'\s+', "", str(L1), count=0, flags=0)
                Level_2 = 'getnci("\\' + L1 + '.*","FULLPATH")'
                try:

                    L2 = conn.get(Level_2)
                    Level_2s = np.append(Level_2s, L2)
                    Levels = np.append(Levels, L2)
                except:
                    pass
                else:
                    pass
        else:
            pass
    except:
        Levels = [Level_0]
    else:
        pass
    # get variable names from mds


    for i in range(len(Levels)):
        mds_nam = Levels[i]
        mds_nam=re.sub('\s+', "", mds_nam, count=0, flags=0)
        # mdscmd = 'getnci("\\' + mds_nam + ':*","FULLPATH")'
        mdscmd = 'getnci("\\' + mds_nam + ':*","NODE_NAME")'
        try:
            mychs=conn.get(mdscmd)  # get  variable  names from mds   end
            for ii in range(len(mychs)):
                if isSpecial == 1:
                    pattern='TOP\.AI|TOP.MNT'
                    searchObj = re.search(pattern, mdscmd, re.I)

                    if searchObj is None:
                        mych=mychs[ii]
                    else:
                        mych='AD' + mychs[ii]  # direct data acquisition
                else:
                    mych=mychs[ii]

                mych = re.sub('\s+', "", mych.value, count=0, flags=0)  # cancel the blank
                patternrep=';' + mych +';'   # repitition

                searchObj=re.search(patternrep,myChnlString,re.I)
                if searchObj is None:
                    myChnlString = myChnlString + mych + ';'
                else:
                    pass
        except:
            pass
        else:
            pass

            # pattern = re.compile(r'[\w]+$')
            # matchObj = pattern.search(mychs[ii].value)
            # if matchObj:
            #     mych=matchObj.group()
            #     myChnlString = myChnlString + mych + ';'
            # else:
            #     pass

        # channelNames = [mdsvalue('getnci("\\pcs_east::TOP:*","FULLPATH")');
        # mdsvalue('getnci("\\pcs_east::TOP.*:*","FULLPATH")')];

        # pattern = re.compile(r'[^\s\o0]*')
        # channelNames = pattern.findall(channelNames)

        # pattern = re.compile(r'[\w]*\Z')
        # channelNames = pattern.findall(channelNames)


        # index = ~cellfun( @ isempty, channelNames);
        # channelNames = channelNames(index);

    return myChnlString

def sct(machine,shotNumber):

    IpAddress, strTreeName = getIpTree4Machine(machine)
    conn = Connection(IpAddress)
    myChnlString=''

    for i in range(len(strTreeName)):
        tree = conn.openTree(strTreeName[i], shotNumber)
        myChnlString = myChnlString + ':' + strTreeName[i] + ':'
        Chnl=getChannelsInTree(conn, strTreeName[i], shotNumber, 0)
        myChnlString = myChnlString + Chnl

    conn.closeAllTrees()
    conn.disconnect()

    ChnlFile = 'machine\\' + machine + '.mat'
    treeChnlFile = os.path.join(os.getcwd(), ChnlFile)

    sio.savemat(treeChnlFile, {'myChnlString': myChnlString})

def sctAD(machine,shotNumber):

    IpAddress, strTreeName = getIpTree4Machine(machine)
    conn = Connection(IpAddress)
    myChnlString=''

    for i in range(len(strTreeName)):
        tree = conn.openTree(strTreeName[i], shotNumber)
        myChnlString = myChnlString + ':' + strTreeName[i] + ':'
        Chnl=getChannelsInTree(conn, strTreeName[i], shotNumber, 1)
        myChnlString = myChnlString + Chnl

    conn.closeAllTrees()
    conn.disconnect()

    ChnlFile = 'machine\\' + machine + '.mat'
    treeChnlFile = os.path.join(os.getcwd(), ChnlFile)

    sio.savemat(treeChnlFile, {'myChnlString': myChnlString})


def exl50db(shotNumber, channelName, *args):
    global mode
    mode = 2

    if isLocalData:
        strTreeName=getTreeName(channelName)
        # current shot :Tree.getCurrent('exl50')
        if len(args) == 1:
            timeWindow = args[0]

        patternDigital = re.compile(r'[-\d\.]+')
        timeResults = patternDigital.findall(timeWindow)
        startTime = float(timeResults[0])
        endTime = float(timeResults[1])
        stepTime = float(timeResults[2])
        myTree = Tree(strTreeName, shotNumber)

        myTree.setTimeContext(startTime, endTime, stepTime)
        n1 = myTree.getNode(r"\{}".format(channelName))

        # if n1.isSegmented():
        #
        #     dt = n1.getSegment(0).dims[0].delta
        #     xs = n1.getSegmentStart(0)
        #     xe = n1.getSegmentEnd(-1)
        #     x = np.arange(xs, xe + dt, dt)
        # else:
        #     x = n1.getData().dim_of()

        x = n1.getData().dim_of()
        if type(x) is np.ndarray:
            pass
        else:
            x=x.data()

        y = n1.getData().value_of()
        if type(y) is np.ndarray:
            pass
        else:
            y=y.data()

        myTree.close()
        U='au'
        return x, y, U  # s --> s

    else:
        [IPAddress, tree] = getIpTree4Machine('exl50')
        x, y, U = dbs(IPAddress, shotNumber, channelName, *args)
        return x, y, U  # s -->


def eastdb(shotNumber, channelName, *args):
    global mode
    mode = 3
    [IPAddress, tree] = getIpTree4Machine('east')
    x, y, U = dbs(IPAddress, shotNumber, channelName, *args)
    return x, y, U  # s --> ms


def dbs(serveName, shotNumber, channelName, *args):
    strTreeName = getTreeName(channelName)
    conn = Connection(serveName)
    tree = conn.openTree(strTreeName, shotNumber)
    if len(args) == 1:
        timeWindow = args[0]
        if timeWindow:
            patternDigital = re.compile(r'[-\d\.]+')
            timeResults = patternDigital.findall(timeWindow)

            timeContext='SetTimeContext(' + timeResults[0] + ',' + timeResults[1] + ',' + timeResults[2] +')'
            conn.get(timeContext)


    x = conn.get(r"dim_of(\{})".format(channelName))
    y = conn.get(r"\{}".format(channelName))
    U = conn.get(r"units_of(\{})".format(channelName))
    if type(x) is np.ndarray:
        pass
    elif (type(x) is Float32Array) and (len(x) ==1):
        x=x[0]
    else:
        x=x.value
    if type(y) is np.ndarray:
        pass
    elif (type(y) is Float32Array) and (len(y) ==1):
        y = y[0]
    else:
        y=y.value

    conn.closeAllTrees()
    return x, y, U    # s --> s


def changeDriver(newMode):

    global mode    # 0=hl,1=local
    mode = newMode



def getLatestShot():
    if mode is 0:
        myDriver = getDriver()
        dpfFileName = myDriver + '\\dpf\\hl2a.dpf'
        dpfFile = open(dpfFileName, 'rb')

        offset = 982  #
        dpfFile.seek(offset)
        content = dpfFile.read(4)  # channel name has 12 bytes
        shotNumber = st.unpack('l', content)[0]  # 4 bytes for long shot number

        dpfFile.close()
    elif mode is 1:
        shotNumber=80020
    elif mode is 2:

        if isMachineReady('exl50'):
            [IPAddress, tree] = getIpTree4Machine('exl50')
            conn = Connection(IPAddress)
            shotNumber = conn.get(r"current_shot('exl50')")
        else:
            pass

    elif mode is 3:

        if isMachineReady('east'):
            [IPAddress, tree] = getIpTree4Machine('east')
            conn = Connection(IPAddress)
            shotNumber = conn.get(r"current_shot('pcs_east')")
        else:
            pass

    if mode is 4:
        myDriver = getDriver()
        dpfFileName = myDriver + '\\dpf\\hl2a.dpf'
        dpfFile = open(dpfFileName, 'rb')

        offset = 982  #
        dpfFile.seek(offset)
        content = dpfFile.read(4)  # channel name has 12 bytes
        shotNumber = st.unpack('l', content)[0]  # 4 bytes for long shot number

        dpfFile.close()



    return shotNumber


def hl2adbSU(shotNumber, channelName):
    mySys = getSystemName(channelName)

    InfFileName = getInfFileName(shotNumber, mySys)
    infchs = InfChnl.InfChnls(InfFileName)
    cns = infchs.getChnls
    if len(str(cns)) < 5:  # None
        print("shot: %d has no this %s " % (shotNumber, channelName))
        myUnit = ''
    else:
        ChnlIndex = getChnlIndex(cns, channelName)
        if ChnlIndex > -1:
            myInfDas = InfDasN.InfDasN(InfFileName)
            myInf = myInfDas.getInfDas(ChnlIndex)
            myUnit = myInf.Unit
        else:
            myUnit = ''

    return mySys, myUnit


def getInf(shotNumber, channelName, *args):
    try:
        if len(args) == 1:
            mySys = args[0]
        elif len(args) == 4:
            mySys = args[3]
        else:
            mySys = getSystemName(channelName)

        InfFileName = getInfFileName(shotNumber, mySys)
        infchs = InfChnl.InfChnls(InfFileName)

        cns = infchs.getChnls
        ChnlIndex = getChnlIndex(cns, channelName)

        if ChnlIndex > -1:
            myInfDas = InfDasN.InfDasN(InfFileName)
            myInf = myInfDas.getInfDas(ChnlIndex)

    except:
        myInf=[];
    else:
        pass

    return myInf


def hl2adb(shotNumber, channelName, *args):
    if len(args) == 1:
        mySys = args[0]
    elif len(args) == 4:
        mySys = args[3]
    else:
        mySys = getSystemName(channelName)

    InfFileName = getInfFileName(shotNumber, mySys)
    infchs = InfChnl.InfChnls(InfFileName)
    cns = infchs.getChnls
    if len(str(cns)) < 5:  # None
        print("shot: %d has no this %s " % (shotNumber, channelName))
        x = 0
        y = 0
        U= 'au'
        return x, y
    ChnlIndex = getChnlIndex(cns, channelName)
    if ChnlIndex > -1:
        myInfDas = InfDasN.InfDasN(InfFileName)
        myInf = myInfDas.getInfDas(ChnlIndex)

        pattern = re.compile(r'(\.[iI][nN][fF])')
        DataFileName = re.sub(pattern, r'.dat', InfFileName)

        pattern = re.compile(r'([iI][nN][fF])')
        DataFileName = re.sub(pattern, r'DATA', DataFileName)
        # DataFileName = 'C:\\das\\80000\\DATA\\80030vol.DAT'

        myData = DataDasN.DataDasN(DataFileName, myStart, myEnd, myFrq)
        x, y = myData.getMycurve(myInf, *args)
        U = myInf.Unit

    else:
        print("shot: %d has no this %s " % (shotNumber, channelName))
        x = 0
        y = 0
        U = 'au'

    return x, y, U   # s->s


def hl2adbN(shotNumber, channelNameN, *args):  # output arguments are 4 with chnlNames
    # channelName is a list, all channel should be in one file
    if len(args) == 1:
        mySys = args[0]
    elif len(args) == 4:
        mySys = args[3]
    else:
        mySys = getSystemName(channelNameN[0])

    InfFileName = getInfFileName(shotNumber, mySys)
    infchs = InfChnl.InfChnls(InfFileName)
    cns = infchs.getChnls
    if len(str(cns)) < 5:  # None
        print("shot: %d has no this %s " % (shotNumber, channelNameN))
        x = 0
        y = 0
        return x, y

    # channelNameN can support regexp
    if (type(channelNameN) == str):
        pattern = re.compile(':(' + channelNameN + '):', re.I)
        channelNameN = pattern.findall(':' + ':'.join(cns) + ':')


    elif (type(channelNameN) == list):
        channelNameN = channelNameN

    ChnlIndexN = getChnlIndexN(cns, channelNameN)

    pattern = re.compile(r'(\.[iI][nN][fF])')
    DataFileName = re.sub(pattern, r'.dat', InfFileName)

    pattern = re.compile(r'([iI][nN][fF])')
    DataFileName = re.sub(pattern, r'DATA', DataFileName)

    myInfDas = InfDasN.InfDasN(InfFileName)
    myInfs = myInfDas.getInfDasN(ChnlIndexN)

    UnitN = []  # output the Unit
    for myInf in myInfs:
        UnitN.append(myInf.Unit)

    myData = DataDasN.DataDasN(DataFileName, myStart, myEnd, myFrq)  # initialize the class
    x, yN = myData.getMycurveN(myInfs, *args)

    return 1000*x, yN, channelNameN, UnitN  # s->ms


def getChnlIndex(myList, myChannel):
    for ii in range(len(myList)):
        # ignore the lower or upper

        matchObj = re.match(myList[ii], myChannel, re.I)

        if not (str(matchObj) == 'None') and len(myList[ii]) == len(myChannel):
            ChnlIndex = ii
            break
        else:
            ChnlIndex = -1

    return ChnlIndex


def getChnlIndexN(myList, myChannelList):
    chnlIndexN = []

    for jj in range(len(myChannelList)):
        # ignore the lower or upper

        for ii in range(len(myList)):
            matchObj = re.match(myList[ii], myChannelList[jj], re.I)

            if not (str(matchObj) == 'None') and len(myList[ii]) == len(myChannelList[jj]):
                ChnlIndex = ii
                break
            else:
                ChnlIndex = -1

        chnlIndexN.append(ChnlIndex)

    return chnlIndexN


def getDasDir(myShot):
    myThousands = int(myShot / 1000);
    myHundreds = int((myShot % 1000) / 100);
    myShotSpan = myThousands * 1000 + int((myHundreds) / 2) * 200;
    # make sure the string is 5 digit

    myDir = '00000' + str(myShotSpan);
    n = len(myDir);
    myDir = myDir[-5:]  # stem of shotnumber for filename
    return myDir


def getDriver():
    if mode is 0:
        myDriver = '\\\\hl\\2adas'
        if not (os.path.exists(myDriver)):
            user = input("请输入用户名：")
            psw = input("请输入用户密码：")

            cmd = 'net use ' + chr(32) + myDriver + chr(32) + psw + chr(32) + '/user:swip\\' + user
            os.system(cmd)

            if not (os.path.exists(myDriver)):
                print("no driver!")
                myDriver = 'c:\\das'

    elif mode is 1:
        myDriver = 'c:\\das'

    if mode is 4:
        myDriver = '\\\\hl\\2mdas'
        if not (os.path.exists(myDriver)):
            user = input("请输入用户名：")
            psw = input("请输入用户密码：")

            cmd = 'net use ' + chr(32) + myDriver + chr(32) + psw + chr(32) + '/user:swip\\' + user
            os.system(cmd)

            if not (os.path.exists(myDriver)):
                print("no driver!")
                myDriver = 'c:\\das'

    return myDriver


def getInfFileName(myShot, mySys):
    # myDriver = getDriver()
    myDir = getDasDir(myShot)
    myShotName = '00000' + str(myShot)
    myShotName = myShotName[-5:]  # should be five character
    myInfFileName = getDriver() + '\\' + myDir + '\\INF\\' + myShotName + mySys + '.inf'
    return myInfFileName


def isMachineReady(machine):
    # IpAddress = 'mds.ipp.ac.cn'  # 202.127.204.12
    # IpAddress = '192.168.20.11'  # exl50
    [IpAddress, tree] = getIpTree4Machine(machine)
    cmd = 'ping ' + IpAddress + '> pingInf.txt'
    tic = datetime.now()
    os.system(cmd)
    toc = datetime.now()
    elapsedSeconds=(toc-tic).total_seconds()

    pingInf = open('pingInf.txt', 'r')
    pingStatus = pingInf.read()
    pingInf.close()

    checkPattern = re.compile('已发送 = 4，已接收 = 4，丢失 = 0')
    mObj = checkPattern.search(pingStatus)

    if (mObj is None) or elapsedSeconds >10:
        return False

    else:
        return True

def setSystemName(myShot):
    # myDriver = getDriver()
    myDir = getDasDir(myShot)
    myShotName = '00000' + str(myShot)
    myShotName = myShotName[-5:]  # should be five character
    myInfDirFiles = getDriver() + '\\' + myDir + '\\INF\\' + myShotName + '* '

    cmd = 'dir ' + myInfDirFiles + '> chnl_systemFiles.txt'
    os.system(cmd)
    chnl_sysFile = open('chnl_systemFiles.txt', 'r')
    chnl_sys = chnl_sysFile.read()
    chnl_sysFile.close()

    pattern = re.compile(r'\d{5}([a-zA-Z]{3}).[iI][nN][fF]')
    systemNames = pattern.findall(chnl_sys)
    strSystemChnl = ''
    for i in range(len(systemNames)):
        if systemNames[i].lower() == 'vec':
            continue
        else:
            strSystemChnl = strSystemChnl + systemNames[i] + ':\n'
            InfFileName = getInfFileName(myShot, systemNames[i])
            infchs = InfChnl.InfChnls(InfFileName)
            chnls = infchs.getChnls
            for chnl in chnls:
                strSystemChnl = strSystemChnl + ';' + chnl  + ';\n'

    if mode is 0:
        SystemChnlFile=os.path.join(os.getcwd(), 'machine\\systemNameFile0.txt')
    elif mode is 1:
        SystemChnlFile=os.path.join(os.getcwd(), 'machine\\systemNameFile1.txt')
    elif mode is 4:
        SystemChnlFile=os.path.join(os.getcwd(), 'machine\\systemNameFile4.txt')

    systemNameFile = open(SystemChnlFile, 'w')
    n = systemNameFile.writelines(strSystemChnl)
    systemNameFile.close()


def getSystemName(channelName):

    if mode == 2:
        treeChnlFile = os.path.join(os.getcwd(), 'machine\\exl50.mat')
    elif mode == 3:
        treeChnlFile = os.path.join(os.getcwd(), 'machine\\east.mat')


    if mode is 0:
        SystemChnlFile=os.path.join(os.getcwd(), 'machine\\systemNameFile0.txt')
    elif mode is 1:
        SystemChnlFile=os.path.join(os.getcwd(), 'machine\\systemNameFile1.txt')
    elif mode is 4:
        SystemChnlFile=os.path.join(os.getcwd(), 'machine\\systemNameFile4.txt')

    chnl_sysFile = open(SystemChnlFile, 'r')
    chnl_sys = chnl_sysFile.read()
    chnl_sysFile.close()

    pattern = re.compile(';' + channelName + ';', re.I)
    mObj = pattern.search(chnl_sys)
    if len(str(mObj)) < 5:  # no chnl find
        mySys = []
    else:
        myString = mObj.group()
        myStart = mObj.start()
        pattern = re.compile('([a-zA-Z]{3}:)')
        sysList = pattern.findall(chnl_sys)
        for i in range(0, len(sysList)):
            pattern = re.compile(sysList[i])
            mObj = pattern.search(chnl_sys)
            mySysStart = mObj.start()
            if mySysStart > myStart:
                mySys = sysList[i - 1]
                break
            else:
                mySys = sysList[i]

    return mySys[:3]


def getTreeName(channelName):
    #  .mat version


    if mode == 2:
        if sys.platform in ['linux', 'darwin']:
            treeChnlFile = os.path.join(os.getcwd(), 'machine/exl50.mat')
        else:
            treeChnlFile = os.path.join(os.getcwd(), 'machine\\exl50.mat')
    elif mode == 3:
        treeChnlFile = os.path.join(os.getcwd(), 'machine\\east.mat')


    # if not (os.path.exists(treeChnlFile)):


    a = sio.loadmat(treeChnlFile)
    chnl_sys = str(a['myChnlString'])

    pattern = re.compile(';' + channelName + ';', re.I)
    mObj = pattern.search(chnl_sys)
    if len(str(mObj)) < 5:  # no chnl find
        mySys = []  # myTree
    else:
        myString = mObj.group()
        myStart = mObj.start()
        pattern = re.compile(':' + '\w*' + ':')
        sysList = pattern.findall(chnl_sys)
        for i in range(len(sysList)):
            pattern = re.compile(sysList[i])
            mObj = pattern.search(chnl_sys)
            mySysStart = mObj.start()
            if mySysStart > myStart:
                mySys = sysList[i - 1]
                break
            else:
                mySys = sysList[i]

    """
    #  .txt version
    mode =3
    channelName='pcpf1'

    if mode is 2:
        treeChnlFile = 'C:\\DataProc\\exl50\\exl50.txt'
    elif mode is 3:
        treeChnlFile = 'C:\\DataProc\\east\\east.txt'

    chnl_sysFile = open(treeChnlFile, 'r')
    chnl_sys = chnl_sysFile.read()
    chnl_sysFile.close()

    pattern = re.compile(';' + channelName + ';', re.I)
    mObj = pattern.search(chnl_sys)
    if len(str(mObj)) < 5:  # no chnl find
        mySys = []  # myTree
    else:
        myString = mObj.group()
        myStart = mObj.start()
        pattern = re.compile(':' + '\w*' + ':')
        sysList = pattern.findall(chnl_sys)
        for i in range(1, len(sysList)):
            pattern = re.compile(sysList[i])
            mObj = pattern.search(chnl_sys)
            mySysStart = mObj.start()
            if mySysStart > myStart:
                mySys = sysList[i - 1]
                break
            else:
                mySys = sysList[i]
    """
    return mySys[1:-1]


def getChnlNode(channelName):

    # .mat version



    if mode == 2:
        treeChnlFile = os.path.join(os.getcwd(), 'machine\\exl50.mat')
    elif mode == 3:
        treeChnlFile = os.path.join(os.getcwd(), 'machine\\east.mat')

    a = sio.loadmat(treeChnlFile)
    chnl_sys = str(a['myChnlString'])

    # ??? why plus ';', more channel ignored
    # patternChnl = re.compile(';\w*' + channelName + '\w*;', re.I)

    patternChnl = re.compile('\w*' + channelName + '\w*', re.I)
    chnlList = patternChnl.findall(chnl_sys)

    myChnlSys = []
    if len(chnlList) == 0:  # no chnl find
        pass
    else:
        for chnl in chnlList:
            patternChnl = re.compile(chnl, re.I)
            mObj = patternChnl.search(chnl_sys)
            myStart = mObj.start()

            patternSyS = re.compile(':' + '\w*' + ':')
            sysList = patternSyS.findall(chnl_sys)

            for i in range(len(sysList)):
                pattern1 = re.compile(sysList[i])
                mObj = pattern1.search(chnl_sys)
                mySysStart = mObj.start()

                if mySysStart > myStart:
                    myChnlSysFind = sysList[i - 1][1:] + chnl
                    break
                else:
                    myChnlSysFind = sysList[i][1:] + chnl

            myChnlSys.append(myChnlSysFind)

            """
    # .txt version
    if mode is 2:
        treeChnlFile = 'C:\\DataProc\\exl50\\exl50.txt'
    elif mode is 3:
        treeChnlFile = 'C:\\DataProc\\east\\east.txt'

    chnl_sysFile = open(treeChnlFile, 'r')
    chnl_sys = chnl_sysFile.read()
    chnl_sysFile.close()

    # ??? why plus ';', more channel ignored
    # patternChnl = re.compile(';\w*' + channelName + '\w*;', re.I)

    patternChnl = re.compile('\w*' + channelName + '\w*', re.I)
    chnlList = patternChnl.findall(chnl_sys)

    myChnlSys = []
    if len(chnlList) == 0:  # no chnl find
        pass
    else:
        for chnl in chnlList:
            patternChnl = re.compile(chnl, re.I)
            mObj = patternChnl.search(chnl_sys)
            myStart = mObj.start()

            patternSyS = re.compile(':' + '\w*' + ':')
            sysList = patternSyS.findall(chnl_sys)

            for i in range(1, len(sysList)):
                pattern1 = re.compile(sysList[i])
                mObj = pattern1.search(chnl_sys)
                mySysStart = mObj.start()

                if mySysStart > myStart:
                    myChnlSysFind = sysList[i - 1][1:] + chnl
                    break
                else:
                    myChnlSysFind = sysList[i][1:] + chnl

            myChnlSys.append(myChnlSysFind)
    """


    return myChnlSys


def getChnlPattern(channelName):
    if mode is 0:
        SystemChnlFile=os.path.join(os.getcwd(), 'machine\\systemNameFile0.txt')
    elif mode is 1:
        SystemChnlFile=os.path.join(os.getcwd(), 'machine\\systemNameFile1.txt')
    elif mode is 4:
        SystemChnlFile=os.path.join(os.getcwd(), 'machine\\systemNameFile4.txt')

    chnl_sysFile = open(SystemChnlFile, 'r')
    chnl_sys = chnl_sysFile.read()
    chnl_sysFile.close()


    # why plus ';', more channel ignored
    # patternChnl = re.compile(';\w*' + channelName + '\w*;', re.I)

    patternChnl = re.compile('\w*' + channelName + '\w*', re.I)
    chnlList = patternChnl.findall(chnl_sys)

    myChnlSys = []
    if len(chnlList)==0:  # no chnl find
        pass
    else:
        for chnl in chnlList:
            patternChnl = re.compile(chnl, re.I)
            mObj = patternChnl.search(chnl_sys)
            myStart = mObj.start()

            patternSyS = re.compile('([a-zA-Z]{3}:)')
            sysList = patternSyS.findall(chnl_sys)

            for i in range(1,len(sysList)):
                pattern1 = re.compile(sysList[i])
                mObj = pattern1.search(chnl_sys)
                mySysStart = mObj.start()

                if mySysStart > myStart:
                    myChnlSysFind=sysList[i-1] + chnl
                    break
                else:
                    myChnlSysFind = sysList[i] + chnl

            myChnlSys.append(myChnlSysFind)



    return myChnlSys

##  your code here





# x, y, U=exl50db(4912, 'ip','0:3:0.001')
# # x, y, U=hl2adb(36808,'I_div_imp2', 'MIF')
# plt.plot(x,y)
# plt.show()


# x,y, u=hl2adb(20000,'ipbuild',0,2,'1000hz','fbc')
# plt.plot(x,y)
# plt.show()
#
# x, y, U=hl2adb(37051, 'I_div_imp2', 0, 3, '1000hz', 'MIF')
# # x, y, U=hl2adb(36808,'I_div_imp2', 'MIF')
# plt.plot(x,y)
# plt.show()



#######################################


# setSystemName(37052)
# profile.run("s,u=hl2adbSU(80023,'U4U')")


# x, y, U=hl2adb(37051, 'I_div_imp2', 0, 3, '1000hz', 'MIF')
# # x, y, U=hl2adb(36808,'I_div_imp2', 'MIF')
# plt.plot(x,y)
# plt.show()


# x,y=hl2adb(36808,'I_div_imp2', 'MIF')")
# print(s)
# print(u)

# setSystemName(36808)

# x, y, U = eastdb(33038, 'pcpf1','0:10:0.1')
# plt.plot(x,y)
# plt.show()
#

# x, y=hl2adbN(36808, ['BOLU01','BOLU02','BOLU03'], -100000, 2000000, '10000hz', 'BLM')
# x, y=hl2adbN(36981, ['NBHE_I3VFil','NBHE_I3IArc','NBHE_I3ISnb'], 0, 2000000, '10000hz', 'IH2')

#
# x, yN, channelNameN, UnitN = hl2adbN(37052, 'mpol_[0-9][0-9]', 0, 2000, '10000hz', 'MIF')
# plt.plot(x, yN[0])
# plt.show()
# plt.plot(x, yN[1])
# plt.show()
# plt.plot(x, yN[2])
"""
try:
    plt.show()
except:
    pass
"""

"""

plt.plot(x,y)
plt.show()
x,y=hl2adb(36808,'I_div_imp2', 'MIF')

plt.plot(x,y)
plt.show()
x,y=hl2adb(36808,'I_div_imp2', 'MIF')

plt.plot(x,y)
plt.show()
x,y=hl2adb(36808,'I_div_imp2', 'MIF')

plt.plot(x,y)
plt.show()
x,y=hl2adb(36808,'I_div_imp2', 'MIF')

plt.plot(x,y)
plt.show()




x,y=hl2adb(36808,'lfdh', 'LFB')

plt.plot(x,y)
plt.show()




x,y=hl2adb(36808,'lfdh', 'LFB')

plt.plot(x,y)
plt.show()







setSystemName(80023)
s,u=hl2adbSU(80023,'U4U')




# x,y=hl2adb(80023,'UCS', 'vol')


"""
#  sct('east', 33038)
