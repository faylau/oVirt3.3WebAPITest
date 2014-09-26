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

# V0.3           2014/09/25     存在问题，修改了getItemsList成员函数，      Liu Fei
#                               解决了dict中存在list的问题，以及特殊类型
#                               dict的问题（全部key均包含#或@字符）。
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
        self.count = 2
        
    def existNormalKey(self, d):
        '''
        @summary: 判断某个dict是普通还是特殊类型（便于在getItemsList中进行特殊操作）
        @note: （1）特殊类型：dict的所有key均包含 @ 或 # 字符；（2）普通类型：dict中存在不含@或#字符的key。
        @param d: 一个字典
        @return: （1）True：普通字典；（2）False：特殊字典。
        '''
        for key in d:
            if '@' in key:
                pass
            elif '#' in key:
                pass
            else:
                return True
        return False
    
    def getItemsList(self, item):
        '''
        @summary: 获取Dict中全部叶子节点的信息，包括keys和value（对应init函数中的items_path_list）
        @param item: 待解析的dict中的item，此item的value有可能是dict、list或unicode（叶子节点）
        @return: 往成员变量self.items_path_list中写入每个叶子节点的key路径以及value
        '''
        # 临时变量，用于存储被pop出来的节点，便于后续再进行append操作。
        self.temp = None
        
        # 如果当前item是字典
        if isinstance(item, dict):
            # 判断字典类型，并设置标志位
            self.flag = self.existNormalKey(item)
            # 遍历字典，将key依次存放于keys_list列表中，并对dict[key]元素进行递归
            for k in item:
                self.keys_list.append(k)
                self.getItemsList(item[k])
            # 当flag标志位为False（dict为特殊类型）且keys_list不为空（说明递归可以继续）时，将keys_list最后元素出栈，并保存。
            if not self.flag and self.keys_list:
                self.temp = self.keys_list.pop()
            elif self.flag and self.keys_list:
                self.keys_list.pop()
        
        # 如果当前item是list，进行遍历，并且对list中的元素进行递归，将上面出栈的元素重新进栈。
        elif isinstance(item, list):
            for i in item:
                self.getItemsList(i)
                self.keys_list.append(self.temp)
            # 遍历结束后，若flag为False，表明list中的dict是特殊类型，需要进行一次pop操作。
            if not self.flag:
                self.keys_list.pop()
        
        # 如果当前item为叶子节点的value，将该值保存到keys_list中，形成一个叶子节点的完整路径。
        else:
            self.keys_list.append(item)
            self.items_path_list.append(deepcopy(self.keys_list))
#             print self.keys_list
            self.keys_list.pop()
            self.keys_list.pop()
                
    def isSubsetDict(self, dict1, dict2):
        '''
        @summary: 判断dict1是否为dict2的子集（相应的叶子元素值相等）。
        @param dict1: 第一个OrderedDict；
        @param dict2: 第二个OrderedDict；
        @return: True or False
        '''
        self.getItemsList(dict1)
        items_path_list_1 = self.items_path_list
#         print items_path_list_1
        self.__init__()
        self.getItemsList(dict2)
        items_path_list_2 = self.items_path_list
#         print items_path_list_2
        # 对dict1中的元素进行遍历，并判断其是否存在于dict2中
        for i in items_path_list_1:
            if i in items_path_list_2:
                continue
            else:
                print i
                return False
        return True

if __name__=='__main__':
#     print wait_until(False, 10)
    xml1 = '''
    <host id="001">
        <name>host1</name>
        <link href="bbb"></link>
        <link href="aaa"></link>
    </host>
    '''
    xml2 = '''
    <host id="001">
        <link href="aaa"></link>
        <link href="bbb"></link>
        <name>host1</name>
        <desc>host111</desc>
    </host>
    '''
    
    import xmltodict
    dict1 = xmltodict.parse(xml1)
    dict2 = xmltodict.parse(xml2)
        
    dc = DictCompare()
    dc.getItemsList(dict2)
#     print dc.items_path_list
    print dc.isSubsetDict(dict1, dict2)
            