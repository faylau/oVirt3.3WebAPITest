#encoding:utf-8

nw_name1 = 'network001'
nw_name2 = 'network002'



'''
@note: PreData
'''
nw_info1 = '''
<network>
    <name>%s</name>
    <data_center id= "5849b030-626e-47cb-ad90-3ce782d831b3"/> 
    <vlan id = "2"/>
        
</network>
''' %nw_name1
'''
@note: TestData
'''
nw_info2 = '''
<network>
    <name>%s</name>
    <data_center id= "5849b030-626e-47cb-ad90-3ce782d831b3"/> 
    <vlan id = "2"/>
</network>
''' %nw_name2
'''
@note: ExpectedData
'''
expected_status_code = 409
expected_info ='''
<fault>
    <reason>Operation Failed</reason>
    <detail>[The specified VLAN ID (2) is already in use.]</detail>
</fault>
'''
