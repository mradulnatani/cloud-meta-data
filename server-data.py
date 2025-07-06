import requests
import boto3
import json
import botocore

# Step 1: Get IMDSv2 token
def get_imds_v2_token():
    try:
        response = requests.put(
            "http://169.254.169.254/latest/api/token",
            headers={"X-aws-ec2-metadata-token-ttl-seconds": "21600"},
            timeout=2
        )
        return response.text
    except Exception as e:
        print(f"Error getting IMDSv2 token: {e}")
        return None

# Step 2: Get instance metadata
def get_metadata(path, token):
    try:
        url = f"http://169.254.169.254/latest/meta-data/{path}"
        headers = {"X-aws-ec2-metadata-token": token}
        response = requests.get(url, headers=headers, timeout=2)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching metadata for {path}: {e}")
        return ""

# Step 3: Get tag values from EC2
def get_instance_tag_values(instance_id, region):
    try:
        ec2 = boto3.client('ec2', region_name=region)
        response = ec2.describe_tags(Filters=[
            {'Name': 'resource-id', 'Values': [instance_id]}
        ])
        tags = response.get('Tags', [])
        return [tag['Value'] for tag in tags]
    except botocore.exceptions.ClientError as e:
        print(f"ClientError: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []

# Step 4: Send tag values to Django
def send_tags_to_django(tags):
    try:
        api_url  = "https://6583-14-139-240-228.ngrok-free.app/api/receive-tags/"
        headers = {'Content-Type': 'application/json'}
        response = requests.post(api_url, json={"tags": tags}, headers=headers, timeout=5)
        print(f"Tags sent to Django (status {response.status_code}): {response.text}")
    except Exception as e:
        print(f"Failed to send tags to Django: {e}")

# Step 5: Main logic
def main():
    token = get_imds_v2_token()
    if not token:
        print("Could not retrieve metadata token")
        return

    instance_id = get_metadata("instance-id", token)
    az = get_metadata("placement/availability-zone", token)
    region = az[:-1] if az else ""

    if not instance_id or not region:
        print("Instance ID or Region is missing")
        return

    tags = get_instance_tag_values(instance_id, region)
    print("Retrieved tag values:", tags)

    if tags:
        send_tags_to_django(tags)
    else:
        print("No tag values to send")

if __name__ == "__main__":
    main()


