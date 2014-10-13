#encoding:utf-8


'''
@PreData
'''


'''
@note: TestData
'''
cluster_info = '''
<data_driver>
    <cluster>
        <cpu id="Intel Penryn Family"/>
        <data_center  id="5849b030-626e-47cb-ad90-3ce782d831b3"/>
    </cluster>
    <cluster>
        <name>Cluster001</name>
        <cpu id="Intel Penryn Family"/> 
    </cluster>
    <cluster>
        <name>Cluster001</name>
        <data_center  id="5849b030-626e-47cb-ad90-3ce782d831b3"/> 
    </cluster>
</data_driver>
'''

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