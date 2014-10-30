#encoding:utf-8
import TestData.Cluster.ITC02_Setup as ModuleData
from TestAPIs.DataCenterAPIs import DataCenterAPIs
from Configs.GlobalConfig import Hosts
dc_id = DataCenterAPIs().getDataCenterIdByName(ModuleData.dc_name)
cluster_name = 'test-cluster'

'''
@note: PreData
'''
cluster_info = '''
<cluster>
        <name>%s</name>
        <cpu id="Intel Penryn Family"/>
        <data_center  id="%s"/>
</cluster>
''' %(cluster_name,dc_id)

vm_name = 'vm3'
vm_info='''
<vm>
        <name>vm3</name>
        <description>Virtual Machine 2</description>
        <type>server</type>
        <memory>536870912</memory>
        <cluster>
            <name>%s</name>
        </cluster>
        <template>
            <name>Blank</name>
        </template>
        <cpu>
            <topology sockets="2" cores="1"/>
        </cpu>
        <os>
            <boot dev="cdrom"/>
            <boot dev="hd"/>
        </os>
    </vm>
'''%cluster_name

'''
@note: TestData
'''
host_del_option = '''
<action>
    <force>true</force>
    <async>false</async>
</action>
'''

'''
@note: ExpectedData
'''
status_code = 409
expected_info = '''
<fault>
    <reason>Operation Failed</reason>
    <detail>[Cannot remove Cluster. Host Cluster contains one or more Vms.]</detail>
</fault>
'''