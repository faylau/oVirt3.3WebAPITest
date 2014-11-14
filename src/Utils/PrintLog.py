#encoding=utf-8

__authors__ = ['"Liu Fei" <fei.liu@cs2c.com.cn>']
__version__ = "V0.1"

'''
# ChangeLog:
#---------------------------------------------------------------------------------
# Version        Date                Desc                            Author
#---------------------------------------------------------------------------------
# V0.1           2014/06/20          初始版本                                                            Liu Fei 
#---------------------------------------------------------------------------------
'''

import os
import logging

class LogPrint():
    '''
    @summary: 日志打印及管理类
    '''
#     src_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
#     log_file_path = src_dir + os.path.sep + 'Results'
    
    def __init__(self, log_file="log.txt", log_level=logging.INFO):
        pass
        logging.basicConfig(level=log_level,
                            format='%(asctime)s %(levelname)s\t| %(filename)s[line:%(lineno)d]\t| %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
#                             filename=log_file,
                            filemode="a")
    
    def set_log_level(self, log_level):
        '''
        @summary: 设置日志级别
        @param log_level: 日志级别，取值包含DEBUG、INFO、ERROR、WARNING、CRITICAL
        '''
        self.log_level = log_level
    
    def debug(self, msg):
        logging.debug(msg)
    
    def info(self, msg):
        logging.info(msg)
    
    def error(self, msg):
        logging.error(msg)
    
    def warning(self, msg):
        logging.warning(msg)
    
    def critical(self, msg):
        logging.critical(msg)
        
if __name__=='__main__':
    LogPrint().debug("This is a debug message.")
    LogPrint().info("This is a info message.")
    LogPrint().error("This is a error message.")
    LogPrint().warning("This is a warning message.")
    LogPrint().critical("This is a critical message.")