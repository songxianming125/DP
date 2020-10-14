from MDSplus import Tree, mdsExceptions


class mdsTree:
    """ 构建MDSplus.Tree的一些常用方法 """
    def __init__(self, dbname, shot):
        self.shot = shot
        self.dbname = dbname
        self.tree = Tree(self.dbname, self.shot)


    def formChannelPool(self):
        """ 构建一个通道池, 对外显示的通道均有与通道名称相同的tags  """
        node_list = self.tree.getNodeWild("***")
        channels = []
        for node in node_list:
            if node.usage == 'SIGNAL' and len(node.tags) == 1 and str(node.tags[0]) == node.name:
                channels.append(node.name.strip())
        return channels


    def close(self):
        self.tree.close()


    def getCurrentShot(self):
        """ 获取当前炮号 """
        try:
            shot_num = self.tree.getCurrent()
            new_tree = Tree(self.dbname, shot_num)
            shot_num = shot_num if new_tree.getNode('FBC:DUPS1').getLength() else shot_num-1
        except mdsExceptions.TreeNNF:
            # MDSplus.mdsExceptions.TreeNNF: %TREE-W-NNF, Node Not Found
            shot_num = shot_num if new_tree.getNode('FBC:IP').getLength() else shot_num-1
        except mdsExceptions.TreeNOCURRENT:
            # MDSplus.mdsExceptions.TreeNOCURRENT: %TREE-E-NOCURRENT, No current shot number set for this tree.
            shot_num = None
        return shot_num


    def renameChaName(self, channel_name):
        """ 通道名加r'\'是通道的tags, 不在使用'子树:通道名'方式进行索引"""
        return '\\' + channel_name.upper()


    def isHaveData(self, channel_name):
        """ 返回储存内容长度, 当里面不是数据是公式的时候也有长度(此时如果公式索引的通道没数据同样没有数据) """
        # length = self.tree.getNode(self.renameChaName(channel_name)).getCompressedLength()
        length = self.tree.getNode(self.renameChaName(channel_name)).getLength()
        return length


    def getWrittenTime(self, channel_name):
        """ 获得数据写入时间 """
        return self.tree.getNode(self.renameChaName(channel_name)).getTimeInserted().date


    def setTimeContext(self, begin, end, delta):
        """ 设置起止时间及采样率，参数单位s """
        self.tree.setTimeContext(begin, end, delta)


    def getData(self, channel_name, begin=None, end=None, delta=None):
        """ 
        返回x,y数据，如果没有数据，或出错，返回两个空列表
        """
        self.setTimeContext(begin, end, delta)
        channel_name = self.renameChaName(channel_name)
        try:
            data_x = self.tree.getNode(channel_name).dim_of().data()
            data_y = self.tree.getNode(channel_name).data()
        except mdsExceptions.TreeNODATA:
            # MDSplus.mdsExceptions.TreeNODATA: %TREE-E-NODATA, No data available for this node
            data_x = []
            data_y = []
        except mdsExceptions.TreeNNF:
            # MDSplus.mdsExceptions.TreeNNF: %TREE-W-NNF, Node Not Found
            data_x = []
            data_y = []
        except Exception as e:
            print('Check {} find that {}'.format(channel_name, str(e)))
            data_x = []
            data_y = []

        return data_x, data_y


    def getYInfo(self, channel_name):
        """ 
        获得通道数据Y轴单位
        """
        try:
            unit = self.tree.getNode(self.renameChaName(channel_name)).units_of()
            unit = '-' if unit == ' ' else unit
        except Exception as e:
            print('get {} unit find that {}'.format(channel_name, str(e)))
            unit = '-'
        return {"unit":unit}


def currentShot(dbname):
    """ 获取当前炮，与mdsTree类分开原因：调用的时候不用先实例化一个tree了 """
    try:
        shot_num = Tree.getCurrent(dbname)
        new_tree = Tree(dbname, shot_num)
        shot_num = shot_num if new_tree.getNode('FBC:DUPS1').getLength() else shot_num-1
        new_tree.close()
    except mdsExceptions.TreeNNF:
        # MDSplus.mdsExceptions.TreeNNF: %TREE-W-NNF, Node Not Found
        shot_num = shot_num if new_tree.getNode('FBC:IP').getLength() else shot_num-1
        new_tree.close()
    except mdsExceptions.TreeNOCURRENT:
        # MDSplus.mdsExceptions.TreeNOCURRENT: %TREE-E-NOCURRENT, No current shot number set for this tree.
        # 本地测试的时候用的exl50_copy数据库获取不到当前炮，里面只有4983炮数据
        shot_num = 4983
    return shot_num


