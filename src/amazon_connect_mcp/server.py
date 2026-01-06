"""Amazon Connect MCP Server."""
from fastmcp import FastMCP

from .tools import core, cases, contacts, config, analytics, profiles, campaigns, ai, wizard
from .tools.visualizer import open_visualizer

mcp = FastMCP(
    "amazon-connect-mcp",
    instructions="""Amazon Connect MCP Server - AI assistant for contact center operations.

TIER 1 (Core - use these first):
- describe_instance, list_instances, list_queues
- get_current_metrics
- search_contacts, describe_contact
- create_case, get_case, search_cases

TIER 2 (Search for these when needed):
- cases_* : Case templates, fields, layouts, domains
- contacts_* : Voice, chat, tasks, transfers, recording
- config_* : Flows, queues, routing, users, agent status
- analytics_* : Metrics, evaluations
- profiles_* : Customer profiles
- campaigns_* : Outbound campaigns
- ai_* : Amazon Q in Connect

QUICK ACCESS:
- qic_search: Use when user says "QiC", "Q in Connect", or wants to search Connect knowledge base

WIZARD & TEMPLATES:
- template_list, template_get, template_customize
- wizard_start_setup, wizard_get_iac_template
"""
)

# ============================================
# TIER 1: Core Tools (Always Loaded)
# ============================================

mcp.tool()(core.describe_instance)
mcp.tool()(core.create_instance)
mcp.tool()(core.delete_instance)
mcp.tool()(core.list_instances)
mcp.tool()(core.list_queues)
mcp.tool()(core.get_current_metrics)
mcp.tool()(core.search_contacts)
mcp.tool()(core.describe_contact)
mcp.tool()(core.create_case)
mcp.tool()(core.get_case)
mcp.tool()(core.search_cases)
mcp.tool()(core.list_domains_for_instance)

# ============================================
# TIER 2: Domain Tools
# ============================================

# Cases
mcp.tool()(cases.cases_create_template)
mcp.tool()(cases.cases_list_templates)
mcp.tool()(cases.cases_get_template)
mcp.tool()(cases.cases_update_template)
mcp.tool()(cases.cases_create_field)
mcp.tool()(cases.cases_list_fields)
mcp.tool()(cases.cases_update_field)
mcp.tool()(cases.cases_create_layout)
mcp.tool()(cases.cases_list_layouts)
mcp.tool()(cases.cases_update_case)
mcp.tool()(cases.cases_delete_case)
mcp.tool()(cases.cases_create_related_item)
mcp.tool()(cases.cases_list_cases_for_contact)
mcp.tool()(cases.cases_create_domain)
mcp.tool()(cases.cases_list_domains)
mcp.tool()(cases.cases_get_domain)
mcp.tool()(cases.cases_associate_domain)

# Contacts
mcp.tool()(contacts.contacts_start_outbound_voice)
mcp.tool()(contacts.contacts_start_chat)
mcp.tool()(contacts.contacts_start_task)
mcp.tool()(contacts.contacts_stop)
mcp.tool()(contacts.contacts_transfer)
mcp.tool()(contacts.contacts_update_attributes)
mcp.tool()(contacts.contacts_start_recording)
mcp.tool()(contacts.contacts_stop_recording)

# Config - Session Management
mcp.tool()(config.set_session)
mcp.tool()(config.get_session)
mcp.tool()(config.clear_session)

# Config
mcp.tool()(config.config_list_contact_flows)
mcp.tool()(config.config_describe_contact_flow)
mcp.tool()(config.config_create_contact_flow)
mcp.tool()(config.config_update_contact_flow_content)
mcp.tool()(config.config_create_queue)
mcp.tool()(config.config_describe_queue)
mcp.tool()(config.config_update_queue_status)
mcp.tool()(config.config_list_phone_numbers)
mcp.tool()(config.config_list_routing_profiles)
mcp.tool()(config.config_create_routing_profile)
mcp.tool()(config.config_list_hours_of_operations)
mcp.tool()(config.config_create_hours_of_operation)
mcp.tool()(config.config_list_users)
mcp.tool()(config.config_list_security_profiles)
mcp.tool()(config.config_describe_user)
mcp.tool()(config.config_create_user)
mcp.tool()(config.config_update_user_routing_profile)
mcp.tool()(config.config_list_agent_statuses)
mcp.tool()(config.config_put_user_status)

# Analytics
mcp.tool()(analytics.analytics_get_metric_data)
mcp.tool()(analytics.analytics_get_current_user_data)
mcp.tool()(analytics.analytics_list_contact_evaluations)
mcp.tool()(analytics.analytics_start_contact_evaluation)
mcp.tool()(analytics.analytics_list_evaluation_forms)

# Profiles
mcp.tool()(profiles.profiles_create_profile)
mcp.tool()(profiles.profiles_search)
mcp.tool()(profiles.profiles_get_profile)
mcp.tool()(profiles.profiles_update_profile)
mcp.tool()(profiles.profiles_delete_profile)
mcp.tool()(profiles.profiles_merge)
mcp.tool()(profiles.profiles_list_domains)
mcp.tool()(profiles.profiles_create_domain)
mcp.tool()(profiles.profiles_associate_domain)

# Campaigns
mcp.tool()(campaigns.campaigns_create)
mcp.tool()(campaigns.campaigns_list)
mcp.tool()(campaigns.campaigns_describe)
mcp.tool()(campaigns.campaigns_start)
mcp.tool()(campaigns.campaigns_pause)
mcp.tool()(campaigns.campaigns_resume)
mcp.tool()(campaigns.campaigns_stop)
mcp.tool()(campaigns.campaigns_delete)
mcp.tool()(campaigns.campaigns_get_state)
mcp.tool()(campaigns.campaigns_put_outbound_requests)
mcp.tool()(campaigns.campaigns_start_onboarding)
mcp.tool()(campaigns.campaigns_get_onboarding_status)
mcp.tool()(campaigns.campaigns_delete_onboarding)

# AI (Amazon Q in Connect)
mcp.tool()(ai.ai_list_assistants)
mcp.tool()(ai.ai_query_assistant)
mcp.tool()(ai.ai_list_knowledge_bases)
mcp.tool()(ai.ai_search_content)
mcp.tool()(ai.ai_get_recommendations)
mcp.tool()(ai.ai_create_session)
mcp.tool()(ai.ai_list_quick_responses)
mcp.tool()(ai.ai_search_quick_responses)
mcp.tool()(ai.qic_search)

# ============================================
# WIZARD & TEMPLATES
# ============================================
wizard.register_wizard_tools(mcp)


# ============================================
# VISUALIZER
# ============================================
@mcp.tool()
async def layout_visualizer() -> dict:
    """Launch the Cases Layout Visualizer in your browser.
    
    Opens a drag-and-drop interface to:
    - Select industry templates (retail, healthcare, etc.)
    - Drag fields into Top Panel (always visible) or More Info (tabbed)
    - Reorder fields by dragging within panels
    - See generated JSON layout code in real-time
    - Copy the JSON for use with cases_create_layout
    """
    filepath = open_visualizer()
    return {
        "status": "opened",
        "file": filepath,
        "instructions": [
            "1. Select an industry template from the dropdown",
            "2. Drag fields to Top Panel or More Info section",
            "3. Drag fields within a panel to reorder them",
            "4. Copy the generated JSON",
            "5. Use with cases_create_layout(domain_id, name, content)"
        ]
    }


def main():
    mcp.run()


if __name__ == "__main__":
    main()
