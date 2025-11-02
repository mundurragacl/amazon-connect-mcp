"""Tier 2: Outbound Campaigns tools - Defer loaded."""
from ..aws_clients import get_campaigns_client


async def campaigns_create(
    name: str,
    connect_instance_id: str,
    channel_subtype_config: dict
) -> dict:
    """Create an outbound campaign."""
    client = get_campaigns_client()
    return client.create_campaign(
        name=name,
        connectInstanceId=connect_instance_id,
        channelSubtypeConfig=channel_subtype_config,
    )


async def campaigns_list(connect_instance_id: str, max_results: int = 25) -> dict:
    """List outbound campaigns."""
    client = get_campaigns_client()
    return client.list_campaigns(
        filters={"instanceIdFilter": {"value": connect_instance_id, "operator": "Eq"}},
        maxResults=max_results,
    )


async def campaigns_describe(campaign_id: str) -> dict:
    """Get campaign details."""
    client = get_campaigns_client()
    return client.describe_campaign(id=campaign_id)


async def campaigns_start(campaign_id: str) -> dict:
    """Start a campaign."""
    client = get_campaigns_client()
    return client.start_campaign(id=campaign_id)


async def campaigns_pause(campaign_id: str) -> dict:
    """Pause a campaign."""
    client = get_campaigns_client()
    return client.pause_campaign(id=campaign_id)


async def campaigns_resume(campaign_id: str) -> dict:
    """Resume a paused campaign."""
    client = get_campaigns_client()
    return client.resume_campaign(id=campaign_id)


async def campaigns_stop(campaign_id: str) -> dict:
    """Stop a campaign."""
    client = get_campaigns_client()
    return client.stop_campaign(id=campaign_id)


async def campaigns_delete(campaign_id: str) -> dict:
    """Delete a campaign."""
    client = get_campaigns_client()
    return client.delete_campaign(id=campaign_id)


async def campaigns_get_state(campaign_id: str) -> dict:
    """Get campaign state."""
    client = get_campaigns_client()
    return client.get_campaign_state(id=campaign_id)


async def campaigns_put_outbound_requests(
    campaign_id: str,
    outbound_requests: list[dict]
) -> dict:
    """Add contacts to dial list."""
    client = get_campaigns_client()
    return client.put_outbound_request_batch(
        id=campaign_id,
        outboundRequests=outbound_requests,
    )
