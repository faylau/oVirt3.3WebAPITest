#encoding:utf-8

'''
Created on 2015��8��18��

@author: liuxd


'''
from TestAPIs.VirtualMachineAPIs import VirtualMachineAPIs, VmDiskAPIs,VmSnapshotAPIs
import TestData.VirtualMachine.ITC05_SetUp as ModuleData
from TestData.VirtualMachine.scenarios3_Snapshot import snapshot_description,snapshot_disk_id

cloneapi=VmSnapshotAPIs()
snapshot_id=cloneapi.getVmSnapshotIDBydisp(ModuleData.snapshot_name, snapshot_description)
snapshot_image_id=cloneapi.getVmSnapshot_disk_imageID(ModuleData.snapshot_name, snapshot_id, snapshot_description)

'''
---------------------------------------------------------------------------------------------------
@note: Test-Data-clone-onlinesnapshot
---------------------------------------------------------------------------------------------------
'''
cloneVmname='cloneOnlineSnapshot'       
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
---------------------------------------------------------------------------------------------------
@note: Test-Data-restore-onlinesnapshot
---------------------------------------------------------------------------------------------------
'''

xml_restore_vm_option='''
     <action>
        <restore_memory>true</restore_memory>
       <disks>
          <disk id="%s">
       <image_id>%s</image_id>
       <snapshot id="%s"/>
     </disk>
     </disks>
    </action>''' %(snapshot_disk_id,snapshot_image_id,snapshot_id)
    
    
      
'''
---------------------------------------------------------------------------------------------------
@note: ExpectedData
---------------------------------------------------------------------------------------------------
'''

expect_status_code_clone = 200
expected_status_code_Clone_vm = 202

