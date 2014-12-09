#encoding=utf-8

__authors__ = ['"Liu Fei" <fei.liu@cs2c.com.cn>']
__version__ = "V0.2"

'''
# ChangeLog:
#---------------------------------------------------------------------------------
# Version        Date                Desc                            Author
#---------------------------------------------------------------------------------
# V0.1           2014/06/20          初始版本                                                            Liu Fei
#---------------------------------------------------------------------------------
# V0.2           2014/12/09          *加入了ContextFilter日志过滤条件       Liu Fei
#---------------------------------------------------------------------------------
'''

import logging


class LogPrint():
    '''
    @summary: 日志打印及管理类
    '''
    def __init__(self, log_file="log.txt", log_level=logging.INFO):
        '''
        @summary: 初始化函数
        '''
        self.logger = logging.Logger('itest')
        self.logger.setLevel(log_level)
        hdr = logging.StreamHandler()
        self.logger.addHandler(hdr)
        formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s| %(filename)-10s[line:%(lineno)-.4d] | %(message)s',
                                      datefmt='%Y-%m-%d %H:%M:%S')
        hdr.setFormatter(formatter)
        
        
        # 为logging日志输出添加Filter
#         logging.getLogger().addFilter(ContextFilter())

#         logging.basicConfig(level=log_level,
#                             format='%(asctime)s %(levelname)-8s| %(filename)-15s[line:%(lineno)-.4d] | %(message)s',
#                             datefmt='%Y-%m-%d %H:%M:%S',
# #                             filename=log_file,
#                             filemode="a"
#                             )
#         requests_log = logging.getLogger("requests.packages.urllib3")
#         requests_log.setLevel(logging.WARN)
#         requests_log.propagate = True
    
#     def set_log_level(self, log_level):
#         '''
#         @summary: 设置日志级别
#         @param log_level: 日志级别，取值包含DEBUG、INFO、ERROR、WARNING、CRITICAL
#         '''
#         self.log_level = log_level
    
    def debug(self, msg):
        self.logger.debug(msg)
    
    def info(self, msg):
        self.logger.info(msg)
    
    def error(self, msg):
        self.logger.error(msg)
    
    def warning(self, msg):
        self.logger.warn(msg)
    
    def critical(self, msg):
        self.logger.critical(msg)
        
if __name__=='__main__':
    LogPrint().debug("This is a debug message.")
    LogPrint().info("This is a info message.")
    LogPrint().info("Starting new HTTPS connection")
    LogPrint().error("This is a error message.")
    LogPrint().warning("This is a warning message.")
    LogPrint().critical("This is a critical message.")