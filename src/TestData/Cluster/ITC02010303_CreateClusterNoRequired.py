#encoding:utf-8
import TestData.Cluster.ITC02_Setup as ModuleData
from TestAPIs.DataCenterAPIs import DataCenterAPIs

'''
@PreData
'''


'''
@note: TestData
'''
dc_id = DataCenterAPIs().getDataCenterIdByName(ModuleData.dc_name)
cluster_info = '''
<data_driver>
    <cluster>
        <cpu id="Intel Penryn Family"/>
        <data_center  id="%s"/>
    </cluster>
    <cluster>
        <name>Cluster001</name>
        <cpu id="Intel Penryn Family"/> 
    </cluster>
    <cluster>
        <name>Cluster001</name>
        <data_center  id="%s"/> 
    </cluster>
</data_driver>
'''%(dc_id,dc_id)

'''
@note: ExpectedResult
'''
expected_status_code = 400
expected_info_list = [
'''
<fault><reason>Incomplete parameters</reason><detail>Cluster [name] required for add</detail></fault>
''',
'''
<fault><reason>Incomplete parameters</reason><detail>Cluster [dataCenter.name|id] required for add</detail></fault>
''',
'''
<fault><reason>Operation Failed</reason><detail>[Cannot add Cluster. CPU type must be specified]</detail></fault>

'''
]