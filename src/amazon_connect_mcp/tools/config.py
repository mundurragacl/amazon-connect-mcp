"""Tier 2: Configuration tools - Defer loaded."""
from ..aws_clients import get_connect_client

# Session context for region - can be set by set_session tool
_session_context = {
    "region": None,
    "instance_id": None
}


def _get_client(region: str | None = None):
    """Get client using provided region, session context, or default."""
    effective_region = region or _session_context.get("region")
    return get_connect_client(effective_region)


def _get_instance(instance_id: str | None = None) -> str:
    """Get instance ID from parameter or session context."""
    effective_id = instance_id or _session_context.get("instance_id")
    if not effective_id:
        raise ValueError("instance_id required - provide it or use set_session first")
    return effective_id


# Session Management
async def set_session(
    instance_id: str | None = None,
    region: str | None = None
) -> dict:
    """Set session context for subsequent operations.
    
    Once set, all config tools will use these defaults unless overridden.
    
    Args:
        instance_id: Default Connect instance ID
        region: AWS region (e.g., 'us-east-1', 'us-west-2')
    
    Returns current session context.
    """
    if instance_id:
        _session_context["instance_id"] = instance_id
    if region:
        _session_context["region"] = region
    return {
        "session": _session_context.copy(),
        "message": "Session context updated. All subsequent config operations will use these defaults."
    }


async def get_session() -> dict:
    """Get current session context."""
    return {"session": _session_context.copy()}


async def clear_session() -> dict:
    """Clear session context."""
    _session_context["region"] = None
    _session_context["instance_id"] = None
    return {"message": "Session context cleared"}


# Contact Flows
async def config_list_contact_flows(
    instance_id: str,
    max_results: int = 100,
    region: str | None = None
) -> dict:
    """List contact flows."""
    client = _get_client(region)
    return client.list_contact_flows(InstanceId=instance_id, MaxResults=max_results)


async def config_describe_contact_flow(
    instance_id: str,
    contact_flow_id: str,
    region: str | None = None
) -> dict:
    """Get contact flow details."""
    client = _get_client(region)
    return client.describe_contact_flow(InstanceId=instance_id, ContactFlowId=contact_flow_id)


async def config_create_contact_flow(
    name: str,
    flow_type: str,
    content: str,
    description: str = "",
    instance_id: str | None = None,
    region: str | None = None
) -> dict:
    """Create a contact flow. Types: CONTACT_FLOW, CUSTOMER_QUEUE, CUSTOMER_HOLD, etc."""
    client = _get_client(region)
    effective_instance_id = _get_instance(instance_id)
    return client.create_contact_flow(
        InstanceId=effective_instance_id,
        Name=name,
        Type=flow_type,
        Content=content,
        Description=description,
    )


async def config_update_contact_flow_content(
    instance_id: str,
    contact_flow_id: str,
    content: str,
    region: str | None = None
) -> dict:
    """Update contact flow content."""
    client = _get_client(region)
    return client.update_contact_flow_content(
        InstanceId=instance_id,
        ContactFlowId=contact_flow_id,
        Content=content,
    )


# Queues
async def config_create_queue(
    name: str,
    hours_of_operation_id: str,
    description: str = "",
    instance_id: str | None = None,
    region: str | None = None
) -> dict:
    """Create a queue."""
    client = _get_client(region)
    effective_instance_id = _get_instance(instance_id)
    return client.create_queue(
        InstanceId=effective_instance_id,
        Name=name,
        HoursOfOperationId=hours_of_operation_id,
        Description=description,
    )


async def config_describe_queue(
    instance_id: str,
    queue_id: str,
    region: str | None = None
) -> dict:
    """Get queue details."""
    client = _get_client(region)
    return client.describe_queue(InstanceId=instance_id, QueueId=queue_id)


async def config_update_queue_status(
    instance_id: str,
    queue_id: str,
    status: str,
    region: str | None = None
) -> dict:
    """Update queue status. Status: ENABLED or DISABLED."""
    client = _get_client(region)
    return client.update_queue_status(InstanceId=instance_id, QueueId=queue_id, Status=status)


# Phone Numbers
async def config_list_phone_numbers(
    instance_id: str,
    max_results: int = 100,
    region: str | None = None
) -> dict:
    """List phone numbers for an instance."""
    client = _get_client(region)
    # First get instance ARN, then list phone numbers
    instance_info = client.describe_instance(InstanceId=instance_id)
    instance_arn = instance_info["Instance"]["Arn"]
    return client.list_phone_numbers_v2(TargetArn=instance_arn, MaxResults=max_results)


