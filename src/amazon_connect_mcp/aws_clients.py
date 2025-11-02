import boto3
from functools import lru_cache
from .config import settings


def get_connect_client(region: str | None = None):
    """Get Connect client for specified region or default."""
    return boto3.client("connect", region_name=region or settings.aws_region)


@lru_cache
def get_cases_client():
    return boto3.client("connectcases", region_name=settings.aws_region)


@lru_cache
def get_profiles_client():
    return boto3.client("customer-profiles", region_name=settings.aws_region)


@lru_cache
def get_wisdom_client():
    return boto3.client("qconnect", region_name=settings.aws_region)


@lru_cache
def get_campaigns_client():
    return boto3.client("connectcampaignsv2", region_name=settings.aws_region)
