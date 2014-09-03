#coding=utf-8

import logging

class LogPrint():
    def __init__(self, log_file="log.txt", log_level=logging.DEBUG):
        logging.basicConfig(level=log_level,
                            format='%(asctime)s %(levelname)s\t| %(filename)s[line:%(lineno)d]\t| %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            filename=log_file,
                            filemode="a")
    
    def set_log_level(self):
        pass
    
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