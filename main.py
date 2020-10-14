from DPI import *
import matplotlib.pyplot as plt
from xml.dom.minidom import parse
import xml.dom.minidom



DOMTree = xml.dom.minidom.parse("options.xml")
options = DOMTree.documentElement
machine = options.getElementsByTagName("machine")
a=machine[0].childNodes[0].data


pass

#
# getDateTime('exl50',5695)
# sct('exl50', 5695)


#
# mode=3
# x, y, U = eastdb(33038, 'pcrl01')  # east machine

# x, y, U = exl50db(5443, 'U_PS1')  # exl50 machine


# x, y, U=exl50db(4912, 'ip','0:3:0.001')



## for hl2adb, you should set the mode parameter for working properly
# mode=    0=hl2a,1=local, 2=exl50,3=east,4=hl2m
# DPI.mode=0
# x, y, U=hl2adb(36808,'I_div_imp2', 'MIF')  # hl2a hl2m or local das




plt.plot(x, y)
plt.show()
