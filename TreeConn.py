from MDSplus import *
import matplotlib.pyplot as plt
import numpy as np
# import scipy.io as sio
# import re
import math

strTreeName="exl50"
currentShot=1

myTree = Tree(strTreeName, currentShot)
# myTree.setTimeContext(1,2,0.0001)
# allChnl=myTree.getNodeWild("*").name
n1 = myTree.getNode("\\axuv006")

if n1.isSegmented():

    dt=n1.getSegment(0).dims[0].delta
    xs=n1.getSegmentStart(0)
    xe=n1.getSegmentEnd(-1)
    x=np.arange(xs,xe+dt,dt)
else:
    x = n1.getData().dim_of()


y=n1.getData().value_of()




myTree.close()

plt.plot(x, y)
plt.show()

"""
"""
#   remote data reading
#   asipp data from hefei

serveName='mds.ipp.ac.cn'
strTreeName='pcs_east'
currentShot=33038
conn = Connection(serveName)
tree=conn.openTree(strTreeName, currentShot)

# exec(r'x = conn.get(r"dim_of(\{})")'.format("auxv001"))
# exec(r'y=conn.get(r"value_of(\axuv001)")')
cn="pcpf1"
cmd ='x = conn.get(r"dim_of(\{})")'.format(cn)

exec(cmd)

y=conn.get(r"\pcpf1")

# x = conn.get(r"dim_of(\pcpf1[1:2:0.01])")
# y=conn.get(r"\pcpf1[1:2:0.01]")

conn.closeAllTrees()

plt.plot(x, y)
plt.show()
i=1





"""



from mdsconnector import mdsConnector
#help(mdsConnector)
# serveName='mds.ipp.ac.cn'
# strTreeName='east'
# currentShot=33038




from mdsconnector import mdsConnector

serveName='mds.ipp.ac.cn'
strTreeName='east'
currentShot=33038

c = mdsConnector(serveName)
t = c.Tree(strTreeName, currentShot)
n = t.getNode('pcpf1')
d1 = n.record  ##### data remains on remote host
d2 = n.execute('$ + 10', d1)  ##### data remains on remote host
d3 = d2.data()  ##### d3 is a numpy array on local host
d4 = c.Data.execute('$ + 10', d3)  ### d3 is sent to remote data remains on remote
d5 = d4.data()  ##### d5 is a numpy array on local host

serveName="192.168.0.100"
strTreeName="exl50"
currentShot=10
conn = Connection(serveName)



# serveName='mds.ipp.ac.cn'
# strTreeName='pcs_east'
# currentShot=33038
# conn = Connection(serveName)


# result = conn.get("(MY_NODE:DATA * $1)*$2" , Int32(2), Int32(10))



#conn.closeAllTrees()
#tree=conn.openTree("east", currentShot)
tree=conn.openTree(strTreeName, currentShot)
#tree=conn.openTree("rtefit", currentShot)


# tree = conn.Tree(experiment, shot)
#
# topNode = tree.getNode("\\TOP")

# t = conn.get(r"dim_of(\pcpf1)")
# y=conn.get(r"\pcpf1")

exec(r't = conn.get(r"dim_of(\{})")'.format("auxv001"))
exec(r'y=conn.get(r"value_of(\axuv001)")')

plt.plot(t, y)
plt.show()


# myTree = Tree(strTreeName, currentShot)
# n1 = myTree.getNode('Ip')
#
# result = conn.get("(Ip:DATA * $1)*$2" , Int32(2), Int32(10))
# result = conn.get("(Ip:DATA * $1)*$2" , Int32(2), Int32(10))
#print result

# closeTree(strTreeName, currentShot)

#
# import sys
# from MDSplus import *
#
#
# def traverseTree(rootNode, tabs):
#     rootName = rootNode.getNodeName()
#     for i in range(0, tabs):
#         print
#         "\t",
#     print
#     rootName
#     try:
#         children = rootNode.getChildren()
#         for c in children:
#             traverseTree(c, tabs + 1)
#     except:
#         pass
#     try:
#         members = rootNode.getMembers()
#         for m in members:
#             traverseTree(m, tabs + 1)
#     except:
#         pass
#
#
# if (len(sys.argv) < 2 or len(sys.argv) > 3):
#     print
#     "Usage: dump_tree <experiment> [shot]"
#     sys.exit(0)
# experiment = sys.argv[1]
# shot = -1
# if (len(sys.argv) > 2):
#     shot = int(sys.argv[2])
# try:
#     tree = Tree(experiment, shot)
# except:
#     print
#     "Cannot open tree " + experiment + " shot " + shot
#     sys.exit(0);
#
# topNode = tree.getNode("\\TOP")
# traverseTree(topNode, 0);
"""