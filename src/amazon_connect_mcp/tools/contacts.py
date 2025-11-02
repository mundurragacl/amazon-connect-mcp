"""Tier 2: Contact tools - Defer loaded."""
from ..aws_clients import get_connect_client


# Outbound Contacts
async def contacts_start_outbound_voice(
    instance_id: str,
    destination_phone: str,
    contact_flow_id: str,
    source_phone: str,
    attributes: dict[str, str] | None = None
) -> dict:
    """Initiate an outbound voice call."""
    client = get_connect_client()
    params = {
        "InstanceId": instance_id,
        "DestinationPhoneNumber": destination_phone,
        "ContactFlowId": contact_flow_id,
        "SourcePhoneNumber": source_phone,
    }
    if attributes:
        params["Attributes"] = attributes
    return client.start_outbound_voice_contact(**params)


async def contacts_start_chat(
    instance_id: str,
    contact_flow_id: str,
    participant_display_name: str,
    attributes: dict[str, str] | None = None
) -> dict:
    """Start a chat contact."""
    client = get_connect_client()
    params = {
        "InstanceId": instance_id,
        "ContactFlowId": contact_flow_id,
        "ParticipantDetails": {"DisplayName": participant_display_name},
    }
    if attributes:
        params["Attributes"] = attributes
    return client.start_chat_contact(**params)


async def contacts_start_task(
    instance_id: str,
    contact_flow_id: str,
    name: str,
    description: str = "",
    attributes: dict[str, str] | None = None
) -> dict:
    """Create a task contact."""
    client = get_connect_client()
    params = {
        "InstanceId": instance_id,
        "ContactFlowId": contact_flow_id,
        "Name": name,
        "Description": description,
    }
    if attributes:
        params["Attributes"] = attributes
    return client.start_task_contact(**params)


# Contact Management
async def contacts_stop(instance_id: str, contact_id: str) -> dict:
    """End a contact."""
    client = get_connect_client()
    return client.stop_contact(InstanceId=instance_id, ContactId=contact_id)


async def contacts_transfer(
    instance_id: str,
    contact_id: str,
    queue_id: str | None = None,
    user_id: str | None = None
) -> dict:
    """Transfer a contact to a queue or user."""
    client = get_connect_client()
    params = {"InstanceId": instance_id, "ContactId": contact_id}
    if queue_id:
        params["QueueId"] = queue_id
    if user_id:
        params["UserId"] = user_id
    return client.transfer_contact(**params)


async def contacts_update_attributes(
    instance_id: str,
    contact_id: str,
    attributes: dict[str, str]
) -> dict:
    """Update contact attributes."""
    client = get_connect_client()
    return client.update_contact_attributes(
        InstanceId=instance_id,
        InitialContactId=contact_id,
        Attributes=attributes,
    )


# Recording
async def contacts_start_recording(
    instance_id: str,
    contact_id: str,
    voice_recording: bool = True
) -> dict:
    """Start contact recording."""
    client = get_connect_client()
    return client.start_contact_recording(
        InstanceId=instance_id,
        ContactId=contact_id,
        InitialContactId=contact_id,
        VoiceRecordingConfiguration={"VoiceRecordingTrack": "ALL" if voice_recording else "NONE"},
    )


async def contacts_stop_recording(instance_id: str, contact_id: str) -> dict:
    """Stop contact recording."""
    client = get_connect_client()
    return client.stop_contact_recording(
        InstanceId=instance_id,
        ContactId=contact_id,
        InitialContactId=contact_id,
    )
