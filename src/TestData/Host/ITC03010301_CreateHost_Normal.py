#encoding:utf-8

__authors__ = ['"Liu Fei" <fei.liu@cs2c.com.cn>']
__version__ = "V0.1"

'''
# ChangeLog:
#---------------------------------------------------------------------------------
# Version        Date                Desc                            Author
#---------------------------------------------------------------------------------
# V0.1           2014/10/17          初始版本                                                            Liu Fei 
#---------------------------------------------------------------------------------
'''

from Configs.GlobalConfig import Hosts
from TestData.Host import ITC03_SetUp as ModuleData
from TestAPIs.ClusterAPIs import ClusterAPIs


host = Hosts['node1']
'''
@note: Pre-TestData
'''

'''
@note: Test-Data
'''
host_name = 'node-ITC03010301'
cluster_id = ClusterAPIs().getClusterIdByName(ModuleData.cluster_name)
xml_host_info = '''
<host>
    <cluster id="%s"/>
    <name>%s</name>
    <address>%s</address>
    <root_password>%s</root_password>
</host>
''' % (cluster_id, host_name, host['ip'], host['password'])

'''
@note: Post-TestData
'''
xml_del_option = '''
<action>
    <force>true</force>
    <async>false</async>
</action>
'''

'''
@note: ExpectedResult
'''
status_code = 201