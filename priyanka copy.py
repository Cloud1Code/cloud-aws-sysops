

import boto3

def delete_route_in_custom_route_tables(vpc_id, destination_cidr='172.16.0.0/12'):
    ec2 = boto3.client('ec2')

    # Retrieve all route tables in the VPC
    route_tables = ec2.describe_route_tables(
        Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}]
    )['RouteTables']

    for route_table in route_tables:
        for route in route_table['Routes']:
            if route['DestinationCidrBlock'] == destination_cidr and 'GatewayId' in route:
                if route['GatewayId'].startswith('igw-'):
                    try:
                        # Delete the route
                        ec2.delete_route(
                            RouteTableId=route_table['RouteTableId'],
                            DestinationCidrBlock=destination_cidr
                        )
                        print(f"Deleted route {destination_cidr} from {route_table['RouteTableId']}")
                    except Exception as e:
                        print(f"Error deleting route: {e}")

if __name__ == "__main__":
    # Replace 'your-vpc-id' with your actual VPC ID
    vpc_id = 'vpc-086e1e11f57a8654a'
    delete_route_in_custom_route_tables(vpc_id)