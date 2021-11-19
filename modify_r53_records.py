import boto3
import xlrd

client = boto3.client('route53')


def get_cname_list(HostedZoneId):
    cname_record_list = []
    paginator = client.get_paginator('list_resource_record_sets')
    source_zone_records = paginator.paginate(HostedZoneId=HostedZoneId)
    for record_set in source_zone_records:
        for record in record_set['ResourceRecordSets']:
            if record['Type'] == 'CNAME':
                print(record['Name'])
                cname_record_list.append(record['Name'])

    return cname_record_list


def add_cname_record(source, target, HostedZoneId):
    try:
        response = client.change_resource_record_sets(
            HostedZoneId=HostedZoneId,
            ChangeBatch={
                'Comment': 'add %s -> %s' % (source, target),
                'Changes': [
                    {
                        'Action': 'UPSERT',
                        'ResourceRecordSet': {
                            'Name': source,
                            'Type': 'CNAME',
                            'TTL': 300,
                            'ResourceRecords': [{'Value': target}]
                        }
                    }]
            })
    except Exception as e:
        print(e)


if __name__ == '__main__':
    # cname_list = get_cname_list('Z088706320IW42K59Z1GX')
    data = xlrd.open_workbook('/Users/jiajuche/Desktop/2.xls')
    table = data.sheets()[0]
    operate_number = 1
    for i in range(table.nrows):
        row_value = table.row_values(i)
        print(row_value)
        # if row_value[0] in cname_list:
        #     print(f'{row_value[0]} in cname_list')
        # else:
        #     print(f'{row_value[0]} not in cname_list')
        # test code
        add_cname_record(row_value[0], row_value[1], 'Z088706320IW42K59Z1GX')
        print(f'已经更新到第{i+1}行')
        if operate_number <= 1:
            num = input(f'已经更新到第{i+1}行, 请输入继续操作的记录数量：')
            operate_number = int(num)
        else:
            operate_number = operate_number - 1

