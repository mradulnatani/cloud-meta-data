import requests
import boto3
import json
import botocore

# Function to get IMDSv2 token
def get_imds_v2_token():
    try:
        token_url = "http://169.254.169.254/latest/api/token"
        headers = {"X-aws-ec2-metadata-token-ttl-seconds": "21600"}
        token = requests.put(token_url, headers=headers, timeout=2).text
        return token
    except Exception as e:
        return None

# Function to get metadata value by path
def get_metadata(path, token):
    try:
        url = f"http://169.254.169.254/latest/meta-data/{path}"
        headers = {"X-aws-ec2-metadata-token": token}
        response = requests.get(url, headers=headers, timeout=2)
        response.raise_for_status()
        return response.text
    except Exception:
        return ""

def get_instance_tags(instance_id, region):
    try:
        ec2 = boto3.client('ec2', region_name=region)
        response = ec2.describe_tags(
            Filters=[
                {'Name': 'resource-id', 'Values': [instance_id]}
            ]
        )
        tags = {tag['Key']: tag['Value'] for tag in response.get('Tags', [])}
        return tags
    except botocore.exceptions.ClientError as e:
        return f"Could not retrieve tags: {e}"
    except Exception as e:
        return f"Could not retrieve tags: {e}"

def main():
    token = get_imds_v2_token()
    if not token:
        print(json.dumps({"error": "Unable to retrieve IMDSv2 token."}, indent=4))
        return

    instance_id = get_metadata('instance-id', token)
    instance_type = get_metadata('instance-type', token)
    hostname = get_metadata('hostname', token)
    ami_id = get_metadata('ami-id', token)
    local_ipv4 = get_metadata('local-ipv4', token)
    public_ipv4 = get_metadata('public-ipv4', token)
    availability_zone = get_metadata('placement/availability-zone', token)
    
    # Derive region from availability zone (strip last char)
    region = availability_zone[:-1] if availability_zone else ""

    tags = ""
    if instance_id and region:
        tags = get_instance_tags(instance_id, region)
    else:
        tags = "Missing instance ID or region."

    output = {
        "instance_id": instance_id,
        "instance_type": instance_type,
        "hostname": hostname,
        "ami_id": ami_id,
        "local_ipv4": local_ipv4,
        "public_ipv4": public_ipv4,
        "availability_zone": availability_zone,
        "region": region,
        "tags": tags
    }

    print(json.dumps(output, indent=4))

if __name__ == "__main__":
    main()

