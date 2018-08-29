
from  simple_salesforce import Salesforce

import pandas as pd

USER='***'
PWD='***'
token='***'

# to access UAT set the sandbox true option
sf = Salesforce(username=USER, password=PWD, security_token=token, sandbox=True)


# (1) Set data type mapping# (1) Se 
mapping =\
{'id':'varchar',\
'boolean':'bool',\
'reference':'varchar',\
'string':'varchar',\
'picklist':'varchar',\
'textarea':'varchar',\
'double':'decimal',\
'phone':'varchar',\
'url':'varchar',\
'currency':'double',\
'int':'int',\
'datetime':'timestamp',\
'date':'timestamp',\
'email':'varchar',\
'multipicklist':'varchar',\
'percent':'decimal',\
'decimal':'decimal',\
'long':'bigint',\
'address':'varchar',\
'masterrecord':'varchar',\
'location':'varchar',\
'encryptedstring':'varchar'}


# (4) Size paramter set# (4) Si 
def set_parameter(column_type, record):
    '''Takes column type and json record to determine column length/ percision'''
    param = ''
    if column_type == 'varchar' or column_type == 'Unknown':
        param = "(" + str(record['length']) + ")"
    elif column_type == 'decimal':
        param = "(" + str(record['precision']) + "," + str(record['scale']) + ")"
    else:
        param = ''
    return param


# (5) Set Primary Key 
def set_primary_key(column_name):
    '''If id, then add primary key'''
    param = ''
    if column_name == 'id':
        param = 'Primary Key'
    else:
        param = ''
    return param   

# (6) Mapping function
import json
import sys

def map_columns (json_data):
    ''' Takes json data from rest API and convert to Create Table Statement '''
    field_list = []
    counter = 1
    for record in json_data['fields']:
        tmp = []
        column_name = record['name'].lower()
        try:
            column_type = mapping[record['type'].lower()]
        except:
            column_type = 'Unknown'
        column_param = set_parameter(column_type, record)
        primary_key_param = set_primary_key(column_name)

        tmp.append(column_name)
        tmp.append(column_type)
        tmp.append(column_param)
        tmp.append(primary_key_param)
        counter += 1
        if counter <= len(json_data['fields']):
            tmp.append(",")
        field_list.append(tmp)
    return field_list


from stringstring  importimport  TemplateTemplate
t = Template('''grant select on staging.$tablename to readonly_user; 
grant select on staging.$tablename to tabapp_user;
''')


def create_ddl(object_name):
    md = sf.restful("sobjects/{}/describe/".format(object_name), params=None)
    field_list = map_columns(md)
    tablename = object_name.lower()
    ddlfile = tablename + ".sql"
    with open(ddlfile, "w") as f:
        f.write('Create Table staging.{} (\n'.format(tablename))
        for row in field_list:
            f.write(' '.join(tuple(row)) +'\n')
        f.write(');\n')
        f.write(t.substitute(tablename=tablename))


objectnamesraw  = '''DMAPP__Account_Plan_Unit_Insight_Map__c
DMAPP__AM_Plan_Team__c
DMAPP__AM_Plan_Metric_Score__c
DMAPP__Account_Insight_Map__c
DMAPP__Account_Insight_Map_Node__c
DMAPP__Account_Insight_Map_Node_Parent__c'''        

objectnames=objectnamesraw.split('\n')

for object_name in objectnames:
    create_ddl(object_name)



