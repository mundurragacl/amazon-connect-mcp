"""Tier 1: Core tools - Always loaded."""
from fastmcp import Context
from ..aws_clients import get_connect_client, get_cases_client, get_instance_region

# Import session context from config module
from .config import _session_context


def _get_session_region():
    """Get region from session context."""
    return _session_context.get("region")


def _get_session_instance():
    """Get instance_id from session context."""
    return _session_context.get("instance_id")


# Instance & Configuration
async def describe_instance(instance_id: str) -> dict:
    """Get Amazon Connect instance details."""
    region = get_instance_region(instance_id)
    client = get_connect_client(region)
    result = client.describe_instance(InstanceId=instance_id)
    # Add region info to the result
    result['Instance']['Region'] = region
    return result


async def create_instance(
    instance_alias: str,
    identity_management_type: str = "CONNECT_MANAGED",
    inbound_calls_enabled: bool = True,
    outbound_calls_enabled: bool = True,
    region: str = "us-east-1"
) -> dict:
    """Create a new Amazon Connect instance.
    
    Args:
        instance_alias: Unique name for the instance
        identity_management_type: SAML, CONNECT_MANAGED, or EXISTING_DIRECTORY
        inbound_calls_enabled: Enable inbound calls
        outbound_calls_enabled: Enable outbound calls
        region: AWS region for the instance
    """
    client = get_connect_client(region)
    return client.create_instance(
        InstanceAlias=instance_alias,
        IdentityManagementType=identity_management_type,
        InboundCallsEnabled=inbound_calls_enabled,
        OutboundCallsEnabled=outbound_calls_enabled
    )


async def delete_instance(
    instance_id: str,
    confirm: bool = False
) -> dict:
    """Delete an Amazon Connect instance. THIS ACTION IS PERMANENT.
    
    Args:
        instance_id: The ID of the instance to delete
        confirm: Must be True to proceed. Set to False to get a confirmation prompt.
    
    Returns:
        Confirmation message or deletion result
    """
    if not confirm:
        return {
            "status": "CONFIRMATION_REQUIRED",
            "message": "⚠️ WARNING: Deleting an Amazon Connect instance is PERMANENT and cannot be undone. "
                       "All data including contact flows, queues, users, and historical data will be lost. "
                       "To proceed, call delete_instance again with confirm=True",
            "instance_id": instance_id
        }
    
    region = get_instance_region(instance_id)
    client = get_connect_client(region)
    client.delete_instance(InstanceId=instance_id)
    return {
        "status": "DELETED",
        "message": f"Instance {instance_id} has been permanently deleted",
        "instance_id": instance_id
    }


async def list_instances(region: str | None = None) -> dict:
    """List all Amazon Connect instances. If no region specified, lists across all regions."""
    if region:
        client = get_connect_client(region)
        result = client.list_instances()
        for inst in result.get('InstanceSummaryList', []):
            inst['Region'] = region
        instances = result.get('InstanceSummaryList', [])
    else:
        # List across all Connect-supported regions
        regions = ['us-east-1', 'us-west-2', 'eu-west-2', 'eu-central-1', 'ap-southeast-1', 
                   'ap-southeast-2', 'ap-northeast-1', 'ap-northeast-2', 'ca-central-1', 'af-south-1']
        
        instances = []
        for r in regions:
            try:
                client = get_connect_client(r)
                result = client.list_instances()
                for inst in result.get('InstanceSummaryList', []):
                    inst['Region'] = r
                    instances.append(inst)
            except Exception:
                pass
    
    return {
        'InstanceSummaryList': instances,
        '_llm_guidance': {
            'nextStep': 'Ask user which instance to work with, then call set_session',
            'action': {
                'tool': 'set_session',
                'params': {
                    'instance_id': '<selected_instance_Id>',
                    'region': '<selected_instance_Region>'
                }
            },
            'note': 'Setting session ensures all subsequent operations use correct region'
        }
    }


