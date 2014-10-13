#encoding:utf-8

from Configs.GlobalConfig import Hosts
import ITC03_SetUp as ModuleData

'''
@note: Pre-TestData
'''
host_name = 'node-ITC03010503'
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
xml_del_host_option = '''
<action>
    <force>true</force>
    <async>false</async>
</action>
'''

'''
@note: Post-TestData
'''


'''
@note: ExpectedResult
'''
expected_status_code_create_host = 201
expected_status_code_del_host_up = 409
expected_info_del_host_up = '''
<fault>
    <reason>Operation Failed</reason>
    <detail>[Cannot remove Host. Host is operational. Please switch Host to Maintenance mode first.]</detail>
</fault>
'''
expected_status_code_deactive_host = 200
expected_status_code_del_host = 200