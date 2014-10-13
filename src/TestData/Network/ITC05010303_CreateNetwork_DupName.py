#encoding:utf-8

nw_name = 'network001'



'''
@note: PreData and TestData
'''
nw_info = '''
<network>
    <name>%s</name>
    <data_center id= "5849b030-626e-47cb-ad90-3ce782d831b3"/>    
</network>
''' %nw_name

'''
@note: ExpectedData
'''
expected_status_code = 409
expected_info ='''
<fault>
    <reason>Operation Failed</reason>
    <detail>[Cannot add Network. The logical network's name is already used by an existing logical network in the same data-center.
-Please choose a different name.]</detail>
</fault>
'''
