#encoding:utf-8
from TestAPIs.VirtualMachineAPIs import VirtualMachineAPIs, VmDiskAPIs,VmSnapshotAPIs
import TestData.VirtualMachine.ITC05_SetUp as ModuleData



'''
---------------------------------------------------------------------------------------------------
@note: Test-Data
---------------------------------------------------------------------------------------------------
'''
xml_start_vm_once = '''
<action>
    <vm>
        <display>
            <type>spice</type>
        </display>
        <os>
            <boot dev="hd"/>
        </os>
    </vm>
</action>
'''

'''
---------------------------------------------------------------------------------------------------
@note: Test-Data
---------------------------------------------------------------------------------------------------
'''
vmapi=VirtualMachineAPIs()
vmdiskapi=VmDiskAPIs()  

snapshot_vm_id = vmapi.getVmIdByName(ModuleData.snapshot_name)
snapshot_disk_id = vmdiskapi.getVmDiskIdByName(ModuleData.snapshot_name, ModuleData.disk_alias)
snapshot_description='snapshotdisk'
xml_snapshotOnline_info = '''
<snapshot>
    <description>%s</description>
    <persist_memorystate>true</persist_memorystate>
    <vm id="%s"/>
    <disks>
       <disk id="%s"/>
    </disks>
</snapshot>'''%(snapshot_description,snapshot_vm_id,snapshot_disk_id)

'''
---------------------------------------------------------------------------------------------------
@note: ExpectedData
---------------------------------------------------------------------------------------------------
'''



expected_status_code_SnapshotOnline = 202
expected_status_code=200