# -*- coding: UTF-8 -*-
import os
import struct as st
import re

class InfChnls:
    'ChnlNames in one Inf file'

    def __init__(self, FileName):
        self.FileName = FileName

    @property
    def getChnls(self):
        if os.path.exists(self.FileName):
            from os import stat
            statinfo = stat(self.FileName)
            filelen = statinfo.st_size

            chnllen = 122  # every channel has 122 bytes
            chnlcnt = int(filelen / chnllen)
            infFile = open(self.FileName, 'rb')
            chnlNames = []
            for i in range(chnlcnt):
                increment = 122 * i
                offset = increment+12  # from 12 bytes
                infFile.seek(offset)
                content = infFile.read(12)  # channel name has 12 bytes

                indexEnd = len(content)
                for i in range(indexEnd):
                    if content[i] == 0:
                        indexEnd = i
                        break

                for i in range(indexEnd) :
                    if content[i] > 127:
                        indexEnd1 = i
                        break

                chnl = content[:indexEnd].decode('gbk')
                # channel conditionnig
                name = re.sub('\W', '', chnl)
                chnlNames.append(name)

            infFile.close()
            return chnlNames

        else:
            print('inf file do not exists!')
