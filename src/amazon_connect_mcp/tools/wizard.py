"""Wizard and template management tools for Amazon Connect MCP."""

from typing import Any
from ..templates.loader import list_templates, get_template, customize_template


def register_wizard_tools(mcp):
    """Register wizard and template tools with the MCP server."""

    @mcp.tool()
    def template_list(category: str | None = None) -> dict[str, Any]:
        """List available Amazon Connect configuration templates.
        
        Args:
            category: Optional filter by category (cases, views, data_tables, routing, profiles, ai, campaigns, iac)
        
        Returns templates organized by category with name, path, and subcategory.
        """
        templates = list_templates(category)
        
        # Group by category
        grouped = {}
        for t in templates:
            cat = t["category"]
            if cat not in grouped:
                grouped[cat] = []
            grouped[cat].append({
                "name": t["name"],
                "subcategory": t["subcategory"],
                "path": t["path"]
            })
        
        return {
            "total": len(templates),
            "categories": grouped
        }

    @mcp.tool()
    def template_get(category: str, name: str, subcategory: str | None = None) -> dict[str, Any]:
        """Get a specific template by category and name.
        
        Includes LLM guidance for proper usage workflow.
        
        Args:
            category: Template category (cases, views, data_tables, routing, profiles, ai, campaigns, iac)
            name: Template name (without extension)
            subcategory: Optional subcategory (e.g., 'hours_of_operation' for routing)
        
        Returns the full template content with usage guidance.
        """
        try:
            template = get_template(category, name, subcategory)
            return {
                "category": category,
                "name": name,
                "subcategory": subcategory,
                "template": template
            }
        except FileNotFoundError as e:
            return {"error": str(e)}

    @mcp.tool()
    def template_customize(
        category: str,
        name: str,
        overrides: dict[str, Any],
        subcategory: str | None = None
    ) -> dict[str, Any]:
        """Customize a template with specific overrides.
        
        Args:
            category: Template category
            name: Template name
            overrides: Dictionary of values to override in the template
            subcategory: Optional subcategory
        
        Returns the customized template.
        """
        try:
            template = get_template(category, name, subcategory)
            customized = customize_template(template, overrides)
            return {
                "category": category,
                "name": name,
                "customized": True,
                "template": customized
            }
        except FileNotFoundError as e:
            return {"error": str(e)}

    @mcp.tool()
    def template_get_case_workflow(domain_id: str, template_name: str) -> dict[str, Any]:
        """Get the complete workflow for creating a case from a template.
        
        Returns field mappings and step-by-step instructions with actual field IDs
        from the target domain. Use this before creating cases to avoid validation errors.
        
        Args:
            domain_id: The cases domain ID
            template_name: Template name (e.g., 'ecommerce_support', 'healthcare_support')
        
        Returns workflow steps with field ID mappings.
        """
        try:
            template = get_template("cases", template_name)
        except FileNotFoundError:
            return {"error": f"Template '{template_name}' not found"}
        
        workflow = {
            "template_name": template_name,
            "domain_id": domain_id,
            "steps": [
                {
                    "step": 1,
                    "action": "Get existing fields",
                    "tool": "cases_list_fields",
                    "params": {"domain_id": domain_id},
                    "purpose": "Map field names to UUIDs"
                },
                {
                    "step": 2,
                    "action": "Ensure customer profile exists",
                    "tool": "profiles_search or profiles_create_profile",
                    "purpose": "customer_id requires profile ARN format",
                    "arn_format": "arn:aws:profile:{region}:{account}:domains/{domain}/profiles/{id}"
                },
                {
                    "step": 3,
                    "action": "Create case with minimal fields",
                    "tool": "create_case",
                    "params": {
                        "domain_id": domain_id,
                        "template_id": "<get from cases_list_templates>",
                        "fields": {
                            "title": "<case title>",
                            "customer_id": "<profile ARN from step 2>"
                        }
                    },
                    "note": "Start minimal - add other fields via update"
                },
                {
                    "step": 4,
                    "action": "Update case with additional fields",
                    "tool": "cases_update_case",
                    "purpose": "Add custom fields using UUIDs from step 1"
                }
            ],
            "template_fields": template.get("customFields", []),
            "required_for_creation": ["title", "customer_id"],
            "tips": [
                "Use Text fields when possible - SingleSelect requires exact value matches",
                "Skip fields that cause validation errors, update them later",
                "Field IDs are UUIDs for custom fields, strings for system fields"
            ]
        }
        
        return workflow

    @mcp.tool()
    def template_get_routing_workflow(instance_id: str, region: str) -> dict[str, Any]:
        """Get the complete workflow for setting up routing (hours, queues, profiles, flows).
        
        Returns step-by-step instructions with tool calls and dependencies.
        Use this before creating routing configuration to ensure correct order.
        
        Args:
            instance_id: The Connect instance ID
            region: AWS region (e.g., 'us-east-1', 'us-west-2')
        
        Returns workflow steps with exact tool calls.
        """
        return {
            "instance_id": instance_id,
            "region": region,
            "_llm_guidance": {
                "critical": "Execute steps IN ORDER - each step depends on previous step's output",
                "session": "Session will be set automatically in step 1"
            },
            "steps": [
                {
                    "step": 1,
                    "action": "Set session context",
                    "tool": "set_session",
                    "params": {
                        "instance_id": instance_id,
                        "region": region
                    },
                    "purpose": "All subsequent calls will use this instance/region",
                    "output": "Confirmation message"
                },
                {
                    "step": 2,
                    "action": "Create Hours of Operation",
                    "tool": "config_create_hours_of_operation",
                    "params": {
                        "name": "Business Hours",
                        "time_zone": "America/New_York",
                        "config": [
                            {"Day": "MONDAY", "StartTime": {"Hours": 8, "Minutes": 0}, "EndTime": {"Hours": 17, "Minutes": 0}},
                            {"Day": "TUESDAY", "StartTime": {"Hours": 8, "Minutes": 0}, "EndTime": {"Hours": 17, "Minutes": 0}},
                            {"Day": "WEDNESDAY", "StartTime": {"Hours": 8, "Minutes": 0}, "EndTime": {"Hours": 17, "Minutes": 0}},
                            {"Day": "THURSDAY", "StartTime": {"Hours": 8, "Minutes": 0}, "EndTime": {"Hours": 17, "Minutes": 0}},
                            {"Day": "FRIDAY", "StartTime": {"Hours": 8, "Minutes": 0}, "EndTime": {"Hours": 17, "Minutes": 0}}
                        ]
                    },
                    "output": "HoursOfOperationId - SAVE THIS for step 3",
                    "template": "routing/hours_of_operation/business_hours"
                },
                {
                    "step": 3,
                    "action": "Create Queue",
                    "tool": "config_create_queue",
                    "params": {
                        "name": "General Support Queue",
                        "hours_of_operation_id": "<HoursOfOperationId from step 2>",
                        "description": "Main support queue"
                    },
                    "output": "QueueId - SAVE THIS for step 4",
                    "template": "routing/queues/general_support"
                },
                {
                    "step": 4,
                    "action": "Create Routing Profile",
                    "tool": "config_create_routing_profile",
                    "params": {
                        "name": "Support Agent Profile",
                        "default_outbound_queue_id": "<QueueId from step 3>",
                        "description": "Profile for support agents",
                        "media_concurrencies": [
                            {"Channel": "VOICE", "Concurrency": 1},
                            {"Channel": "CHAT", "Concurrency": 3}
                        ]
                    },
                    "output": "RoutingProfileId",
                    "template": "routing/profiles/support_agent"
                },
                {
                    "step": 5,
                    "action": "Create Contact Flow (optional)",
                    "tool": "config_create_contact_flow",
                    "params": {
                        "name": "Main Inbound Flow",
                        "flow_type": "CONTACT_FLOW",
                        "content": "<JSON string of flow definition>"
                    },
                    "note": "Content must be JSON.stringify'd flow definition",
                    "template": "contact_flows/healthcare_inbound"
                }
            ],
            "dependency_chain": "Hours → Queue → Routing Profile → Contact Flow",
            "tips": [
                "Each step's output ID is required for the next step",
                "Use template_get to fetch full template content",
                "Contact flow content must be a JSON string, not object"
            ]
        }

    @mcp.tool()
    def wizard_start_setup(
        use_case: str,
        instance_name: str,
        region: str = "us-east-1"
    ) -> dict[str, Any]:
        """Start the Amazon Connect setup wizard.
        
        Args:
            use_case: Primary use case (basic, cases_enabled, ai_enhanced, full_enterprise)
            instance_name: Desired instance alias
            region: AWS region for deployment
        
        Returns recommended configuration and next steps.
        """
        use_case_configs = {
            "basic": {
                "description": "Basic contact center with voice and chat",
                "features": ["voice", "chat", "basic_routing"],
                "templates": {
                    "hours": "routing/hours_of_operation/business_hours",
                    "queue": "routing/queues/general_support",
                    "profile": "routing/profiles/support_agent",
                    "iac": "iac/cloudformation/basic_instance"
                },
                "next_steps": [
                    "wizard_configure_basics",
                    "wizard_configure_routing",
                    "wizard_deploy"
                ]
            },
            "cases_enabled": {
                "description": "Contact center with case management",
                "features": ["voice", "chat", "basic_routing", "cases"],
                "templates": {
                    "hours": "routing/hours_of_operation/business_hours",
                    "queue": "routing/queues/general_support",
                    "profile": "routing/profiles/support_agent",
                    "case_template": "cases/general_support"
                },
                "next_steps": [
                    "wizard_configure_basics",
                    "wizard_configure_routing",
                    "wizard_configure_cases",
                    "wizard_deploy"
                ]
            },
            "ai_enhanced": {
                "description": "Contact center with AI assistance (Amazon Q in Connect)",
                "features": ["voice", "chat", "basic_routing", "cases", "amazon_q", "step_by_step_guides"],
                "templates": {
                    "hours": "routing/hours_of_operation/business_hours",
                    "queue": "routing/queues/general_support",
                    "profile": "routing/profiles/support_agent",
                    "case_template": "cases/general_support",
                    "screen_pop": "views/screen_pop",
                    "topic_selection": "views/topic_selection"
                },
                "next_steps": [
                    "wizard_configure_basics",
                    "wizard_configure_routing",
                    "wizard_configure_cases",
                    "wizard_configure_ai",
                    "wizard_configure_views",
                    "wizard_deploy"
                ]
            },
            "full_enterprise": {
                "description": "Full enterprise contact center with all features",
                "features": ["voice", "chat", "email", "tasks", "cases", "amazon_q", "customer_profiles", "contact_lens", "outbound_campaigns", "data_tables"],
                "templates": {
                    "hours": "routing/hours_of_operation/business_hours",
                    "queue": "routing/queues/general_support",
                    "profile": "routing/profiles/support_agent",
                    "case_templates": ["cases/general_support", "cases/billing_inquiry", "cases/technical_support"],
                    "views": ["views/screen_pop", "views/topic_selection", "views/case_creation_form", "views/call_disposition"],
                    "data_tables": ["data_tables/holiday_schedule", "data_tables/emergency_routing"]
                },
                "next_steps": [
                    "wizard_configure_basics",
                    "wizard_configure_routing",
                    "wizard_configure_cases",
                    "wizard_configure_ai",
                    "wizard_configure_views",
                    "wizard_configure_campaigns",
                    "wizard_deploy"
                ]
            }
        }
        
        config = use_case_configs.get(use_case, use_case_configs["basic"])
        
        return {
            "wizard_session": {
                "use_case": use_case,
                "instance_name": instance_name,
                "region": region,
                "status": "started"
            },
            "configuration": config,
            "message": f"Wizard started for '{use_case}' setup. Follow the next_steps to complete configuration."
        }

    @mcp.tool()
    def wizard_get_iac_template(
        use_case: str = "basic",
        instance_name: str = "my-connect-instance",
        region: str = "us-east-1",
        timezone: str = "America/New_York",
        enable_contact_lens: bool = True
    ) -> dict[str, Any]:
        """Generate Infrastructure as Code template for Amazon Connect deployment.
        
        Args:
            use_case: Deployment type (basic, cases_enabled, ai_enhanced, full_enterprise)
            instance_name: Instance alias
            region: AWS region
            timezone: Timezone for hours of operation
            enable_contact_lens: Enable Contact Lens analytics
        
        Returns CloudFormation template reference and deployment instructions.
        """
        return {
            "template_type": "CloudFormation",
            "use_case": use_case,
            "template_path": "templates/iac/cloudformation/basic_instance.yaml",
            "parameters": {
                "InstanceAlias": instance_name,
                "Timezone": timezone,
                "EnableContactLens": str(enable_contact_lens).lower()
            },
            "deployment_command": f"aws cloudformation create-stack --stack-name {instance_name}-connect --template-body file://basic_instance.yaml --parameters ParameterKey=InstanceAlias,ParameterValue={instance_name} ParameterKey=Timezone,ParameterValue={timezone} --region {region}",
            "note": "Use template_get(category='iac', name='basic_instance', subcategory='cloudformation') to fetch full template"
        }
