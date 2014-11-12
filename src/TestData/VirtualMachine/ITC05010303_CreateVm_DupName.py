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
vm_name = "vm-ITC05010303"

xml_vm_info='''
<vm>
    <name>%s</name>
    <description>Test for ITC05010303</description>
    <type>server</type>
    <memory>536870912</memory>
    <cluster>
        <name>%s</name>
    </cluster>
    <template>
        <name>Blank</name>
    </template>
    <cpu>
        <topology sockets="1" cores="1"/>
    </cpu>
</vm>
''' % (vm_name, ModuleData.cluster_nfs_name)


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
expected_status_code_create_vm_dup = 400
expected_info_create_vm_dup = '''
<fault>
    <reason>Operation Failed</reason>
    <detail>[Cannot add VM. The VM name is already in use, please choose a unique name and try again.]</detail>
</fault>
'''

