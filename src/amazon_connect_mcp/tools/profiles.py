"""Tier 2: Customer Profiles tools - Defer loaded."""
from ..aws_clients import get_profiles_client, get_connect_client
from .config import _session_context


def _get_session_region():
    return _session_context.get("region")


def _get_session_instance():
    return _session_context.get("instance_id")


async def profiles_create_profile(
    domain_name: str,
    first_name: str | None = None,
    last_name: str | None = None,
    email: str | None = None,
    phone: str | None = None,
    attributes: dict[str, str] | None = None
) -> dict:
    """Create a customer profile."""
    client = get_profiles_client(_get_session_region())
    params = {"DomainName": domain_name}
    if first_name:
        params["FirstName"] = first_name
    if last_name:
        params["LastName"] = last_name
    if email:
        params["EmailAddress"] = email
    if phone:
        params["PhoneNumber"] = phone
    if attributes:
        params["Attributes"] = attributes
    return client.create_profile(**params)


async def profiles_search(
    domain_name: str,
    key_name: str,
    values: list[str],
    max_results: int = 25
) -> dict:
    """Search profiles by key (e.g., _email, _phone, _account)."""
    client = get_profiles_client(_get_session_region())
    return client.search_profiles(
        DomainName=domain_name,
        KeyName=key_name,
        Values=values,
        MaxResults=max_results,
    )


async def profiles_get_profile(domain_name: str, profile_id: str) -> dict:
    """Get profile details."""
    client = get_profiles_client(_get_session_region())
    response = client.batch_get_profile(DomainName=domain_name, ProfileIds=[profile_id])
    if response.get("Profiles"):
        return response["Profiles"][0]
    return {"error": "Profile not found", "ProfileId": profile_id}


async def profiles_update_profile(
    domain_name: str,
    profile_id: str,
    first_name: str | None = None,
    last_name: str | None = None,
    email: str | None = None,
    phone: str | None = None,
    attributes: dict[str, str] | None = None
) -> dict:
    """Update a customer profile."""
    client = get_profiles_client(_get_session_region())
    params = {"DomainName": domain_name, "ProfileId": profile_id}
    if first_name:
        params["FirstName"] = first_name
    if last_name:
        params["LastName"] = last_name
    if email:
        params["EmailAddress"] = email
    if phone:
        params["PhoneNumber"] = phone
    if attributes:
        params["Attributes"] = attributes
    return client.update_profile(**params)


async def profiles_delete_profile(domain_name: str, profile_id: str) -> dict:
    """Delete a customer profile."""
    client = get_profiles_client(_get_session_region())
    return client.delete_profile(DomainName=domain_name, ProfileId=profile_id)


async def profiles_merge(
    domain_name: str,
    main_profile_id: str,
    profile_ids_to_merge: list[str]
) -> dict:
    """Merge duplicate profiles."""
    client = get_profiles_client(_get_session_region())
    return client.merge_profiles(
        DomainName=domain_name,
        MainProfileId=main_profile_id,
        ProfileIdsToBeMerged=profile_ids_to_merge,
    )


async def profiles_list_domains(max_results: int = 25) -> dict:
    """List profile domains."""
    client = get_profiles_client(_get_session_region())
    return client.list_domains(MaxResults=max_results)


async def profiles_create_domain(
    domain_name: str,
    default_expiration_days: int = 365
) -> dict:
    """Create a profile domain."""
    client = get_profiles_client(_get_session_region())
    result = client.create_domain(
        DomainName=domain_name,
        DefaultExpirationDays=default_expiration_days,
    )
    result["_llm_guidance"] = {
        "nextSteps": [
            "1. Associate this domain with your Connect instance using profiles_associate_domain",
            "2. Then associate Cases domain using cases_associate_domain (requires profiles first)"
        ],
        "workflow": {
            "step1": {"tool": "profiles_associate_domain", "params": {"domain_name": domain_name}},
            "step2": {"tool": "cases_associate_domain", "note": "Do this AFTER profiles association"}
        },
        "CRITICAL": "Cases integration requires Customer Profiles to be associated FIRST"
    }
    return result


async def profiles_associate_domain(
    domain_name: str,
    instance_id: str | None = None,
    object_type_name: str = "CTR"
) -> dict:
    """Associate a Customer Profiles domain with a Connect instance.
    
    This enables Customer Profiles for the instance, allowing contact data
    to flow into customer profiles automatically.
    
    Args:
        domain_name: The Customer Profiles domain name to associate
        instance_id: Connect instance ID (uses session if not provided)
        object_type_name: Object type for the integration (default: CTR for Contact Trace Records)
    
    Returns:
        Integration details including domain, URI, and creation time
    
    IMPORTANT: This must be done BEFORE associating Cases domain.
    The correct order is:
    1. Create profiles domain (profiles_create_domain)
    2. Associate profiles domain (this tool)
    3. Create cases domain (cases_create_domain)  
    4. Associate cases domain (cases_associate_domain)
    """
    region = _get_session_region()
    effective_instance_id = instance_id or _get_session_instance()
    
    if not effective_instance_id:
        return {
            "error": "No instance_id provided and no session set",
            "action": "Call set_session(instance_id, region) first or provide instance_id parameter"
        }
    
    if not region:
        return {
            "error": "No region set in session",
            "action": "Call set_session(instance_id, region) first"
        }
    
    # Get the instance ARN
    connect_client = get_connect_client(region)
    instance_info = connect_client.describe_instance(InstanceId=effective_instance_id)
    instance_arn = instance_info["Instance"]["Arn"]
    
    # Create the integration
    profiles_client = get_profiles_client(region)
    result = profiles_client.put_integration(
        DomainName=domain_name,
        Uri=instance_arn,
        ObjectTypeName=object_type_name
    )
    
    result["_llm_guidance"] = {
        "status": "Customer Profiles domain associated successfully",
        "nextStep": {
            "description": "Now you can associate a Cases domain",
            "tool": "cases_associate_domain",
            "note": "Cases requires Customer Profiles to be associated first"
        },
        "whatThisDoes": f"Contact data (CTR) from instance will now flow into {domain_name} profiles"
    }
    
    return result
