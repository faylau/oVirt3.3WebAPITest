#coding:utf-8

__authors__ = ['"Liu Fei" <fei.liu@cs2c.com.cn>']
__version__ = "V0.1"

'''
# ChangeLog:
#---------------------------------------------------------------------------------
# Version        Date                Desc                            Author
#---------------------------------------------------------------------------------
# V0.1           2014/11/02          初始版本                                                            Liu Fei 
#---------------------------------------------------------------------------------
'''

from TestData.VirtualMachine import ITC05_SetUp as ModuleData
from TestAPIs.ClusterAPIs import ClusterAPIs
from TestAPIs.TemplatesAPIs import TemplatesAPIs

'''
---------------------------------------------------------------------------------------------------
@note: Pre-Test-Data
---------------------------------------------------------------------------------------------------
'''



'''
---------------------------------------------------------------------------------------------------
@note: Test-Data
---------------------------------------------------------------------------------------------------
'''
vm_name = 'vm-ITC05010301'
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
    <os type="NKAS6x64">
        <boot dev="hd"/>
    </os>
    <high_availability>
        <enabled>true</enabled>
        <priority>50</priority>
    </high_availability>
    <display>
        <type>vnc</type>
        <monitors>1</monitors>
        <smartcard_enabled>true</smartcard_enabled>
    </display>
    <stateless>false</stateless>
    <placement_policy>
        <affinity>migratable</affinity>
    </placement_policy>
    <memory_policy>
        <guaranteed>536870912</guaranteed>
    </memory_policy>
    <usb>
        <enabled>false</enabled>
    </usb>
</vm>
''' % (vm_name, cluster_id, template_id)

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
expected_status_code_create_vm = 201
expected_status_code_get_vm_info = 200
expected_status_code_del_vm = 200

