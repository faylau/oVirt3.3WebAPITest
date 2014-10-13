#encoding:utf-8

from Configs.GlobalConfig import Hosts
from TestData.Host import ITC03_SetUp as ModuleData
from TestAPIs.ClusterAPIs import ClusterAPIs

'''
@note: Pre-TestData
'''
host_name = 'node-ITC030102'
xml_host_info = '''
<host>
    <cluster id="%s"/>
    <name>%s</name>
    <address>%s</address>
    <root_password>%s</root_password>
</host>
''' % (ClusterAPIs().getClusterIdByName(ModuleData.cluster_name), host_name, Hosts['node4']['ip'], Hosts['node4']['password'])

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
status_code = 200