async def list_queues(instance_id: str, max_results: int = 100) -> dict:
    """List queues in an Amazon Connect instance."""
    region = _get_session_region() or get_instance_region(instance_id)
    client = get_connect_client(region)
    return client.list_queues(InstanceId=instance_id, MaxResults=max_results)


# Real-time Metrics
async def get_current_metrics(
    instance_id: str,
    queue_ids: list[str] | None = None,
    channel: str = "VOICE"
) -> dict:
    """Get real-time metrics for queues and agents. If no queue_ids provided, fetches all queues first."""
    region = _get_session_region() or get_instance_region(instance_id)
    client = get_connect_client(region)
    
    # If no queues specified, get all queues
    if not queue_ids:
        queues_resp = client.list_queues(InstanceId=instance_id, MaxResults=100)
        queue_ids = [q['Id'] for q in queues_resp.get('QueueSummaryList', [])]
    
    if not queue_ids:
        return {"MetricResults": [], "message": "No queues found"}
    
    return client.get_current_metric_data(
        InstanceId=instance_id,
        Filters={"Queues": queue_ids, "Channels": [channel]},
        CurrentMetrics=[
            {"Name": "AGENTS_AVAILABLE", "Unit": "COUNT"},
            {"Name": "AGENTS_ONLINE", "Unit": "COUNT"},
            {"Name": "CONTACTS_IN_QUEUE", "Unit": "COUNT"},
            {"Name": "OLDEST_CONTACT_AGE", "Unit": "SECONDS"},
        ],
    )


# Contact Operations
async def search_contacts(
    instance_id: str,
    time_range_start: str,
    time_range_end: str,
    max_results: int = 100
) -> dict:
    """Search contacts within a time range (ISO 8601 format)."""
    region = _get_session_region() or get_instance_region(instance_id)
    client = get_connect_client(region)
    return client.search_contacts(
        InstanceId=instance_id,
        TimeRange={
            "Type": "INITIATION_TIMESTAMP",
            "StartTime": time_range_start,
            "EndTime": time_range_end,
        },
        MaxResults=max_results,
    )


async def describe_contact(instance_id: str, contact_id: str) -> dict:
    """Get details of a specific contact."""
    region = _get_session_region() or get_instance_region(instance_id)
    client = get_connect_client(region)
    return client.describe_contact(InstanceId=instance_id, ContactId=contact_id)


# Cases - Core Operations
async def create_case(
    domain_id: str,
    template_id: str,
    fields: dict[str, str],
    region: str | None = None
) -> dict:
    """Create a new case."""
    effective_region = region or _get_session_region()
    client = get_cases_client(effective_region)
    return client.create_case(
        domainId=domain_id,
        templateId=template_id,
        fields=[{"id": k, "value": {"stringValue": v}} for k, v in fields.items()],
    )


async def get_case(domain_id: str, case_id: str, region: str | None = None) -> dict:
    """Get case details."""
    effective_region = region or _get_session_region()
    client = get_cases_client(effective_region)
    return client.get_case(domainId=domain_id, caseId=case_id, fields=[{"id": "title"}])


async def search_cases(
    domain_id: str,
    filter_field: str | None = None,
    filter_value: str | None = None,
    max_results: int = 25,
    region: str | None = None
) -> dict:
    """Search cases in a domain."""
    effective_region = region or _get_session_region()
    client = get_cases_client(effective_region)
    params = {"domainId": domain_id, "maxResults": max_results}
    if filter_field and filter_value:
        params["filter"] = {
            "field": {"id": filter_field, "value": {"stringValue": filter_value}}
        }
    return client.search_cases(**params)


async def list_domains_for_instance(instance_id: str, max_results: int = 10) -> dict:
    """List case domains for a specific Connect instance."""
    region = _get_session_region() or get_instance_region(instance_id)
    client = get_cases_client(region)
    return client.list_domains(maxResults=min(max_results, 10))
