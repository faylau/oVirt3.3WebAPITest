#encoding:utf-8

from Configs.GlobalConfig import Hosts
from TestData.Host import ITC03_SetUp as ModuleData
from TestAPIs.ClusterAPIs import ClusterAPIs

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
''' % (cluster_id, host_name, Hosts['node4']['ip'], Hosts['node4']['password'])

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