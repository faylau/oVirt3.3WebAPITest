#encoding:utf-8
import TestData.Cluster.ITC02_Setup as ModuleData
from TestAPIs.DataCenterAPIs import DataCenterAPIs
'''
@note: PreData and TestData
'''
dc_id = DataCenterAPIs().getDataCenterIdByName(ModuleData.dc_name)
cluster_name = 'test-cluster'
cluster_info = '''
<cluster>
        <name>%s</name>
        <cpu id="Intel Penryn Family"/>
        <data_center  id="%s"/>  
</cluster>
''' %(cluster_name,dc_id)

'''
@ExpectedData
'''
status_code = 409
error_info = '''
<fault>
    <reason>Operation Failed</reason>
    <detail>[Cannot create Cluster. Cluster name is already in use.]</detail>
</fault>
'''