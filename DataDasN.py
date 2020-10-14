# -*- coding: UTF-8 -*-
import os
import struct as st
import InfDas
import numpy as np
from scipy import interpolate


class DataDasN:
    'more channel for Das informations in one Inf file'

    def __init__(self, FileName, myStart, myEnd, myFrq):
        self.FileName = FileName
        global myStart0, myEnd0, myFrq0
        myStart0=myStart
        myEnd0=myEnd
        myFrq0=myFrq


    @property
    def getDataDasN(self):
        if os.path.exists(self.FileName):
            from os import stat
            myInfs = []
            statinfo = stat(self.FileName)
            filelen = statinfo.st_size

            chnllen = 122  # every channel has 122 bytes
            chnlcnt = int(filelen / chnllen)

            infFile = open(self.FileName, 'rb')
            contents = infFile.read()  # all channel information is read and stored in contents
            for i in range(chnlcnt):
                increment = chnllen * i
                content = contents[increment:increment + chnllen]
                myInfs.append(InfDas.InfDas(content))

            infFile.close()
            return myInfs
        else:
            print("no this file")
            return -1

    def getMycurve(self, myInf,*args):
        if os.path.exists(self.FileName):
            dataFile = open(self.FileName, 'rb')
            #  read the data exactly long
            # default value is set here
            # reference the external variable
            myStart = myStart0
            myEnd = myEnd0
            myFrq = myFrq0
            mySys = ''

            if len(args) == 1:
                mySys = args[0]
            elif len(args) == 2:
                myStart = args[0]
                myEnd = args[1]

            elif len(args) == 3:
                myStart = args[0]
                myEnd = args[1]
                myFrq = args[2]

            elif len(args) == 4:
                myStart = args[0]
                myEnd = args[1]
                myFrq = args[2]
            #   mySys = args[3]
            else:
                print("check you argument")

            iStep = 1 / myInf.Freq  # swip use ms as the nature time unit
            #  the unit of myInf.Dly is what?
            iStartTime = myInf.Dly + (myInf.Post - myInf.Len) * iStep
            iEnd = iStartTime + iStep * (myInf.Len - 1)

            # make sure the input value is reasonable
            if myStart < iStartTime:
                myStart = iStartTime
            if myEnd > iEnd:
                myEnd = iEnd

            index = range(0, myInf.Len, 1)  # range([start,] stop[, step]), step=1 means original data
            indexArray = np.array(index, dtype=np.float32)
            # for interpolation
            x1 = iStartTime + indexArray * iStep
            # x1 = indexArray * iStep
            y1 = index

            # try to get the real x (time window)
            if type(myFrq) is int or type(myFrq) is float:
                myStep = myFrq
            elif type(myFrq) == str:
                if myFrq[-1].isalpha():
                    if myFrq[-2].isalpha():
                        myStep = 1 / float(myFrq[:-2])
                    else:
                        myStep = 1 / float(myFrq[:-1])
                else:
                    myStep = 1 / float(myFrq)

            f = interpolate.interp1d(x1, y1,kind='nearest', fill_value="extrapolate")
            x = np.arange(myStart, myEnd, myStep)  # swip use ms as the nature time unit

            indexY = np.array(f(x), dtype=int)

            # from where and read how many bytes???
            if myInf.AttribDt == 6:  # byte curve
                offset = 0 + indexY[0]*myInf.DatWth  # 1 For VB, 0 For python, C++ and Matlab
            else:
                offset = 0 + indexY[0]*myInf.DatWth + myInf.Addr  # 1 For VB, 0 For python, C++ and Matlab. myInf.Addr is the position of byte



            dataFile.seek(offset)
            myInf.Len = indexY[-1] - indexY[0]+1 # how many data
            content = dataFile.read(myInf.Len * myInf.DatWth)  # the total length is indexY[-1]*myInf.DatWth
            # indexY = range(0, myInf.Len, 1)
            y = self.getOneCurve(content, myInf, indexY - indexY[0])

            dataFile.close()
            return x, y
        else:
            print("no this curve")
            return 0,0

    def getMycurveN(self, myInfN, *args):
        if os.path.exists(self.FileName):
            dataFile = open(self.FileName, 'rb')
            #  read the data exactly long
            # default value is set here
            myStart = myStart0
            myEnd = myEnd0
            myFrq = myFrq0
            mySys = ''

            if len(args) == 1:
                mySys = args[0]
            elif len(args) == 2:
                myStart = args[0]
                myEnd = args[1]

            elif len(args) == 3:
                myStart = args[0]
                myEnd = args[1]
                myFrq = args[2]

            elif len(args) == 4:
                myStart = args[0]
                myEnd = args[1]
                myFrq = args[2]
            #   mySys = args[3]
            else:
                print("check you argument")

            yN=[]
            for myInf in myInfN:

                iStep = 1 / myInf.Freq
                iStartTime = myInf.Dly + (myInf.Post - myInf.Len) * iStep
                iEnd = iStartTime + iStep * (myInf.Len - 1)

                # make sure the input value is reasonable
                if myStart < iStartTime:
                    myStart = iStartTime
                if myEnd > iEnd:
                    myEnd = iEnd

                index = range(0, myInf.Len, 1)  # range([start,] stop[, step])
                indexArray = np.array(index, dtype=np.float32)
                # for interpolation
                x1 = indexArray * iStep
                y1 = index
                # try to get the real x (time window)
                if type(myFrq) is int or type(myFrq) is float:
                    myStep = myFrq
                elif type(myFrq) == str:
                    if myFrq[-1].isalpha():
                        if myFrq[-2].isalpha():
                            myStep = 1 / float(myFrq[:-2])
                        else:
                            myStep = 1 / float(myFrq[:-1])
                    else:
                        myStep = 1 / float(myFrq)

                f = interpolate.interp1d(x1, y1, kind='nearest', fill_value="extrapolate")
                x = np.arange(myStart, myEnd, myStep)  # swip use ms as the nature time unit

                indexY = np.array(f(x), dtype=int)

                # from where and read how many bytes???
                if myInf.AttribDt == 6:  # byte curve
                    offset = 0 + indexY[0]*myInf.DatWth  # 1 For VB, 0 For python, C++ and Matlab
                else:
                    offset = 0 + indexY[0]*myInf.DatWth + myInf.Addr  # 1 For VB, 0 For python, C++ and Matlab. myInf.Addr is the position of byte

                dataFile.seek(offset)
                myInf.Len = indexY[-1] - indexY[0] + 1  # how many data
                content = dataFile.read(myInf.Len * myInf.DatWth)  # the total length
                y = self.getOneCurve(content, myInf, indexY - indexY[0])
                yN.append(y)

            dataFile.close()
            return x, yN
        else:
            print("no this curve")
            return 0,0

    @classmethod
    def getOneCurve(cls, content, DasInfo, indexY):

        if DasInfo.AttribDt == 3: # direct phsical value
            if DasInfo.DatWth == 4:  # single float
                fmt='<' + str(DasInfo.Len) + 'f'
                """
                myData=[]
                for i in range(DasInfo.Len):
                    offset=i*DasInfo.DatWth
                    myData1 = st.unpack('f', content[offset:offset+DasInfo.DatWth])
                    myData2 = DasInfo.Factor * myData1[0] - DasInfo.Offset
                    myData.append(myData2)
                y=np.array(myData,dtype = np.float32)
                """
            elif DasInfo.DatWth == 8: # double float

                """
                myData=[]
                for i in range(DasInfo.Len):
                    offset=offset+i*DasInfo.DatWth
                    myData1 = st.unpack('d',content[offset:offset+DasInfo.DatWth])
                    myData2 = DasInfo.Factor * myData1[0] - DasInfo.Offset
                    myData.append(myData2)
                y=np.array(myData, dtype = np.float64)
                """
                fmt = '<' + str(DasInfo.Len) + 'd'

            y = st.unpack_from(fmt, content, 0)

            y = np.array(y)
            # y = np.reshape(y, (DasInfo.Len, -1))
            y = DasInfo.Factor * y - DasInfo.Offset





        elif (DasInfo.AttribDt == 2) or (DasInfo.AttribDt == 5):
            if DasInfo.DatWth == 2:  # int16
                fmt = '<' + str(DasInfo.Len) + 'H'
                """
                myData=[]
                for i in range(DasInfo.Len):
                    
                    offset=i*DasInfo.DatWth
                    myData1 = st.unpack('H', content[offset:offset+DasInfo.DatWth])
                    myData2 = DasInfo.Factor * (myData1[0]) - DasInfo.Offset
                    myData.append(myData2)
                y=np.array(myData,dtype = np.float32)
                """
            elif DasInfo.DatWth == 1: # int8
                fmt = '<' + str(DasInfo.Len) + 'B'
                """
                myData = []
                for i in range(DasInfo.Len):
                    offset = i * DasInfo.DatWth
                    myData1 = st.unpack('B', content[offset:offset + DasInfo.DatWth])
                    myData2 = DasInfo.Factor * (myData1[0]) - DasInfo.Offset
                    myData.append(myData2)
                y = np.array(myData, dtype=np.float32)
                
                """

            y = st.unpack_from(fmt, content, 0)
            y = np.array(y)
            # y = np.reshape(y, (DasInfo.Len, -1))
            y = DasInfo.Factor * y - DasInfo.Offset

        elif DasInfo.AttribDt == 1:  # real acq, may be large data
            if DasInfo.DatWth == 2:  # int16
                """
                fmt = '<' + str(myLength) + 'H'
                y2 = st.unpack_from(fmt, content[indexY], 0)
                y3 = np.reshape(y2, (DasInfo.Len, -1))
                y = DasInfo.Factor * (DasInfo.LowRang + y3 * (
                        DasInfo.HighRang - DasInfo.LowRang) / DasInfo.MaxDat) - DasInfo.Offset

                """
                fmt='<' + str(DasInfo.Len) +'H'


            elif DasInfo.DatWth == 1:  # int8
                fmt = '<' + str(DasInfo.Len) + 'B'

            y = st.unpack_from(fmt, content,0)
            y = np.array(y)
            # y=np.reshape(y,(DasInfo.Len,-1))
            y=DasInfo.Factor * (DasInfo.LowRang + y * (
                                DasInfo.HighRang - DasInfo.LowRang) / DasInfo.MaxDat) - DasInfo.Offset

        elif DasInfo.AttribDt == 6:  # bit curve
            myData = []
            # for i in range(DasInfo.Len):
            #     offset = i * DasInfo.DatWth
            #     myData1 = st.unpack('B', content[offset:offset + DasInfo.DatWth])
            #     myData2 = DasInfo.Factor * (DasInfo.LowRang + (myData1[0]) * (
            #                 DasInfo.HighRang - DasInfo.LowRang) / DasInfo.MaxDat) - DasInfo.Offset
            #     myData.append(myData2)

            fmt = '<' + str(DasInfo.Len) + 'B'

            #  ??? SONGXIANMING
            for i in range(DasInfo.Len):
                # DasInfo.Addr is the position of the byte
                offset = i * DasInfo.DatWth + int(DasInfo.Addr / 8)  # the number position of byte, 1=8 bits
                bitPosition = DasInfo.Addr%8
                valueInPosition=2**bitPosition
                myData1 = st.unpack('B', content[offset:offset+1])  # should have :
                myData2 = (valueInPosition & myData1[0])/valueInPosition  # cg 1 & 17 =0

                myData.append(myData2)
            y = np.array(myData, dtype=np.float32)
            # for display purpose, set the first two value
            y[0]=0
            y[1]=1

        y = y[indexY]

        return y





