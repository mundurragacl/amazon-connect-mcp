"""Tier 2: Customer Profiles tools - Defer loaded."""
from ..aws_clients import get_profiles_client
from .config import _session_context


def _get_session_region():
    return _session_context.get("region")


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
    return client.create_domain(
        DomainName=domain_name,
        DefaultExpirationDays=default_expiration_days,
    )
