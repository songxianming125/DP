# -*- coding: UTF-8 -*-
import os
import struct as st
import re
import InfDas



class InfDasN:
    'more channel for Das informations in one Inf file'

    def __init__(self, FileName):
        self.FileName = FileName


    def getInfDasN(self, ChnlIndexN):
        if os.path.exists(self.FileName):
            from os import stat
            myInfs = []
            statinfo = stat(self.FileName)
            filelen = statinfo.st_size

            chnllen = 122  # every channel has 122 bytes
            chnlcnt = int(filelen / chnllen)
            infFile = open(self.FileName, 'rb')
            contents = infFile.read()  # all channel information is read and stored in contents
            for ChnlIndex in ChnlIndexN:
                increment = chnllen * ChnlIndex
                content = contents[increment:increment+chnllen]
                myInfs.append(InfDas.InfDas(content))

            infFile.close()
            return myInfs
        else:
            print("no this file")
            return -1

    def getInfDas(self, ChnlIndex):
        if os.path.exists(self.FileName):
            from os import stat
            myInfs = []
            statinfo = stat(self.FileName)
            filelen = statinfo.st_size

            chnllen = 122  # every channel has 122 bytes
            chnlcnt = int(filelen / chnllen)
            infFile = open(self.FileName, 'rb')
            offset = chnllen*ChnlIndex  # ChnlIndex channel offset
            infFile.seek(offset)
            content = infFile.read(chnllen)  # one channel length is 122
            infFile.close()
            return InfDas.InfDas(content)
        else:
            print("no this file")
            return -1


"""
infs = InfDasN('C:\\das\\80000\\INF\\80030vol.INF')
cns = infs.getInfDasN
print("channels:", str(cns[0].ChnlId))
"""