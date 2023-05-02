# This script will first list all EC2 instances across all regions, 
# and for each instance it will print the instance ID, private IP, public IP and other instance info. 
# For example, if an instance does not have a public IP or a private IP, the script will print "N/A" instead

import boto3
import csv

# Create a boto3 client for EC2
ec2_client = boto3.client('ec2')

# Get a list of all regions
all_regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]

# Create a list to store all instances
all_instances = []

# Iterate over each region and list all instances
for region_name in all_regions:
    print(f"Instances in {region_name}:")
    print('_'*60)
    ec2_region_client = boto3.client('ec2', region_name=region_name)
    reservations = ec2_region_client.describe_instances()['Reservations']
    for reservation in reservations:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            instance_type = instance.get('InstanceType', 'N/A')
            instance_state = instance.get('State', {}).get('Name', 'N/A')
            private_ip = instance.get('PrivateIpAddress', 'N/A')
            public_ip = instance.get('PublicIpAddress', 'N/A')
            image_id = instance.get('ImageId', 'N/A')
            tags = instance.get('Tags', [])
            name_tag = next((tag['Value'] for tag in instance['Tags'] if tag['Key'] == 'Name'), 'N/a') if tags else 'N/A'
            instance_info = {
                'Instance ID': instance_id,
                'Private IP': private_ip,
                'Public IP': public_ip,
                'Image ID (AMI)': image_id,
                'Name': name_tag,
                'Instance Type': instance_type,
                'Instance Status': instance_state,
                'Region': region_name
            }
            all_instances.append(instance_info)
            print(f"Instance ID: {instance_id}")
            print(f"Private IP: {private_ip}")
            print(f"Public IP: {public_ip}")
            print(f"Image ID (AMI): {image_id}")
            print(f"Name: {name_tag}")
            print(f"Instance Type: {instance_type}")
            print(f"Instance current Status: {instance_id} is {instance_state}")
            print('_'*60)

# Write the instance information to a CSV file
with open('ec2_instances.csv', mode='w') as csv_file:
    fieldnames = ['Instance ID', 'Private IP', 'Public IP', 'Image ID (AMI)', 'Name', 'Instance Type', 'Instance Status', 'Region']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for instance_info in all_instances:
        writer.writerow(instance_info)
