#encoding:utf-8

__authors__ = ['"Liu Fei" <fei.liu@cs2c.com.cn>']
__version__ = "V0.1"

'''
# ChangeLog:
#---------------------------------------------------------------------------------
# Version        Date            Desc                                Author
#---------------------------------------------------------------------------------
# V0.1           2014/09/03     初始版本                                                                      Liu Fei 
# V0.2           2014/09/24     增加了DictCompare类（getItemsList     Liu Fei
#                               和isSubsetDict两个成员函数），主要     
#                               用于判定dict1是否为dict2的子集。
#---------------------------------------------------------------------------------
'''

from datetime import datetime, timedelta
import time
from copy import deepcopy


def wait_until(condition, duration_time, interval_time=2):
    '''
    @summary: 在指定时间内判断某个条件是否符合要求
    @param duration_time: 持续检查的时间（秒）
    @param interval_time: 每次检查的间隔时间（单位：秒，缺省值为2）
    @return: True or False
    '''
    # 判断持续时间是否大于间隔时间
    if interval_time > duration_time:
        raise Exception("The duration time should greater than interval time.")
    end_time = datetime.now() + timedelta(seconds=duration_time)
    while (datetime.now() < end_time):
        if condition:
            return condition
        else:
            time.sleep(interval_time)
    return condition

class DictCompare(object):
    '''
    @summary: 比较两个Dictionary之间的关系（待扩展）
    '''
    def __init__(self):
        '''
        @summary: 初始化构造函数：
        (1) items_path_list: 用于存储一个dict中全部叶子节点的keys和values（也就是keys_list的集合）
        (2) keys_list: 用于存储dict中叶子节点的keys和values，如['hosts', 'host', 0, '@id', '001']
        '''
        self.items_path_list = []
        self.keys_list = []
    
    def getItemsList(self, item):
        '''
        @summary: 获取Dict中全部叶子节点的信息，包括keys和value（对应init函数中的items_path_list）
        @param item: 进行解析的dict中的item，此item的value有可能是dict、list或unicode（叶子节点）
        @return: 往成员变量self.items_path_list中写入每个叶子节点的key路径以及value
        '''
        # 对item中的元素进行遍历（该item的值有可能是dict，也有可能是list，也有可能是叶子节点）
        for i in item:
            # 如果该item的vlaue是一个dict，则记录下当前的key，然后递归调用此函数
            if isinstance(item[i], dict):
                self.keys_list.append(i)
                self.getItemsList(item[i])
            # 如果该item的value是一个list，则记录下当前的key以及每个list元素的下标，然后递归调用此函数
            elif isinstance(item[i], list):
                self.keys_list.append(i)
                list_len = len(item[i])
                for n in range(list_len):
#                     self.keys_list.append(n)
                    self.getItemsList(item[i][n])
#                     self.keys_list.pop()    # 若list中存在多个同级元素，保存其下标后，需要将下标pop，以便保存下一个同级元素的下标
            # 如果该元素是叶子节点，则保存当前的key
            else:
                self.keys_list.append(i)
                self.keys_list.append(item[i])
                self.items_path_list.append(deepcopy(self.keys_list))
                self.keys_list.pop()
                self.keys_list.pop()
                
    def isSubsetDict(self, dict1, dict2):
        '''
        @summary: 判断dict1是否为dict2的子集（且相应的叶子元素值相等）。
        @param dict1: 第一个OrderedDict类型的dict；
        @param dict2: 第二个OrderedDict类型的dict；
        @return: True or False
        @bug: 当存在list时，里面的多个同级元素是按XML中出现的顺序标识的（如第一个host是0，第二个host是），
                                如果dict2中host顺序与此不符，则对比会失败。针对该问题，后续有需要再进行改进。
        '''
        self.getItemsList(dict1)
        items_path_list_1 = self.items_path_list
        self.__init__()
        self.getItemsList(dict2)
        items_path_list_2 = self.items_path_list
        # 对dict1中的元素进行遍历，并判断其是否存在于dict2中
        for i in items_path_list_1:
            if i in items_path_list_2:
                continue
            else:
                return False
        return True

if __name__=='__main__':
#     print wait_until(False, 10)
    xml1 = '''
    <hosts>

        <host id="002">
            <name>host2</name>
        </host>
        <host id="001">
            <name>host1</name>
        </host>
    </hosts>
    '''
    xml2 = '''
    <hosts>
        <host id="001">
            <name>host1</name>
            <desc>host111</desc>
        </host>
        <host id="002">
            <name>host2</name>
            <desc>host222</desc>
        </host>
        <host id="003">
            <name>host3</name>
            <desc>host333</desc>
        </host>
        <type>aaaaaaaaaa</type>
    </hosts>
    '''
    
    import xmltodict
    dict1 = xmltodict.parse(xml1)
    dict2 = xmltodict.parse(xml2)
    
    dc = DictCompare()
    print dc.isSubsetDict(dict1, dict2)
            