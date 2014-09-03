#encoding:utf-8

__authors__ = ['"Liu Fei" <fei.liu@cs2c.com.cn>']
__version__ = "V0.1"

'''
# ChangeLog:
#---------------------------------------------------------------------------------
# Version        Date                Desc                            Author
#---------------------------------------------------------------------------------
# V0.1           2014/08/28          初始版本                                                            Liu Fei 
#---------------------------------------------------------------------------------
'''

import requests

from Configs import GlobalConfig

class HttpClient(object):
    '''
    @summary: 通过requests来封装一个HttpClient，专门用于调用HTTP接口并发送各种类型请求
    '''
    auth = ('%s@%s' % (GlobalConfig.WebAdmin['user'], GlobalConfig.WebAdmin['domain']), GlobalConfig.WebAdmin['password'])
    headers = GlobalConfig.headers
    
    def __init__(self):
        '''
        Constructor
        '''
        pass
    
    @classmethod
    def sendRequest(self, method, api_url, auth=auth, verify=False, headers=headers, data=None):
        '''
        @summary: 类方法，主要通过调用requests包来对指定接口发送GET/PUT/POST/DELETE等请求
        @param method: HTTP请求类型，目前包括GET/PUT/POST/DELETE等4种
        @param api_url: 要访问的接口地址
        @param: auth: HTTP认证信息，缺省从GlobalConfig中读取WebAdmin信息，如('admin@internal'，'qwer1234'）
        @param verify: 是否需要认证证书文件，requests缺省为True，此处根据需要将其缺省值设定为False
        @param headers: HTTP请求头信息，这里主要指定请求数据的传输格式，如{'content-type':'application/xml'}
        @param data: 请求中需要传输的数据（这里主要是XML格式的文件或字符串），缺省为None
        @return: 一个从服务器端获得的请求响应（response）
        '''
        if method.upper() == "GET":
            return requests.get(url=api_url, auth=self.auth, verify=verify)
        elif method.upper() == "POST":
            return requests.post(url=api_url, auth=self.auth, verify=verify, headers=self.headers, data=data)
        elif method.upper() == "PUT":
            return requests.put(url=api_url, auth=self.auth, verify=verify, headers=self.headers, data=data)
        elif method.upper() == "DELETE":
            if not data:
                return requests.delete(url=api_url, auth=self.auth, verify=verify)
            else:
                return requests.delete(url=api_url, auth=self.auth, verify=verify, headers=self.headers, data=data)
        else:
            raise Exception("The request method should in 'GET/POST/PUT/DELETE'.")


if __name__ == "__main__":
#     pass
    dc_id = '66f3a0b3-33fd-4979-bbcb-c2a175f3cb51'
    api_url = '%s/datacenters/%s' % (GlobalConfig.WebBaseApiUrl, dc_id)
    method = 'DELETE'
    r = HttpClient.sendRequest(method=method, api_url=api_url)
    print r.status_code, r.text