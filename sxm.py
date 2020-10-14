import math
import numpy as np
from scipy import interpolate
import pyqtgraph as pg
import struct as st
import sys

tickWidth=5


class SongAxis(pg.AxisItem):
    def tickStrings(self, values, scale, spacing):
        """Return the strings that should be placed next to ticks. This method is called
        when redrawing the axis and is a good method to override in subclasses.
        The method is called with a list of tick values, a scaling factor (see below), and the
        spacing between ticks (this is required since, in some instances, there may be only
        one tick and thus no other way to determine the tick spacing)

        The scale argument is used when the axis label is displaying units which may have an SI scaling prefix.
        When determining the text to display, use value*scale to correctly account for this prefix.
        For example, if the axis label's units are set to 'V', then a tick value of 0.001 might
        be accompanied by a scale value of 1000. This indicates that the label is displaying 'mV', and
        thus the tick should display 0.001 * 1000 = 1.
        """
        if self.logMode:
            return self.logTickStrings(values, scale, spacing)

        places = max(0, np.ceil(-np.log10(spacing * scale)))
        strings = []
        for v in values:
            vs = v * scale
            if abs(vs) < .001 or abs(vs) >= 10000:
                vstr = "%g" % vs
            else:
                vstr = ("%%0.%df" % places) % vs
            strings.append(vstr)
        return strings

    def tickSpacing(self, minVal, maxVal, size):
        yLim=[minVal, maxVal]
        myYLim, myTickY, myTickYLabel=MyYTick(yLim, 3, 1)
        return [(myYLim[1]-myYLim[0],0)]

    def setGrid(self, grid):
        """Set the alpha value (0-255) for the grid, or False to disable.

        When grid lines are enabled, the axis tick lines are extended to cover
        the extent of the linked ViewBox, if any.
        """
        self.grid = grid
        self.picture = None
        self.prepareGeometryChange()
        self.update()

    def tickValues(self, minVal, maxVal, size):
        self.setGrid(True)
        """
        Return the values and spacing of ticks to draw::

            [
                (spacing, [major ticks]),
                (spacing, [minor ticks]),
                ...
            ]

        By default, this method calls tickSpacing to determine the correct tick locations.
        This is a good method to override in subclasses.
        """
        minVal, maxVal = sorted((minVal, maxVal))

        minVal *= self.scale
        maxVal *= self.scale
        # size *= self.scale

        ticks = []
        tickLevels = self.tickSpacing(minVal, maxVal, size)
        allValues = np.array([])
        for i in range(len(tickLevels)):
            spacing, offset = tickLevels[i]

            ## determine starting tick
            start = (np.ceil((minVal - offset) / spacing) * spacing) + offset

            ## determine number of ticks
            num = 3
            spacing /= num

            start += spacing / 2
            values = (np.arange(num) * spacing + start) / self.scale
            ## remove any ticks that were present in higher levels
            ## we assume here that if the difference between a tick value and a previously seen tick value
            ## is less than spacing/100, then they are 'equal' and we can ignore the new tick.
            ticks.append((spacing / self.scale, values))

        # nticks = []
        # for t in ticks:
        # nvals = []
        # for v in t[1]:
        # nvals.append(v/self.scale)
        # nticks.append((t[0]/self.scale,nvals))
        # ticks = nticks

        return ticks


def ModifyYLimitTick(yLim,n):
    # n is the tick number
    n2=2*n

    yMax=yLim[1]
    yMin=yLim[0]
    dY=yMax-yMin
    #  conditionning, when no difference
    if dY==0:
        yMax +=1
        dY=1





    # find the power of ratio factor
    rn = math.floor(math.log(dY, 10))
    pr=math.pow(10, rn)

    if n == 3:
        zoomfactor=1.3
    elif n == 5:
        zoomfactor = 1.2

    step = zoomfactor * dY / n2

    # if n==3:
    fStep=np.array([0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0, 1.2, 1.5, 1.6, 1.8, 2.0])*pr
    # elif n==5:
    #     fStep=np.array([0.2, 0.4, 0.5, 0.6, 0.8, 1.0, 1.2, 1.5, 1.6, 1.8, 2.0])*pr

    # find the optimal step
    Index=0
    while (fStep[Index] <= step) and (Index<len(fStep)-1):
        Index += 1

    step = fStep[Index]

    adjustfactor=0.01
    if abs(yMax)>abs(yMin):
        yMin=math.floor(yMin/step-adjustfactor)*step
        yMax=yMin+n2*step
    elif abs(yMax)<abs(yMin):
        yMax=math.ceil(yMax/step+adjustfactor)*step
        yMin=yMax-n2*step

    return yMin, yMax, step


