# -*- coding: UTF-8 -*-
import os
import struct as st
import re


class InfDas:
    'Das informations in one Inf file'
    FileType = 'C'*10  # 'SWIP_DAS__' # 10 bytes
    ChnlId = int(0)  # 2 bytes  type=uint16
    ChnlName = 'C'*12  # 12 bytes
    Addr = int(0)  # 4 bytes
    Freq = float(0)  # 4 bytes
    Len = int(0)  # 4 bytes
    Post = int(0)  # 4 bytes
    MaxDat = int(0)  # 2 bytes type=uint16
    LowRang = float(0)  # 4 bytes
    HighRang = float(0)  # 4 bytes
    Factor = float(0)  # 4 bytes
    Offset = float(0)  # 4 bytes
    Unit = 'C'*8  # 8 bytes
    Dly = float(0)  # 4 bytes
    AttribDt = int(0)  # 2 bytes
    DatWth = int(0)  # 2 bytes
    # Sum = 74
    SparI1 = int(0)  # 2 bytes
    SparI2 = int(0)  # 2 bytes
    SparI3 = int(0)  # 2 bytes
    SparF1 = float(0)  # 4 bytes
    SparF2 = float(0)  # 4 bytes
    SparC1 = 'C'*8  # 8 bytes
    SparC2 = 'C'*16  # 16 bytes
    SparC3 = 'C'*10  # 10 bytes
    # Sum = 122
    infStrBin = 'c'*122

    def __init__(self, infString):
        # infStr=infString.encode(encoding='UTF-8',errors='strict')
        if len(infString)<122:
            print("binary bytes is less than 122 long")
        else:
            infStr=infString
            self.infStrBin = infStr
            iStart=0
            iEnd=10
            # myStr = st.unpack('cccccccccc', infStr[iStart:iEnd])  # 'SWIP_DAS__' # 10 bytes
            indexEnd = iEnd
            for i in range(iStart,iEnd):
                if infStr[i]==0:
                    indexEnd=i
                    break
            self.FileType = bytes.decode(infStr[iStart:indexEnd])  # 'SWIP_DAS__' # 10 bytes
            iStart=iEnd
            iEnd=iStart+2
            self.ChnlId=st.unpack('H', infStr[iStart:iEnd])[0]  # 2 bytes  type=uint16
            iStart=iEnd
            iEnd=iStart+12
            indexEnd = iEnd
            for i in range(iStart,iEnd):
                if infStr[i]==0:
                    indexEnd=i
                    break

            self.ChnlName = bytes.decode(infStr[iStart:indexEnd])  # 12 bytes
            iStart=iEnd
            iEnd=iStart+4
            self.Addr = st.unpack('l', infStr[iStart:iEnd])[0]  # 4 bytes
            iStart=iEnd
            iEnd=iStart+4
            self.Freq = st.unpack('f', infStr[iStart:iEnd])[0]  # 4 bytes
            iStart=iEnd
            iEnd=iStart+4
            self.Len = st.unpack('l', infStr[iStart:iEnd])[0]  # 4 bytes
            iStart=iEnd
            iEnd=iStart+4
            self.Post = st.unpack('l', infStr[iStart:iEnd])[0]  # 4 bytes
            iStart=iEnd
            iEnd=iStart+2
            self.MaxDat = st.unpack('H', infStr[iStart:iEnd])[0]  # 2 bytes type=uint16
            iStart=iEnd
            iEnd=iStart+4
            self.LowRang = st.unpack('f', infStr[iStart:iEnd])[0]  # 4 bytes
            iStart=iEnd
            iEnd=iStart+4
            self.HighRang = st.unpack('f', infStr[iStart:iEnd])[0]  # 4 bytes
            iStart=iEnd
            iEnd=iStart+4
            self.Factor = st.unpack('f', infStr[iStart:iEnd])[0] # 4 bytes
            iStart=iEnd
            iEnd=iStart+4
            self.Offset = st.unpack('f', infStr[iStart:iEnd])[0]  # 4 bytes
            iStart=iEnd
            iEnd=iStart+8
            indexEnd = iEnd
            for i in range(iStart,iEnd):
                if infStr[i]==0:
                    indexEnd=i
                    break
            self.Unit = bytes.decode(infStr[iStart:indexEnd])  # 8 bytes
            iStart=iEnd
            iEnd=iStart+4
            self.Dly = st.unpack('f', infStr[iStart:iEnd])[0]  # 4 bytes
            iStart=iEnd
            iEnd=iStart+2
            self.AttribDt = st.unpack('h', infStr[iStart:iEnd])[0]  # 2 bytes
            iStart=iEnd
            iEnd=iStart+2
            self.DatWth = st.unpack('h', infStr[iStart:iEnd])[0]  # 2 bytes
            iStart=iEnd
            iEnd=iStart+2
            # Sum = 74
            self.SparI1 = st.unpack('h', infStr[iStart:iEnd])[0]  # 2 bytes
            iStart=iEnd
            iEnd=iStart+2
            self.SparI2 = st.unpack('h', infStr[iStart:iEnd])[0]  # 2 bytes
            iStart=iEnd
            iEnd=iStart+2
            self.SparI3 = st.unpack('h', infStr[iStart:iEnd])[0]  # 2 bytes
            iStart=iEnd
            iEnd=iStart+4
            self.SparF1 = st.unpack('f', infStr[iStart:iEnd])[0]  # 4 bytes
            iStart=iEnd
            iEnd=iStart+4
            self.SparF2 = st.unpack('f', infStr[iStart:iEnd])[0]  # 4 bytes
            iStart=iEnd
            iEnd=iStart+8
            indexEnd = iEnd
            for i in range(iStart,iEnd):
                if infStr[i]==0:
                    indexEnd=i
                    break
            self.SparC1 = bytes.decode(infStr[iStart:indexEnd])  # 8 bytes
            iStart=iEnd
            iEnd=iStart+16
            indexEnd = iEnd
            for i in range(iStart,iEnd):
                if infStr[i]==0:
                    indexEnd=i
                    break
            self.SparC2 = bytes.decode(infStr[iStart:indexEnd])  # 16 bytes
            iStart=iEnd
            iEnd=iStart+10
            indexEnd = iEnd
            for i in range(iStart,iEnd):
                if infStr[i]==0:
                    indexEnd=i
                    break
            self.SparC3 = bytes.decode(infStr[iStart:indexEnd])  # 10 bytes
            iStart=iEnd
            # Sum = 122


    def getInfStr(self):

        nullString16=st.pack('llll', 0, 0, 0, 0)
        myStr = 'SWIP_DAS'  # InfDas.FileType
        myFileType1=myStr.encode(encoding='UTF-8',errors='strict')  # FileType
        myFileType2=nullString16[:2]  # 2 bytes
        myChnlId=st.pack('H', self.ChnlId)  # 2 bytes  type=uint16
        myStrBin=myFileType1 + myFileType2 + myChnlId
        myStr = self.ChnlName  # ChnlName 12 bytes
        if len(myStr)<12:
            myStrBin = myStrBin + myStr.encode(encoding='UTF-8',errors='strict')+nullString16[:12-len(myStr)]
        else:
            myStrBin = myStrBin + myStr.encode(encoding='UTF-8',errors='strict')
        myStrBin = myStrBin + st.pack('l', self.Addr)  # 4 bytes
        # Sum = 28
        myStrBin = myStrBin + st.pack('f', self.Freq)  # 4 bytes
        myStrBin = myStrBin + st.pack('l', self.Len)  # 4 bytes
        myStrBin = myStrBin + st.pack('l', self.Post)  # 4 bytes
        myStrBin = myStrBin + st.pack('H', self.MaxDat)  # 2 bytes type=uint16
        myStrBin = myStrBin + st.pack('f', self.LowRang)  # 4 bytes
        myStrBin = myStrBin + st.pack('f', self.HighRang)  # 4 bytes
        myStrBin = myStrBin + st.pack('f', self.Factor)  # 4 bytes
        myStrBin = myStrBin + st.pack('f', self.Offset)  # 4 bytes
        # Sum = 58
        myStr = self.Unit  # 8 bytes
        if len(myStr) < 8:
            myStrBin = myStrBin + myStr.encode(encoding='UTF-8', errors='strict') + nullString16[:8 - len(myStr)]
        else:
            myStrBin = myStrBin + myStr.encode(encoding='UTF-8', errors='strict')
        myStrBin = myStrBin + st.pack('f', self.Dly)  # 4 bytes
        myStrBin = myStrBin + st.pack('h', self.AttribDt)  # 2 bytes
        myStrBin = myStrBin + st.pack('h', self.DatWth)  # 2 bytes
        # Sum = 74
        myStrBin = myStrBin + st.pack('h', self.SparI1)  # 2 bytes
        myStrBin = myStrBin + st.pack('h', self.SparI2)  # 2 bytes
        myStrBin = myStrBin + st.pack('h', self.SparI3)  # 2 bytes
        myStrBin = myStrBin + st.pack('f', self.SparF1)  # 4 bytes
        myStrBin = myStrBin + st.pack('f', self.SparF2)  # 4 bytes
        n = len(myStrBin)
        # Sum = 88
        myStr = self.SparC1  # 8 bytes
        if len(myStr)<8:
            myStrBin = myStrBin + myStr.encode(encoding='UTF-8',errors='strict')+nullString16[:8-len(myStr)]
        else:
            myStrBin = myStrBin + myStr.encode(encoding='UTF-8',errors='strict')
        myStr = self.SparC2  # 16 bytes
        if len(myStr)<16:
            myStrBin = myStrBin + myStr.encode(encoding='UTF-8',errors='strict')+nullString16[:16-len(myStr)]
        else:
            myStrBin = myStrBin + myStr.encode(encoding='UTF-8',errors='strict')
        myStr = self.SparC3  # 10 bytes
        if len(myStr)<10:
            myStrBin = myStrBin + myStr.encode(encoding='UTF-8',errors='strict')+nullString16[:10-len(myStr)]
        else:
            myStrBin = myStrBin + myStr.encode(encoding='UTF-8',errors='strict')
        # Sum = 122

        self.infStrBin = myStrBin
        return myStrBin


