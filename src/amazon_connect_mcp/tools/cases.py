"""Tier 2: Cases tools - Defer loaded."""
from ..aws_clients import get_cases_client
from .config import _session_context


def _get_session_region():
    return _session_context.get("region")


# Case Templates
async def cases_create_template(
    domain_id: str,
    name: str,
    description: str = "",
    required_fields: list[str] | None = None
) -> dict:
    """Create a case template."""
    client = get_cases_client(_get_session_region())
    params = {"domainId": domain_id, "name": name, "description": description}
    if required_fields:
        params["requiredFields"] = [{"fieldId": f} for f in required_fields]
    return client.create_template(**params)


async def cases_list_templates(domain_id: str, max_results: int = 25) -> dict:
    """List case templates."""
    client = get_cases_client(_get_session_region())
    return client.list_templates(domainId=domain_id, maxResults=max_results)


async def cases_get_template(domain_id: str, template_id: str) -> dict:
    """Get case template details."""
    client = get_cases_client(_get_session_region())
    return client.get_template(domainId=domain_id, templateId=template_id)


async def cases_update_template(
    domain_id: str,
    template_id: str,
    name: str | None = None,
    description: str | None = None
) -> dict:
    """Update a case template."""
    client = get_cases_client(_get_session_region())
    params = {"domainId": domain_id, "templateId": template_id}
    if name:
        params["name"] = name
    if description:
        params["description"] = description
    return client.update_template(**params)


# Case Fields
async def cases_create_field(
    domain_id: str,
    name: str,
    field_type: str,
    description: str = ""
) -> dict:
    """Create a custom field. Types: Text, Number, Boolean, DateTime, SingleSelect, Url."""
    client = get_cases_client(_get_session_region())
    return client.create_field(
        domainId=domain_id,
        name=name,
        type=field_type,
        description=description,
    )


async def cases_list_fields(domain_id: str, max_results: int = 25) -> dict:
    """List case fields."""
    client = get_cases_client(_get_session_region())
    return client.list_fields(domainId=domain_id, maxResults=max_results)


async def cases_update_field(
    domain_id: str,
    field_id: str,
    name: str | None = None,
    description: str | None = None
) -> dict:
    """Update a case field."""
    client = get_cases_client(_get_session_region())
    params = {"domainId": domain_id, "fieldId": field_id}
    if name:
        params["name"] = name
    if description:
        params["description"] = description
    return client.update_field(**params)


# Case Layouts
async def cases_create_layout(
    domain_id: str,
    name: str,
    content: dict
) -> dict:
    """Create a case layout.
    
    💡 TIP: Use the `layout_visualizer` tool to design layouts visually with drag-and-drop!
    It generates the correct JSON structure for you.
    """
    client = get_cases_client(_get_session_region())
    result = client.create_layout(domainId=domain_id, name=name, content=content)
    result["_tip"] = "Use `layout_visualizer` tool to design layouts visually with drag-and-drop"
    return result


async def cases_list_layouts(domain_id: str, max_results: int = 25) -> dict:
    """List case layouts.
    
    💡 TIP: Use the `layout_visualizer` tool to design new layouts visually!
    """
    client = get_cases_client(_get_session_region())
    result = client.list_layouts(domainId=domain_id, maxResults=max_results)
    result["_tip"] = "Use `layout_visualizer` tool to design new layouts visually with drag-and-drop"
    return result


# Case Operations
async def cases_update_case(
    domain_id: str,
    case_id: str,
    fields: dict[str, str]
) -> dict:
    """Update case fields (including status, assignment, etc.)."""
    client = get_cases_client(_get_session_region())
    return client.update_case(
        domainId=domain_id,
        caseId=case_id,
        fields=[{"id": k, "value": {"stringValue": v}} for k, v in fields.items()],
    )


async def cases_delete_case(domain_id: str, case_id: str) -> dict:
    """Delete a case."""
    client = get_cases_client(_get_session_region())
    return client.delete_case(domainId=domain_id, caseId=case_id)


async def cases_create_related_item(
    domain_id: str,
    case_id: str,
    item_type: str,
    content: dict
) -> dict:
    """Create a related item (contact, comment) for a case."""
    client = get_cases_client(_get_session_region())
    return client.create_related_item(
        domainId=domain_id,
        caseId=case_id,
        type=item_type,
        content=content,
    )


async def cases_list_cases_for_contact(
    domain_id: str,
    contact_arn: str,
    max_results: int = 25
) -> dict:
    """List cases linked to a contact."""
    client = get_cases_client(_get_session_region())
    params = {
        "domainId": domain_id,
        "contactArn": contact_arn,
    }
    if max_results and max_results != 25:
        params["maxResults"] = max_results
    return client.list_cases_for_contact(**params)


# Case Domains
async def cases_create_domain(name: str) -> dict:
    """Create a case domain."""
    client = get_cases_client(_get_session_region())
    return client.create_domain(name=name)


async def cases_list_domains(max_results: int = 10, region: str | None = None) -> dict:
    """List case domains."""
    client = get_cases_client(region or _get_session_region())
    return client.list_domains(maxResults=min(max_results, 10))


async def cases_get_domain(domain_id: str, region: str | None = None) -> dict:
    """Get case domain details."""
    client = get_cases_client(region or _get_session_region())
    return client.get_domain(domainId=domain_id)
