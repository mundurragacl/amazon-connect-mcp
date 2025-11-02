"""Tier 1: Core tools - Always loaded."""
from fastmcp import Context
from ..aws_clients import get_connect_client, get_cases_client


# Instance & Configuration
async def describe_instance(instance_id: str) -> dict:
    """Get Amazon Connect instance details."""
    client = get_connect_client()
    return client.describe_instance(InstanceId=instance_id)


async def list_instances(region: str | None = None) -> dict:
    """List all Amazon Connect instances. If no region specified, lists across all regions."""
    if region:
        client = get_connect_client(region)
        result = client.list_instances()
        for inst in result.get('InstanceSummaryList', []):
            inst['Region'] = region
        return result
    
    # List across all Connect-supported regions
    regions = ['us-east-1', 'us-west-2', 'eu-west-2', 'eu-central-1', 'ap-southeast-1', 
               'ap-southeast-2', 'ap-northeast-1', 'ap-northeast-2', 'ca-central-1', 'af-south-1']
    
    all_instances = []
    for r in regions:
        try:
            client = get_connect_client(r)
            result = client.list_instances()
            for inst in result.get('InstanceSummaryList', []):
                inst['Region'] = r
                all_instances.append(inst)
        except Exception:
            pass
    
    return {'InstanceSummaryList': all_instances}


async def list_queues(instance_id: str, max_results: int = 100) -> dict:
    """List queues in an Amazon Connect instance."""
    client = get_connect_client()
    return client.list_queues(InstanceId=instance_id, MaxResults=max_results)


# Real-time Metrics
async def get_current_metrics(
    instance_id: str,
    queue_ids: list[str] | None = None,
    channel: str = "VOICE"
) -> dict:
    """Get real-time metrics for queues and agents. If no queue_ids provided, fetches all queues first."""
    client = get_connect_client()
    
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
    client = get_connect_client()
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
    client = get_connect_client()
    return client.describe_contact(InstanceId=instance_id, ContactId=contact_id)


# Cases - Core Operations
async def create_case(
    domain_id: str,
    template_id: str,
    fields: dict[str, str]
) -> dict:
    """Create a new case."""
    client = get_cases_client()
    return client.create_case(
        domainId=domain_id,
        templateId=template_id,
        fields=[{"id": k, "value": {"stringValue": v}} for k, v in fields.items()],
    )


async def get_case(domain_id: str, case_id: str) -> dict:
    """Get case details."""
    client = get_cases_client()
    return client.get_case(domainId=domain_id, caseId=case_id, fields=[{"id": "title"}])


async def search_cases(
    domain_id: str,
    filter_field: str | None = None,
    filter_value: str | None = None,
    max_results: int = 25
) -> dict:
    """Search cases in a domain."""
    client = get_cases_client()
    params = {"domainId": domain_id, "maxResults": max_results}
    if filter_field and filter_value:
        params["filter"] = {
            "field": {"id": filter_field, "value": {"stringValue": filter_value}}
        }
    return client.search_cases(**params)
