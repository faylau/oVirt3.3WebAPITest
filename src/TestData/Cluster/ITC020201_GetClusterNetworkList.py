#encoding:utf-8
import TestData.Cluster.ITC02_Setup as ModuleData
from TestAPIs.DataCenterAPIs import DataCenterAPIs
cluster_name = 'test-cluster'

'''
@note: PreData
'''
dc_id = DataCenterAPIs().getDataCenterIdByName(ModuleData.dc_name)
cluster_info = '''
<cluster>
        <name>%s</name>
        <cpu id="Intel Penryn Family"/>
        <data_center  id="%s"/>
</cluster>
''' %(cluster_name,dc_id)


status_code = 200
