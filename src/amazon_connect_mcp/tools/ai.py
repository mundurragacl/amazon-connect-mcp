"""Tier 2: Amazon Q in Connect (AI) tools - Defer loaded."""
from ..aws_clients import get_wisdom_client
from .config import _session_context


def _get_session_region():
    return _session_context.get("region")


async def ai_list_assistants() -> dict:
    """List Amazon Q assistants."""
    client = get_wisdom_client(_get_session_region())
    return client.list_assistants()


async def ai_query_assistant(
    assistant_id: str,
    query_text: str,
    max_results: int = 10
) -> dict:
    """Query an assistant for recommendations."""
    client = get_wisdom_client(_get_session_region())
    return client.query_assistant(
        assistantId=assistant_id,
        queryText=query_text,
        maxResults=max_results,
    )


async def ai_list_knowledge_bases(assistant_id: str) -> dict:
    """List knowledge bases for an assistant."""
    client = get_wisdom_client(_get_session_region())
    return client.list_knowledge_bases()


async def ai_search_content(
    knowledge_base_id: str,
    search_expression: str,
    max_results: int = 10
) -> dict:
    """Search content in a knowledge base by exact name match."""
    client = get_wisdom_client(_get_session_region())
    # Note: Only EQUALS operator is supported for NAME field
    return client.search_content(
        knowledgeBaseId=knowledge_base_id,
        searchExpression={
            "filters": [{
                "field": "NAME",
                "operator": "EQUALS",
                "value": search_expression
            }]
        },
        maxResults=max_results,
    )


async def ai_get_recommendations(
    assistant_id: str,
    session_id: str,
    max_results: int = 5
) -> dict:
    """Get AI recommendations for a session."""
    client = get_wisdom_client(_get_session_region())
    return client.get_recommendations(
        assistantId=assistant_id,
        sessionId=session_id,
        maxResults=max_results,
    )


async def ai_create_session(
    assistant_id: str,
    name: str
) -> dict:
    """Create an AI session."""
    client = get_wisdom_client(_get_session_region())
    return client.create_session(assistantId=assistant_id, name=name)


async def ai_list_quick_responses(knowledge_base_id: str, max_results: int = 25) -> dict:
    """List quick responses."""
    client = get_wisdom_client(_get_session_region())
    return client.list_quick_responses(knowledgeBaseId=knowledge_base_id, maxResults=max_results)


async def ai_search_quick_responses(
    knowledge_base_id: str,
    query_text: str,
    max_results: int = 10
) -> dict:
    """Search quick responses."""
    client = get_wisdom_client(_get_session_region())
    return client.search_quick_responses(
        knowledgeBaseId=knowledge_base_id,
        searchExpression={
            "queries": [{
                "name": "content",
                "operator": "CONTAINS",
                "values": [query_text]
            }]
        },
        maxResults=max_results,
    )
