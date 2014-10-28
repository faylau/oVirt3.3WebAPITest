#encoding:utf-8
import TestData.Cluster.ITC02_Setup as ModuleData
from TestAPIs.DataCenterAPIs import DataCenterAPIs

'''
@note: PreData 
'''
dc_name = ModuleData.dc_name
dc_id = DataCenterAPIs().getDataCenterIdByName(ModuleData.dc_name)
cluster_name = 'test-cluster'
cluster_info='''
<cluster>
        <name>%s</name>
        <cpu id="Intel Penryn Family"/>
        <data_center id= "%s"/>
</cluster>
'''%(cluster_name,dc_id)
nw_name = 'test_network'
nw_info = '''
<network>
    <name>%s</name>
    <data_center id= "%s"/> 
</network>
'''%(nw_name,dc_id)


status_code = 201