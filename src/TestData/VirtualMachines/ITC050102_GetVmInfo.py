#coding:utf-8

__authors__ = ['"Liu Fei" <fei.liu@cs2c.com.cn>']
__version__ = "V0.1"

'''
# ChangeLog:
#---------------------------------------------------------------------------------
# Version        Date                Desc                            Author
#---------------------------------------------------------------------------------
# V0.1           2014/10/31          初始版本                                                            Liu Fei 
#---------------------------------------------------------------------------------
'''

import xmltodict

from TestData.VirtualMachines import ITC05_SetUp as ModuleData
from TestAPIs.ClusterAPIs import ClusterAPIs
from TestAPIs.TemplatesAPIs import TemplatesAPIs

'''
---------------------------------------------------------------------------------------------------
@note: Pre-Test-Data
---------------------------------------------------------------------------------------------------
'''
vm_name = 'vm-ITC050102'
cluster_id = ClusterAPIs().getClusterIdByName(ModuleData.cluster_nfs_name)
template_id = TemplatesAPIs().getTemplateIdByName('Blank')

xml_vm_info='''
    <vm>
        <name>%s</name>
        <description>Test for ITC050102</description>
        <type>server</type>
        <memory>536870912</memory>
        <cluster id="%s"/>
        <template id="%s"/>
        <cpu>
            <topology sockets="1" cores="1"/>
        </cpu>
    </vm>
''' % (vm_name, cluster_id, template_id)


'''
---------------------------------------------------------------------------------------------------
@note: Test-Data
---------------------------------------------------------------------------------------------------
'''


'''
---------------------------------------------------------------------------------------------------
@note: Post-Test-Data
---------------------------------------------------------------------------------------------------
'''




'''
---------------------------------------------------------------------------------------------------
@note: ExpectedResult
---------------------------------------------------------------------------------------------------
'''
expected_status_code_get_vm_info = 200
expected_status_code_del_vm = 200

