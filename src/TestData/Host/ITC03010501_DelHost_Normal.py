#encoding:utf-8

from Configs.GlobalConfig import Hosts
import ITC03_SetUp as ModuleData

'''
@note: Pre-TestData
'''
host_name = 'node-ITC03010501'
xml_host_info = '''
<host>
    <cluster>
        <name>%s</name>
    </cluster>
    <name>%s</name>
    <address>%s</address>
    <root_password>%s</root_password>
</host>
''' % (ModuleData.cluster_name, host_name, Hosts['node4']['ip'], Hosts['node4']['password'])

'''
@note: Test-Data
'''


'''
@note: Post-TestData
'''


'''
@note: ExpectedResult
'''
expected_status_code_create_host = 201
expected_status_code_del_host_normal = 200