"""Tier 2: Analytics tools - Defer loaded."""
from ..aws_clients import get_connect_client
from .config import _session_context


def _get_session_region():
    return _session_context.get("region")


async def analytics_get_metric_data(
    instance_id: str,
    start_time: str,
    end_time: str,
    queue_ids: list[str] | None = None,
    metrics: list[str] | None = None
) -> dict:
    """Get historical metrics (ISO 8601 timestamps)."""
    client = get_connect_client(_get_session_region())
    region = _get_session_region() or "us-east-1"
    
    # Build filters - Queues filter is required
    filters = {"FilterKey": "QUEUE", "FilterValues": queue_ids or []}
    
    # If no queue_ids provided, get all queues first
    if not queue_ids:
        queues_response = client.list_queues(InstanceId=instance_id, QueueTypes=["STANDARD"])
        queue_ids = [q["Id"] for q in queues_response.get("QueueSummaryList", [])]
        filters["FilterValues"] = queue_ids
    
    if not filters["FilterValues"]:
        return {"error": "No queues found", "MetricResults": []}
    
    metric_list = metrics or [
        "CONTACTS_QUEUED",
        "CONTACTS_HANDLED",
        "CONTACTS_ABANDONED",
        "AVG_HANDLE_TIME",
    ]
    
    # Get instance ARN for proper resource reference
    instance_info = client.describe_instance(InstanceId=instance_id)
    instance_arn = instance_info["Instance"]["Arn"]
    
    return client.get_metric_data_v2(
        ResourceArn=instance_arn,
        StartTime=start_time,
        EndTime=end_time,
        Filters=[filters],
        Metrics=[{"Name": m} for m in metric_list],
    )


async def analytics_get_current_user_data(
    instance_id: str,
    queue_ids: list[str] | None = None
) -> dict:
    """Get real-time agent data."""
    client = get_connect_client(_get_session_region())
    filters = {}
    if queue_ids:
        filters["Queues"] = queue_ids
    return client.get_current_user_data(InstanceId=instance_id, Filters=filters)


async def analytics_list_contact_evaluations(
    instance_id: str,
    contact_id: str
) -> dict:
    """List evaluations for a contact."""
    client = get_connect_client(_get_session_region())
    return client.list_contact_evaluations(InstanceId=instance_id, ContactId=contact_id)


async def analytics_start_contact_evaluation(
    instance_id: str,
    contact_id: str,
    evaluation_form_id: str
) -> dict:
    """Start an evaluation for a contact."""
    client = get_connect_client(_get_session_region())
    return client.start_contact_evaluation(
        InstanceId=instance_id,
        ContactId=contact_id,
        EvaluationFormId=evaluation_form_id,
    )


async def analytics_list_evaluation_forms(instance_id: str, max_results: int = 25) -> dict:
    """List evaluation forms."""
    client = get_connect_client(_get_session_region())
    return client.list_evaluation_forms(InstanceId=instance_id, MaxResults=max_results)
