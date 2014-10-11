#encoding:utf-8

nw_name1 = 'network001'
nw_name2 = 'network002'
dc_name = 'Default'


'''
@note: PreData
'''
nw_info1 = '''
<network>
    <name>%s</name>
    <data_center id= "5849b030-626e-47cb-ad90-3ce782d831b3"/>    
</network>
''' %nw_name1

nw_info2 = '''
<network>
    <name>%s</name>
    <data_center id= "5849b030-626e-47cb-ad90-3ce782d831b3"/>    
</network>
''' %nw_name2

'''
@note:TestData 
'''
update_info = '''
<network>
    <name>%s</name>
    <description>lalala</description>   
    <mtu>2000</mtu>
</network>
'''%nw_name2

'''
@note:ExpectedData
'''
expected_status_code = 409
expected_info = '''
<fault>
    <reason>Operation Failed</reason>
    <detail>[Cannot edit Network. The logical network's name is already used by an existing logical network in the same data-center.
-Please choose a different name.]</detail>
</fault>
'''