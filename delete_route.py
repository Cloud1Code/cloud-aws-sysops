import boto3
import sys

def get_vpc_id(ec2_client, vpc_name):
    response = ec2_client.describe_vpcs(
        Filters=[
            {'Name': 'tag:Name', 'Values': [vpc_name]}
        ]
    )
    vpcs = response.get('Vpcs', [])
    if not vpcs:
        print(f"VPC with name {vpc_name} not found!")
        sys.exit(1)
    return vpcs[0]['VpcId']

def get_route_table_id(ec2_client, vpc_id):
    response = ec2_client.describe_route_tables(
        Filters=[
            {'Name': 'vpc-id', 'Values': [vpc_id]}
        ]
    )
    route_tables = response.get('RouteTables', [])
    if not route_tables:
        print(f"Route Table not found for VPC {vpc_id}!")
        sys.exit(1)
    return route_tables[0]['RouteTableId']

def delete_route(ec2_client, route_table_id, cidr_block):
    try:
        ec2_client.delete_route(
            RouteTableId=route_table_id,
            DestinationCidrBlock=cidr_block
        )
        print(f"Route {cidr_block} successfully deleted from Route Table {route_table_id}.")
    except Exception as e:
        print(f"Failed to delete route {cidr_block} from Route Table {route_table_id}. Error: {str(e)}")
        sys.exit(1)

def main():
    vpc_name = "my-test-VPC1"
    cidr_block = "172.16.0.0/12"

    # Create a boto3 EC2 client
    ec2_client = boto3.client('ec2')

    # Get the VPC ID
    vpc_id = get_vpc_id(ec2_client, vpc_name)
    print(f"Found VPC ID: {vpc_id}")

    # Get the Route Table ID
    route_table_id = get_route_table_id(ec2_client, vpc_id)
    print(f"Found Route Table ID: {route_table_id}")

    # Delete the specified route
    delete_route(ec2_client, route_table_id, cidr_block)

if __name__ == "__main__":
    main()
list