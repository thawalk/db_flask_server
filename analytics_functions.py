import os
from fabric import Connection

def list_ec2_instances(ec2):
    print('analytics getting called')
    instances = {}
    res = ec2.describe_instances()
    # print(res)
    for r in res['Reservations']:
        for ins in r['Instances']:
            if ins['State']['Name'] == 'running' or ins['State']['Name'] == 'pending':
                instances[ins['InstanceId']] = ins['PublicIpAddress']
    print('Instances {}'.format(instances))
    return instances

def create_security_group(name, description, ip_permissions, ec2):
    print("create security group")
    
    response = ec2.describe_vpcs()
    # print("this is the response")
    # print(response)
    vpc_id = response.get('Vpcs', [{}])[0].get('VpcId', '')

    response = ec2.create_security_group(GroupName=name, Description=description, VpcId=vpc_id)
    security_group_id = response['GroupId']
    print(security_group_id)
    print('Security Group Created {} in vpc {}'.format(security_group_id,vpc_id))
    
    data = ec2.authorize_security_group_ingress(
        GroupId=security_group_id,
        IpPermissions=ip_permissions)
    # print(data)
    print('Ingress Successfully Set {}'.format(data))
    return security_group_id

def create_key_pair(name, ec2):
    response = ec2.create_key_pair(
        KeyName=name
    )
    key = response['KeyMaterial']

    # write the pem file
    fil = open('{}.pem'.format(name), "w")
    fil.write(key)
    fil.close()

    # must give permission
    # os.system('chmod 400 {}.pem'.format(name))
    print('Key Pair {} Created'.format(name))
    return response

def create_instances(ami, max_count, instance_type, key, security_group_id, ec2, instance_name):
    # print('------------before the adding the {} instance--------------'.format(instance_name))
    # list_ec2_instances(ec2)

    instances = ec2.run_instances(
        ImageId = ami,
        MinCount = 1,
        MaxCount = max_count,
        InstanceType = instance_type,
        KeyName = key,
        SecurityGroupIds = [security_group_id]
    )
    instance_list = []
    print('---------------After the adding the {} instance---------------'.format(instance_name))
    for i in instances['Instances']:
        instance_list.append(i['InstanceId'])
    
    print('Instances Created {}'.format(instance_list))
    return instance_list

def get_publicdns(ec2):
    dnslist = {}
    res = ec2.describe_instances()
    for r in res['Reservations']:
        for ins in r['Instances']:
            if ins['State']['Name'] == 'running' or ins['State']['Name'] == 'pending':
                dnslist[ins['InstanceId']] = ins['PublicDnsName']
    print('List of active Instances %s' %dnslist)
    return dnslist

def theconnector(ip, key):
    c = Connection(
        host= ip,
        user="ubuntu",
        connect_kwargs={
            "key_filename": key + ".pem",
        },
    )
    return c





