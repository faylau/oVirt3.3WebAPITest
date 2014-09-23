#encoding:utf-8

'''-----------------------------------------------------------------------------------------
@summary: 主机名称、IP、root密码等信息
'''
Hosts = {'engine' : {'ip':'10.1.167.2', 'password':'qwer1234'},
         'node1' : {'ip':'10.1.167.1', 'password':'qwer1234'},
         'node3' : {'ip':'10.1.167.3', 'password':'qwer1234'},
         'node4' : {'ip':'10.1.167.4', 'password':'qwer1234', 
                    'IMM':{'ip':'10.1.167.14', 'user':'USERID', 'password':'userid', 'type':'ipmi'}}
         }

'''-----------------------------------------------------------------------------------------
@summary: Data存储域名称、地址等信息，包括NFS、ISCSI和FC三类
'''
DataStorages = {'nfs' : {
                            'data1' : '10.1.167.2:/storage/data1',
                            'data2' : '10.1.167.2:/storage/data2'
                        },
                'iscsi' : {
                            'data1-iscsi' : {
                                                'ip':'10.1.161.61',
                                                'port':'3260',
                                                'target':'xxxx',
                                                'lun_id':'xxxx'
                                            }
                           }
                }
'''-----------------------------------------------------------------------------------------
@summary: ISO存储域名称及地址
'''
IsoStorages = {'ISO-Storage1':'10.1.167.2:/storage/iso1',
               'ISO-Storage2':'10.1.167.2:/storage/iso2'
               }

'''-----------------------------------------------------------------------------------------
@summary: Export存储域名称及地址
'''
ExportStorages = {'Export-Storage1':'10.1.167.2:/storage/export1',
                  'Export-Storage2':'10.1.167.2:/storage/export2'
                  }

'''-----------------------------------------------------------------------------------------
@summary: Web管理平台、Http接口相关信息
'''
WebAdmin = {'user':'admin', 'domain':'internal', 'password':'qwer1234'}
WebBaseApiUrl = 'https://%s/api' % Hosts['engine']['ip']
headers = {'content-type':'application/xml'}


