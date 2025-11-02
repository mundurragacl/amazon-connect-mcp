"""Tier 2: Analytics tools - Defer loaded."""
from ..aws_clients import get_connect_client


async def analytics_get_metric_data(
    instance_id: str,
    start_time: str,
    end_time: str,
    queue_ids: list[str] | None = None,
    metrics: list[str] | None = None
) -> dict:
    """Get historical metrics (ISO 8601 timestamps)."""
    client = get_connect_client()
    filters = {}
    if queue_ids:
        filters["Queues"] = queue_ids
    
    metric_list = metrics or [
        "CONTACTS_QUEUED",
        "CONTACTS_HANDLED",
        "CONTACTS_ABANDONED",
        "AVG_HANDLE_TIME",
    ]
    
    return client.get_metric_data_v2(
        ResourceArn=f"arn:aws:connect:*:*:instance/{instance_id}",
        StartTime=start_time,
        EndTime=end_time,
        Filters=[filters] if filters else [],
        Metrics=[{"Name": m} for m in metric_list],
    )


async def analytics_get_current_user_data(
    instance_id: str,
    queue_ids: list[str] | None = None
) -> dict:
    """Get real-time agent data."""
    client = get_connect_client()
    filters = {}
    if queue_ids:
        filters["Queues"] = queue_ids
    return client.get_current_user_data(InstanceId=instance_id, Filters=filters)


async def analytics_list_contact_evaluations(
    instance_id: str,
    contact_id: str
) -> dict:
    """List evaluations for a contact."""
    client = get_connect_client()
    return client.list_contact_evaluations(InstanceId=instance_id, ContactId=contact_id)


async def analytics_start_contact_evaluation(
    instance_id: str,
    contact_id: str,
    evaluation_form_id: str
) -> dict:
    """Start an evaluation for a contact."""
    client = get_connect_client()
    return client.start_contact_evaluation(
        InstanceId=instance_id,
        ContactId=contact_id,
        EvaluationFormId=evaluation_form_id,
    )


async def analytics_list_evaluation_forms(instance_id: str, max_results: int = 25) -> dict:
    """List evaluation forms."""
    client = get_connect_client()
    return client.list_evaluation_forms(InstanceId=instance_id, MaxResults=max_results)