# Routing Profiles
async def config_list_routing_profiles(
    instance_id: str,
    max_results: int = 100,
    region: str | None = None
) -> dict:
    """List routing profiles."""
    client = _get_client(region)
    return client.list_routing_profiles(InstanceId=instance_id, MaxResults=max_results)


async def config_create_routing_profile(
    name: str,
    default_outbound_queue_id: str,
    description: str = "",
    media_concurrencies: list[dict] | None = None,
    instance_id: str | None = None,
    region: str | None = None
) -> dict:
    """Create a routing profile."""
    client = _get_client(region)
    effective_instance_id = _get_instance(instance_id)
    concurrencies = media_concurrencies or [
        {"Channel": "VOICE", "Concurrency": 1},
        {"Channel": "CHAT", "Concurrency": 2},
    ]
    return client.create_routing_profile(
        InstanceId=effective_instance_id,
        Name=name,
        DefaultOutboundQueueId=default_outbound_queue_id,
        Description=description,
        MediaConcurrencies=concurrencies,
    )


# Hours of Operation
async def config_list_hours_of_operations(
    instance_id: str,
    max_results: int = 100,
    region: str | None = None
) -> dict:
    """List hours of operation."""
    client = _get_client(region)
    return client.list_hours_of_operations(InstanceId=instance_id, MaxResults=max_results)


async def config_create_hours_of_operation(
    name: str,
    time_zone: str,
    config: list[dict],
    instance_id: str | None = None,
    region: str | None = None
) -> dict:
    """Create hours of operation."""
    client = _get_client(region)
    effective_instance_id = _get_instance(instance_id)
    return client.create_hours_of_operation(
        InstanceId=effective_instance_id,
        Name=name,
        TimeZone=time_zone,
        Config=config,
    )


# Users
async def config_list_users(
    instance_id: str,
    max_results: int = 100,
    region: str | None = None
) -> dict:
    """List users."""
    client = _get_client(region)
    return client.list_users(InstanceId=instance_id, MaxResults=max_results)


async def config_list_security_profiles(
    instance_id: str,
    max_results: int = 100,
    region: str | None = None
) -> dict:
    """List security profiles."""
    client = _get_client(region)
    return client.list_security_profiles(InstanceId=instance_id, MaxResults=max_results)


async def config_describe_user(
    instance_id: str,
    user_id: str,
    region: str | None = None
) -> dict:
    """Get user details."""
    client = _get_client(region)
    return client.describe_user(InstanceId=instance_id, UserId=user_id)


async def config_create_user(
    instance_id: str,
    username: str,
    routing_profile_id: str,
    security_profile_ids: list[str],
    first_name: str = "Agent",
    last_name: str = "User",
    password: str | None = None,
    phone_type: str = "SOFT_PHONE",
    region: str | None = None
) -> dict:
    """Create a user."""
    client = _get_client(region)
    params = {
        "InstanceId": instance_id,
        "Username": username,
        "IdentityInfo": {"FirstName": first_name, "LastName": last_name},
        "RoutingProfileId": routing_profile_id,
        "SecurityProfileIds": security_profile_ids,
        "PhoneConfig": {"PhoneType": phone_type},
    }
    if password:
        params["Password"] = password
    return client.create_user(**params)


async def config_update_user_routing_profile(
    instance_id: str,
    user_id: str,
    routing_profile_id: str,
    region: str | None = None
) -> dict:
    """Update user's routing profile."""
    client = _get_client(region)
    return client.update_user_routing_profile(
        InstanceId=instance_id,
        UserId=user_id,
        RoutingProfileId=routing_profile_id,
    )


# Agent Status
async def config_list_agent_statuses(
    instance_id: str,
    max_results: int = 100,
    region: str | None = None
) -> dict:
    """List agent statuses."""
    client = _get_client(region)
    return client.list_agent_statuses(InstanceId=instance_id, MaxResults=max_results)


async def config_put_user_status(
    instance_id: str,
    user_id: str,
    agent_status_id: str,
    region: str | None = None
) -> dict:
    """Set agent's current status."""
    client = _get_client(region)
    return client.put_user_status(
        InstanceId=instance_id,
        UserId=user_id,
        AgentStatusId=agent_status_id,
    )
