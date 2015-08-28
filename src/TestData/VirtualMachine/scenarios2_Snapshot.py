#encoding:utf-8
import TestData.VirtualMachine.ITC05_SetUp as ModuleData
from TestAPIs.VirtualMachineAPIs import VmSnapshotAPIs
from TestData.VirtualMachine.scenarios1_Snapshot import description

'''
@note: PreData
'''
'''
@note: 创建虚拟机的离线快照
'''

vmsnapshotapi = VmSnapshotAPIs()
snapshot_id = vmsnapshotapi.getVmSnapshotIDBydisp(ModuleData.snapshot_name, description)
cloneVmname='cloneVM'

xml_clone_vm_option= '''
<vm>
    <name>%s</name>
    <cluster>
        <name>%s</name>
    </cluster>
    <snapshots>
    <snapshot id='%s'/>
    </snapshots>
</vm>
''' %(cloneVmname,ModuleData.cluster_nfs_name,snapshot_id)
'''
@note: ExpectedData
'''
expected_status_code_create_vm = 202
expected_status_code_restore_vm = 200