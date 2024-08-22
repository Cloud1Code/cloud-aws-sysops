import boto3
from botocore.exceptions import ClientError

def get_all_vpc_ids(ec2_client):
    """Fetch all VPC IDs in the account."""
    try:
        response = ec2_client.describe_vpcs()
        vpcs = response.get('Vpcs', [])
        if not vpcs:
            print("No VPCs found in your account.")
            return []
        return [vpc['VpcId'] for vpc in vpcs]
    except ClientError as e:
        print(f"Failed to retrieve VPC IDs. Error: {str(e)}")
        return []

def get_route_table_ids(ec2_client, vpc_id):
    """Fetch all route table IDs associated with the VPC."""
    try:
        response = ec2_client.describe_route_tables(
            Filters=[
                {'Name': 'vpc-id', 'Values': [vpc_id]}
            ]
        )
        route_tables = response.get('RouteTables', [])
        if not route_tables:
            print(f"No route tables found for VPC {vpc_id}.")
            return []
        return [rt['RouteTableId'] for rt in route_tables]
    except ClientError as e:
        print(f"Failed to retrieve route tables for VPC {vpc_id}. Error: {str(e)}")
        return []

def delete_route(ec2_client, route_table_id, cidr_block):
    """Attempt to delete the specified route from a route table."""
    try:
        ec2_client.delete_route(
            RouteTableId=route_table_id,
            DestinationCidrBlock=cidr_block
        )
        print(f"Route {cidr_block} successfully deleted from Route Table {route_table_id}.")
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'InvalidRoute.NotFound':
            print(f"Route {cidr_block} not found in Route Table {route_table_id}. Skipping...")
        elif error_code == 'InvalidRouteTableID.NotFound':
            print(f"Route Table {route_table_id} not found.")
        else:
            print(f"Failed to delete route {cidr_block} from Route Table {route_table_id}. Error: {str(e)}")

def main():
    cidr_block = "172.16.0.0/12"  # CIDR block of the route to delete

    # Create a boto3 EC2 client
    ec2_client = boto3.client('ec2')

    # Get all VPC IDs in the account
    vpc_ids = get_all_vpc_ids(ec2_client)
    if not vpc_ids:
        return

    print(f"Found VPC IDs: {vpc_ids}")

    # For each VPC, get associated route tables and delete the specified route
    for vpc_id in vpc_ids:
        print(f"Processing VPC ID: {vpc_id}")
        route_table_ids = get_route_table_ids(ec2_client, vpc_id)
        if not route_table_ids:
            continue
        for route_table_id in route_table_ids:
            delete_route(ec2_client, route_table_id, cidr_block)

if __name__ == "__main__":
    main()
