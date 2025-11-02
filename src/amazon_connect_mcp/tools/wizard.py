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
        
        Args:
            category: Template category (cases, views, data_tables, routing, profiles, ai, campaigns, iac)
            name: Template name (without extension)
            subcategory: Optional subcategory (e.g., 'hours_of_operation' for routing)
        
        Returns the full template content.
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
        
        Returns CloudFormation template and deployment instructions.
        """
        try:
            template = get_template("iac", "basic_instance", "cloudformation")
            
            return {
                "template_type": "CloudFormation",
                "use_case": use_case,
                "parameters": {
                    "InstanceAlias": instance_name,
                    "Timezone": timezone,
                    "EnableContactLens": str(enable_contact_lens).lower()
                },
                "template": template,
                "deployment_commands": [
                    f"# Deploy using AWS CLI",
                    f"aws cloudformation create-stack \\",
                    f"  --stack-name {instance_name}-connect \\",
                    f"  --template-body file://basic_instance.yaml \\",
                    f"  --parameters ParameterKey=InstanceAlias,ParameterValue={instance_name} \\",
                    f"               ParameterKey=Timezone,ParameterValue={timezone} \\",
                    f"               ParameterKey=EnableContactLens,ParameterValue={str(enable_contact_lens).lower()} \\",
                    f"  --region {region}",
                    "",
                    f"# Or deploy using SAM CLI",
                    f"sam deploy --template-file basic_instance.yaml --stack-name {instance_name}-connect --region {region} --guided"
                ]
            }
        except Exception as e:
            return {"error": str(e)}
