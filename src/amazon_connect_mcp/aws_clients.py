import boto3
from functools import lru_cache
from .config import settings


def get_connect_client(region: str | None = None):
    """Get Connect client for specified region or default."""
    return boto3.client("connect", region_name=region or settings.aws_region)


def get_instance_region(instance_id: str) -> str:
    """Get the region where a Connect instance is located."""
    # Try common regions first
    common_regions = ["us-east-1", "us-west-2", "eu-west-1", "ap-southeast-2"]
    
    for region in common_regions:
        try:
            client = get_connect_client(region)
            client.describe_instance(InstanceId=instance_id)
            return region
        except client.exceptions.ResourceNotFoundException:
            continue
        except Exception:
            continue
    
    # If not found in common regions, try all regions
    ec2 = boto3.client('ec2')
    all_regions = [r['RegionName'] for r in ec2.describe_regions()['Regions']]
    
    for region in all_regions:
        if region in common_regions:
            continue
        try:
            client = get_connect_client(region)
            client.describe_instance(InstanceId=instance_id)
            return region
        except client.exceptions.ResourceNotFoundException:
            continue
        except Exception:
            continue
    
    raise ValueError(f"Instance {instance_id} not found in any region")


def get_cases_client(region: str | None = None):
    """Get Cases client for specified region or default."""
    return boto3.client("connectcases", region_name=region or settings.aws_region)


@lru_cache
def get_profiles_client(region: str | None = None):
    """Get Customer Profiles client for specified region or default."""
    return boto3.client("customer-profiles", region_name=region or settings.aws_region)


@lru_cache
def get_wisdom_client(region: str | None = None):
    """Get Amazon Q in Connect client for specified region or default."""
    return boto3.client("qconnect", region_name=region or settings.aws_region)


@lru_cache
def get_campaigns_client(region: str | None = None):
    """Get Connect Campaigns client for specified region or default."""
    return boto3.client("connectcampaignsv2", region_name=region or settings.aws_region)
