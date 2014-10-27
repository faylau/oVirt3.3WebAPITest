#coding:utf-8


__authors__ = ['"Liu Fei" <fei.liu@cs2c.com.cn>']
__version__ = "V0.1"

'''
# ChangeLog:
#---------------------------------------------------------------------------------
# Version        Date                Desc                            Author
#---------------------------------------------------------------------------------
# V0.1           2014/10/24          初始版本                                                            Liu Fei 
#---------------------------------------------------------------------------------
'''

from Configs.GlobalConfig import ExportStorages
from TestData.DataCenter import ITC01_SetUp as ModuleData

'''
---------------------------------------------------------------------------------------------------
@note: Pre-Test-Data
---------------------------------------------------------------------------------------------------
'''
########################################################################
# 1个数据中心信息（使用模块测试环境中的dc_nfs）                                                                                                                                    
########################################################################
dc_nfs_name = ModuleData.dc_nfs_name

#######################################################################################
# 1个存储域信息（只需要提供存储域名称，因为它是在模块测试环境中已经创建的data2_nfs）                                                                                                                               
#######################################################################################
data_nfs_name = ModuleData.data2_nfs_name

'''
---------------------------------------------------------------------------------------------------
@note: Test-Data
-----
'''
export2 = ExportStorages['Export-Storage3']
export2_name = 'export2-ITC0102030302'
export2_ip = export2['ip']
export2_path = export2['path']
xml_export2_info = '''
    <storage_domain>
        <name>%s</name>
        <type>export</type>
        <host>
            <name>%s</name>
        </host>
        <storage>
            <type>nfs</type>
            <address>%s</address>
            <path>%s</path>
        </storage>
    </storage_domain>
''' % (export2_name, ModuleData.host1_name, export2_ip, export2_path)


'''
---------------------------------------------------------------------------------------------------
@note: Post-Test-Data
---------------------------------------------------------------------------------------------------
'''
# name变量在执行删除的函数中作为参数传递，此处不指定。
xml_del_export_option = '''
<storage_domain>
    <host>
        <name>%s</name>
    </host>
    <format>true</format>
    <async>false</async>
</storage_domain>
'''



'''
---------------------------------------------------------------------------------------------------
@note: ExpectedResult
---------------------------------------------------------------------------------------------------
'''
expected_status_code_attach_sd = 201                    # 将存储域附加到数据中心，成功，返回状态码
expected_status_code_attach_sd_fail = 409               # 将存储域附加到数据中心，失败，返回状态码
expected_info_attach_sd_fail = '''
<fault>
    <reason>Operation Failed</reason>
    <detail>[Cannot attach more than one Import/Export Storage Domain to the same Data Center. If you want to use a newly created Domain, detach the existing attached Domain and attach the new one.]</detail>
</fault>
'''
expected_status_code_deactivate_sd = 200                # 将存储域设置为维护状态，成功，返回状态码
expected_status_code_detach_sd = 200                    # 将存储域从数据中心分离，成功，返回状态码