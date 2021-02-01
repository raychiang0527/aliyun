from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
import json
import requests
import re
 
# ��ʼ��
client = AcsClient('<AccessKey>', '<AccessKeySrc>', 'cn-hangzhou')
request = CommonRequest()
request.set_domain('alidns.aliyuncs.com')
request.set_version('2015-01-09')
domain = "����"
prefix = "ǰ׺"
 
# ��ȡ����IP��ַ
html_text = requests.get("https://ip.cn/").text
ip_text = re.findall(r'(?<![\.\d])(?:25[0-5]\.|2[0-4]\d\.|[01]?\d\d?\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)(?![\.\d])', html_text)
ip = ip_text[0]
print("����IP��ַ��"+ ip)
print("������"+ prefix + "." + domain)
 
# ��ȡ����������RecordId
request.set_action_name('DescribeDomainRecords')
request.add_query_param('DomainName', domain)
response = client.do_action_with_exception(request)
jsonObj = json.loads(response.decode("UTF-8"))
records = jsonObj["DomainRecords"]["Record"]
record = None
for rec in records:
    if rec["RR"] == prefix:
        record = rec
        break
if record == None:
    print("δ�ҵ�����������¼")
    exit()
elif record['Value'] == ip:
    print("����IP��¼��Ϊ����")
    exit()
 
# ����IP��¼
request.set_action_name('UpdateDomainRecord')
request.add_query_param('RecordId', record['RecordId'])
request.add_query_param('RR', prefix)
request.add_query_param('Type', 'A')
request.add_query_param('Value', ip)
response = client.do_action_with_exception(request)
 
print("DDNS�������\n")