import boto3
from botocore.exceptions import ClientError
import json

'''
:groupid 源安全组id
读取多个安全组中的rule
return 合并的IpPermissions数组
'''
def load_groups_rule(groupid):
    ippermissions_list = []
    try:
        ec2 = boto3.client('ec2')
        response = ec2.describe_security_groups(GroupIds=groupid)
        for sg in response["SecurityGroups"]:
            #print(sg['GroupName'])
            ippermissions_list.append(sg['IpPermissions'])
        print(ippermissions_list)
        return ippermissions_list
        # print(response["SecurityGroups"][0]["IpPermissions"])
    except ClientError as e:
        print(e)

'''
:groupid 复制策略的目标安全组id
:ippermissions_list 规则列表，格式为describe security group中的IpPermissions输出
'''
def add_rule_to_sg(groupid, ippermissions_list):
    try:
        ec2 = boto3.client('ec2')
        for rule in ippermissions_list:
            ec2.authorize_security_group_ingress(GroupId=groupid, IpPermissions=rule)
    except ClientError as e:
        print(e)
        


# if __name__ == '__main__':
#     # l = load_groups_rule(['sg-012718beb5e29ccf3', 'sg-02072084f12eb9ff4'])
#     # add_rule_to_sg('sg-0fd98b9de42b847ac', l)