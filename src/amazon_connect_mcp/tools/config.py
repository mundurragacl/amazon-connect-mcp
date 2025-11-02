"""Tier 2: Configuration tools - Defer loaded."""
from ..aws_clients import get_connect_client


# Contact Flows
async def config_list_contact_flows(instance_id: str, max_results: int = 100) -> dict:
    """List contact flows."""
    client = get_connect_client()
    return client.list_contact_flows(InstanceId=instance_id, MaxResults=max_results)


async def config_describe_contact_flow(instance_id: str, contact_flow_id: str) -> dict:
    """Get contact flow details."""
    client = get_connect_client()
    return client.describe_contact_flow(InstanceId=instance_id, ContactFlowId=contact_flow_id)


async def config_create_contact_flow(
    instance_id: str,
    name: str,
    flow_type: str,
    content: str,
    description: str = ""
) -> dict:
    """Create a contact flow. Types: CONTACT_FLOW, CUSTOMER_QUEUE, CUSTOMER_HOLD, etc."""
    client = get_connect_client()
    return client.create_contact_flow(
        InstanceId=instance_id,
        Name=name,
        Type=flow_type,
        Content=content,
        Description=description,
    )


async def config_update_contact_flow_content(
    instance_id: str,
    contact_flow_id: str,
    content: str
) -> dict:
    """Update contact flow content."""
    client = get_connect_client()
    return client.update_contact_flow_content(
        InstanceId=instance_id,
        ContactFlowId=contact_flow_id,
        Content=content,
    )


# Queues
async def config_create_queue(
    instance_id: str,
    name: str,
    hours_of_operation_id: str,
    description: str = ""
) -> dict:
    """Create a queue."""
    client = get_connect_client()
    return client.create_queue(
        InstanceId=instance_id,
        Name=name,
        HoursOfOperationId=hours_of_operation_id,
        Description=description,
    )


async def config_describe_queue(instance_id: str, queue_id: str) -> dict:
    """Get queue details."""
    client = get_connect_client()
    return client.describe_queue(InstanceId=instance_id, QueueId=queue_id)


async def config_update_queue_status(
    instance_id: str,
    queue_id: str,
    status: str
) -> dict:
    """Update queue status. Status: ENABLED or DISABLED."""
    client = get_connect_client()
    return client.update_queue_status(InstanceId=instance_id, QueueId=queue_id, Status=status)


# Routing Profiles
async def config_list_routing_profiles(instance_id: str, max_results: int = 100) -> dict:
    """List routing profiles."""
    client = get_connect_client()
    return client.list_routing_profiles(InstanceId=instance_id, MaxResults=max_results)


async def config_create_routing_profile(
    instance_id: str,
    name: str,
    default_outbound_queue_id: str,
    description: str = "",
    media_concurrencies: list[dict] | None = None
) -> dict:
    """Create a routing profile."""
    client = get_connect_client()
    concurrencies = media_concurrencies or [
        {"Channel": "VOICE", "Concurrency": 1},
        {"Channel": "CHAT", "Concurrency": 2},
    ]
    return client.create_routing_profile(
        InstanceId=instance_id,
        Name=name,
        DefaultOutboundQueueId=default_outbound_queue_id,
        Description=description,
        MediaConcurrencies=concurrencies,
    )


# Hours of Operation
async def config_list_hours_of_operations(instance_id: str, max_results: int = 100) -> dict:
    """List hours of operation."""
    client = get_connect_client()
    return client.list_hours_of_operations(InstanceId=instance_id, MaxResults=max_results)


async def config_create_hours_of_operation(
    instance_id: str,
    name: str,
    time_zone: str,
    config: list[dict]
) -> dict:
    """Create hours of operation."""
    client = get_connect_client()
    return client.create_hours_of_operation(
        InstanceId=instance_id,
        Name=name,
        TimeZone=time_zone,
        Config=config,
    )


# Users
async def config_list_users(instance_id: str, max_results: int = 100) -> dict:
    """List users."""
    client = get_connect_client()
    return client.list_users(InstanceId=instance_id, MaxResults=max_results)


async def config_describe_user(instance_id: str, user_id: str) -> dict:
    """Get user details."""
    client = get_connect_client()
    return client.describe_user(InstanceId=instance_id, UserId=user_id)


async def config_create_user(
    instance_id: str,
    username: str,
    routing_profile_id: str,
    security_profile_ids: list[str],
    phone_type: str = "SOFT_PHONE"
) -> dict:
    """Create a user."""
    client = get_connect_client()
    return client.create_user(
        InstanceId=instance_id,
        Username=username,
        RoutingProfileId=routing_profile_id,
        SecurityProfileIds=security_profile_ids,
        PhoneConfig={"PhoneType": phone_type},
    )


async def config_update_user_routing_profile(
    instance_id: str,
    user_id: str,
    routing_profile_id: str
) -> dict:
    """Update user's routing profile."""
    client = get_connect_client()
    return client.update_user_routing_profile(
        InstanceId=instance_id,
        UserId=user_id,
        RoutingProfileId=routing_profile_id,
    )


# Agent Status
async def config_list_agent_statuses(instance_id: str, max_results: int = 100) -> dict:
    """List agent statuses."""
    client = get_connect_client()
    return client.list_agent_statuses(InstanceId=instance_id, MaxResults=max_results)


async def config_put_user_status(
    instance_id: str,
    user_id: str,
    agent_status_id: str
) -> dict:
    """Set agent's current status."""
    client = get_connect_client()
    return client.put_user_status(
        InstanceId=instance_id,
        UserId=user_id,
        AgentStatusId=agent_status_id,
    )
