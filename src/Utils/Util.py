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

from datetime import datetime, timedelta
import time

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



if __name__=='__main__':
    print wait_until(False, 10)
            