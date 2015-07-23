#encoding:utf-8

'''-----------------------------------------------------------------------------------------
@summary: 主机名称、IP、root密码等信息
'''
Hosts = {'engine' : {'ip':'10.1.164.104', 'password':'qwer1234'},
         'node1' : {'ip':'10.1.85.241', 'password':'qwer1234', 'nic':['eth0', 'eth1', 'eth2', 'eth3']},
         'node2' : {'ip':'10.1.85.205', 'password':'qwer1234'},
         'node3' : {'ip':'10.1.85.191', 'password':'qwer1234', 
                    'IMM':{'ip':'10.1.167.14', 'user':'USERID', 'password':'userid', 'type':'ipmilan'}}
         }

'''-----------------------------------------------------------------------------------------
@summary: Data存储域名称、地址等信息，包括NFS、ISCSI和FC三类
'''
DataStorages = {'nfs' : {
                            'data1' : {'ip':'10.1.164.104', 'path':'/storage/data1'},
                            'data2' : {'ip':'10.1.164.104', 'path':'/storage/data2'},
                            'data3' : {'ip':'10.1.164.104', 'path':'/storage/data3'}
                        },
                'iscsi' : {
                            'serial' : 'SLENOVO_LIFELINE-DISK', 
                            'vendor_id' : 'LENOVO', 
                            'product_id' : 'LIFELINE-DISK', 
                            'data1-iscsi' : {
                                                'ip':'10.1.161.61',
                                                'port':'3260',
                                                'target':'iqn.2012-07.com.lenovoemc:ix12.px12-TI3111.liufei',
                                                'lun_id':'35005907f935f9b7f'
                                            },
                            'data2-iscsi' : {
                                                'ip':'10.1.161.61',
                                                'port':'3260',
                                                'target':'iqn.2012-07.com.lenovoemc:ix12.px12-TI3111.mari',
                                                'lun_id':'35005907f72e55e1b'
                                            }
                           }
                }
'''-----------------------------------------------------------------------------------------
@summary: ISO存储域名称及地址
'''
IsoStorages = {'ISO-Storage1' : {'ip':'10.1.164.104', 'path':'/storage/iso1'},
               'ISO-Storage2' : {'ip':'10.1.164.104', 'path':'/storage/iso2'}
               }

'''-----------------------------------------------------------------------------------------
@summary: Export存储域名称及地址
'''
ExportStorages = {'Export-Storage1' : {'ip':'10.1.164.104', 'path':'/storage/export1'},
                  'Export-Storage2' : {'ip':'10.1.164.104', 'path':'/storage/export2'}, 
                  'Export-Storage3' : {'ip':'10.1.164.104', 'path':'/storage/export3'}
                  }

'''-----------------------------------------------------------------------------------------
@summary: Web管理平台、Http接口相关信息
'''
WebAdmin = {'user':'admin', 'domain':'internal', 'password':'qwer1234'}
WebBaseApiUrl = 'https://%s/api' % Hosts['engine']['ip']
headers = {'content-type':'application/xml'}


