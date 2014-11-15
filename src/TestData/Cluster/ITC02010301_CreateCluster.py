#encoding:utf-8


import TestData.Cluster.ITC02_Setup as ModuleData
from TestAPIs.DataCenterAPIs import DataCenterAPIs

'''
@note: TestData
'''
dc_id = DataCenterAPIs().getDataCenterIdByName(ModuleData.dc_name)
cluster_name = 'cluster-ITC02'
cluster_info = '''
<cluster>
        <name>%s</name>
        <cpu id="Intel Penryn Family"/>
        <data_center  id="%s"/>
        <virt_service>true</virt_service>
        <gluster_service>true</gluster_service>
        <tunnel_migration>true</tunnel_migration>
        <trusted_service>false</trusted_service> 
        <ballooning_enabled>true</ballooning_enabled>  
</cluster>
''' %(cluster_name,dc_id)

status_code = 201