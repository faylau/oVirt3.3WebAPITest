#encoding:utf-8

__authors__ = ['"Liu Fei" <fei.liu@cs2c.com.cn>']
__version__ = "V0.1"

'''
# ChangeLog:
#---------------------------------------------------------------------------------
# Version        Date            Desc                            Author
#---------------------------------------------------------------------------------
# V0.1           2014/09/03      初始版本                                                            Liu Fei 
#---------------------------------------------------------------------------------
'''

import time

def wait_until(condition, duration_time, interval_time):
    '''
    @summary: 智能判断某个条件是否符合要求
    @param duration_time: 持续检查的时间（秒）
    @param interval_time: 每次检查的间隔时间（秒）
    @return: True or False
    '''
    start_time = 0
    if interval_time > duration_time:
        raise Exception("The duration time shoud greater than interval time.")
    else:
        