def getYData(x, y, xspan):
    index = range(len(x))
    f = interpolate.interp1d(x, index, kind='nearest', fill_value="extrapolate")
    indexStart = f(xspan[0])
    indexEnd = f(xspan[1])

    myY = y[int(indexStart):int(indexEnd)]

    return myY


def MyYTick(yLim, n, r, *args):
    # yLim is list with two number
    # n is the tick number, 3 is recommended
    # r is the number of accuracy。 digit number after point

    # gapMode =0  # 0=songxm mode, uniform, 1=conventional mode

    if len(args) == 0:
        gapMode = 0

    elif len(args) == 1:
        gapMode = args[0]

    elif len(args) == 2:
        gapMode = args[0]

    yMin, yMax, step = ModifyYLimitTick(yLim, n)
    numberRight=r

    Y = []

    if gapMode==0:  # control the YTick mode song mode or conventional mode
        for i in range(n):
            Y.append(yMin + (2 * i + 1) * step)  # first half, last half, middle one mode

    elif gapMode==1:  # conventional mode
        for i in range(n):
            Y.append((yMin + 2 * i * step)/pr)

    myYLim=[yMin, yMax]  # list
    myTickY=Y

    myTickYLabel=[]

    for myY in Y:
        if numberRight >= 0:

            YLabel =("%%0.%df" % numberRight) % myY
            YLabel = YLabel + '00000'
            YL = YLabel[:tickWidth]
            myTickYLabel.append(YL)

    return myYLim, myTickY, myTickYLabel

# RSA encryption


def MulMod(a,b,n):
    a = int(a)
    b = int(b)
    n = int(n)
    r = a*b % n
    return int(r)


def PowMod(a,p,n):
    a = int(a)
    p = int(p)
    n = int(n)
    if p == 1:
        r = a % n
    elif p == 2:
        r = a*a % n
    elif p > 2:
        r = a * a % n
        for i in range(p-2):
            r = MulMod(r, a, n)

    return int(r)



def getPartner(e,f):
    c = 1

# r=0;
# [G,C,D] = gcd(e,f);
# if G==1
#     r=C;
# end

    return c


def getPhi(n):

    f = 1

    # # Euler function Phi
    # factor and minus 1 and multiply
    # if n==143
    #     p1=11;
    #     p2=13;
    #     f=(p1-1)*(p2-1);
    # end
    return f

# % prime table:
# % p=[2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113];
# %p=primes(120);
# %n= 143(11*13),(13,37),(23,47)
#
#
# % n=11*31=341 f=10*30=300
# % (7,43) (17,53) (19,79) (37,73)
#
#
# %% big prime
# % less than 256, the top 3 primes=[239 241 251] n=239*241=57599, f=238*240=, e=251
# % its parter=19571
# %(251,19571), (19,9019),(11,20771) (23,4967) (29,5909),(31,22111) (191,15551)
#
#
#
# % less than 256, the top 3 primes=[239 241 251] n=251*241=60491, f=250*240=60000
# %(7,17143), (13,23077),(23,26087), (29,2069)
#
#
# % less than 300 top three 281   283   293   n=251*271=68021 f=250*270=67500
# % (17,19853) (37,5473) (7,9643)
#
# % less than 1000 top three  983   991   997  n=991*997= 988027 f=990*996=986040
# % (911,306311)                       (37,5473) (7,9643)
#


def encrRSA(yourRSAString, n, e):
    myLen = len(yourRSAString)
    # myData = yourRSAString.encode('gb2312')
    # % f = getPhi(n);
    # % p = getPartner(e, f);
    myInt=[]

    for i in range(myLen):
        myData = yourRSAString[i].encode('gbk')
        if len(myData) == 1:
            myIntData=st.unpack('B', myData)[0]

        elif len(myData) == 2:
            myIntData=st.unpack('H', myData)[0]

        # encryption
        myDataInt = PowMod(myIntData, e, n)

        myInt.append(str(myDataInt))

    return myInt


def decrRSA(myRSAData, n, e):

    myLen = len(myRSAData)

    # % f = getPhi(n)
    # % p = getPartner(e, f)

    yourRSAString=''
    for i in range(myLen):
        # decryption from myDataInt
        myIntData = PowMod(int(myRSAData[i]), e, n)
        if myIntData<256:
            yourRSAString += st.pack('B', myIntData).decode('gbk')
        elif myIntData<65536:
            yourRSAString += st.pack('H', myIntData).decode('gbk')

    originalString = yourRSAString

    return originalString

# bigPrime=60491;
# keyFirst=29;
# keySecond=2069;
# 7,9643


myData=encrRSA('宋显明', 68021, 9643)
myString=decrRSA(myData, 68021, 7)
pass
