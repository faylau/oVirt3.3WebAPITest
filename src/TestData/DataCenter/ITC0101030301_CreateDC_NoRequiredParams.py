#encoding:utf-8

__authors__ = ['"Liu Fei" <fei.liu@cs2c.com.cn>']
__version__ = "V0.1"

'''
# ChangeLog:
#---------------------------------------------------------------------------------
# Version        Date                Desc                            Author
#---------------------------------------------------------------------------------
# V0.1           2014/10/24          初始版本                                                            Liu Fei 
# V0.2                                存储类型不再是必需参数                                wei keke
#---------------------------------------------------------------------------------
'''

'''---------------------------------------------------------------------------------
@PreData
---------------------------------------------------------------------------------'''


'''---------------------------------------------------------------------------------
@note: TestData
---------------------------------------------------------------------------------'''
dc_info = '''
<data_driver>
    <data_center>
        <local>false</local>
        <version minor="4" major="3"/>
    </data_center>
    <data_center>
        <name>DC-ITC0101030301-1</name>
    </data_center>
</data_driver>
'''

'''---------------------------------------------------------------------------------
@note: ExpectedResult
---------------------------------------------------------------------------------'''
expected_status_code = 400
expected_info_list = [
'''
<fault><reason>Incomplete parameters</reason><detail>DataCenter [name] required for add</detail></fault>
''',
'''
<fault><reason>Incomplete parameters</reason><detail>DataCenter [local] required for add</detail></fault>
'''
]