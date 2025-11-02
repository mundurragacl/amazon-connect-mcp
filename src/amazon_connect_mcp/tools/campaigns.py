"""Tier 2: Outbound Campaigns tools - Defer loaded."""
from ..aws_clients import get_campaigns_client
from .config import _session_context


def _get_session_region():
    return _session_context.get("region")


async def campaigns_create(
    name: str,
    connect_instance_id: str,
    channel_subtype_config: dict
) -> dict:
    """Create an outbound campaign."""
    client = get_campaigns_client(_get_session_region())
    return client.create_campaign(
        name=name,
        connectInstanceId=connect_instance_id,
        channelSubtypeConfig=channel_subtype_config,
    )


async def campaigns_list(connect_instance_id: str, max_results: int = 25) -> dict:
    """List outbound campaigns."""
    client = get_campaigns_client(_get_session_region())
    return client.list_campaigns(
        filters={"instanceIdFilter": {"value": connect_instance_id, "operator": "Eq"}},
        maxResults=max_results,
    )


async def campaigns_describe(campaign_id: str) -> dict:
    """Get campaign details."""
    client = get_campaigns_client(_get_session_region())
    return client.describe_campaign(id=campaign_id)


async def campaigns_start(campaign_id: str) -> dict:
    """Start a campaign."""
    client = get_campaigns_client(_get_session_region())
    return client.start_campaign(id=campaign_id)


async def campaigns_pause(campaign_id: str) -> dict:
    """Pause a campaign."""
    client = get_campaigns_client(_get_session_region())
    return client.pause_campaign(id=campaign_id)


async def campaigns_resume(campaign_id: str) -> dict:
    """Resume a paused campaign."""
    client = get_campaigns_client(_get_session_region())
    return client.resume_campaign(id=campaign_id)


async def campaigns_stop(campaign_id: str) -> dict:
    """Stop a campaign."""
    client = get_campaigns_client(_get_session_region())
    return client.stop_campaign(id=campaign_id)


async def campaigns_delete(campaign_id: str) -> dict:
    """Delete a campaign."""
    client = get_campaigns_client(_get_session_region())
    return client.delete_campaign(id=campaign_id)


async def campaigns_get_state(campaign_id: str) -> dict:
    """Get campaign state."""
    client = get_campaigns_client(_get_session_region())
    return client.get_campaign_state(id=campaign_id)


async def campaigns_put_outbound_requests(
    campaign_id: str,
    outbound_requests: list[dict]
) -> dict:
    """Add contacts to dial list."""
    client = get_campaigns_client(_get_session_region())
    return client.put_outbound_request_batch(
        id=campaign_id,
        outboundRequests=outbound_requests,
    )


async def campaigns_start_onboarding(connect_instance_id: str, encryption_enabled: bool = False, encryption_key_arn: str | None = None) -> dict:
    """Start instance onboarding for outbound campaigns.
    
    Args:
        connect_instance_id: The Amazon Connect instance ID
        encryption_enabled: Whether to enable encryption (default False)
        encryption_key_arn: KMS key ARN if encryption is enabled
    """
    client = get_campaigns_client(_get_session_region())
    encryption_config = {"enabled": encryption_enabled}
    if encryption_enabled and encryption_key_arn:
        encryption_config["encryptionType"] = "KMS"
        encryption_config["keyArn"] = encryption_key_arn
    return client.start_instance_onboarding_job(
        connectInstanceId=connect_instance_id,
        encryptionConfig=encryption_config
    )


async def campaigns_get_onboarding_status(connect_instance_id: str) -> dict:
    """Get instance onboarding status for outbound campaigns."""
    client = get_campaigns_client(_get_session_region())
    return client.get_instance_onboarding_job_status(connectInstanceId=connect_instance_id)


async def campaigns_delete_onboarding(connect_instance_id: str) -> dict:
    """Delete instance onboarding job (to retry onboarding)."""
    client = get_campaigns_client(_get_session_region())
    return client.delete_instance_onboarding_job(connectInstanceId=connect_instance_id)
