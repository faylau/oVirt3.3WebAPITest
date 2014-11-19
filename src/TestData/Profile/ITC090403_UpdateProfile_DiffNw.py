#encoding:utf-8

__authors__ = ['"Wei Keke" <keke.wei@cs2c.com.cn>']
__version__ = "V0.1"

'''
# ChangeLog:
#---------------------------------------------------------------------------------
# Version        Date                Desc                            Author
#---------------------------------------------------------------------------------
# V0.1           2014/10/09          初始版本                                                            Wei Keke 
#---------------------------------------------------------------------------------
'''

from TestAPIs.DataCenterAPIs import DataCenterAPIs
from TestData.Profile import ITC09_SetUp as ModuleData

'''
@note: PreData
'''
nw_name = 'network_ITC09'
dc_name = ModuleData.dc_name
dc_id = DataCenterAPIs().getDataCenterIdByName(dc_name)
profile_name = 'profile_ITC09'
nw_info = '''
<network>
    <name>%s</name>
    <data_center id= "%s"/>    
</network>
''' %(nw_name,dc_id)

# 字符串中的network id是通过外部调用的函数传递的，不在字符串中传递。
profile_info = '''
    <vnic_profile>
        <name>profile_ITC09</name>
        <description>shelled</description>
        <network id="%s"/>
        <port_mirroring>false</port_mirroring>
    </vnic_profile>
'''

'''
@note: TestData
'''
update_info = '''
    <vnic_profile>
        <description>shelled</description>
        <network id=""/>
        <port_mirroring>true</port_mirroring>
    </vnic_profile>
'''

'''
@note: ExpectedData
'''
expected_status_code = 400
expected_info = '''
<fault>
    <reason>Operation Failed</reason>
    <detail>[Cannot edit VM network interface profile. VM network interface profile's network cannot be changed.]</detail>
</fault>
'''

