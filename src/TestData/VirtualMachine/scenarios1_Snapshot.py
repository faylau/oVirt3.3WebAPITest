#encoding:utf-8
import TestData.VirtualMachine.ITC05_SetUp as ModuleData
from TestAPIs.VirtualMachineAPIs import VmSnapshotAPIs

'''
@note: PreData
'''
'''
@note: 创建离线快照，虚拟机为初始化环境中vm_scenarios
'''

description ='offlinesnapshot'

snapshot_info='''
<snapshot>
    <description>%s</description>
    <persist_memorystate>false</persist_memorystate>
    </snapshot>
''' %description


'''
@note: ExpectedData
'''
expected_status_code = 202


