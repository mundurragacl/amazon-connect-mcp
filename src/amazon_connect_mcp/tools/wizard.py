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

    @mcp.tool()
    def wizard_discover_website(url: str) -> dict[str, Any]:
        """Discover business information from a website for contact center setup.
        
        Extracts brand name, industry, hours, FAQs, and products from the website.
        Use this as the first step in automated onboarding.
        
        Args:
            url: Website URL to analyze (e.g., 'https://example.com')
        
        Returns extracted business data for confirmation before setup.
        """
        import urllib.request
        import urllib.error
        from html.parser import HTMLParser
        
        class SimpleHTMLParser(HTMLParser):
            def __init__(self):
                super().__init__()
                self.text = []
                self.title = ""
                self.in_title = False
                self.faqs = []
                self.current_tag = ""
                self.links = []
                
            def handle_starttag(self, tag, attrs):
                self.current_tag = tag
                if tag == "title":
                    self.in_title = True
                if tag == "a":
                    for attr, value in attrs:
                        if attr == "href" and value:
                            self.links.append(value)
                            
            def handle_endtag(self, tag):
                if tag == "title":
                    self.in_title = False
                self.current_tag = ""
                    
            def handle_data(self, data):
                if self.in_title:
                    self.title = data.strip()
                text = data.strip()
                if text:
                    self.text.append(text)
        
        try:
            # Fetch website
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=30) as response:
                html = response.read().decode("utf-8", errors="ignore")
        except Exception as e:
            return {"error": f"Failed to fetch website: {str(e)}"}
        
        # Parse HTML
        parser = SimpleHTMLParser()
        parser.feed(html)
        full_text = " ".join(parser.text).lower()
        
        # Extract brand from title
        brand = parser.title.split("|")[0].split("-")[0].split("–")[0].strip()
        brand = re.sub(r"[^a-zA-Z0-9\s]", "", brand).strip()
        if not brand:
            brand = url.split("//")[-1].split("/")[0].replace("www.", "").split(".")[0]
        brand_slug = re.sub(r"[^a-z0-9]+", "-", brand.lower()).strip("-")
        
        # Detect industry
        industry_scores = {}
        for industry, keywords in INDUSTRY_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in full_text)
            if score > 0:
                industry_scores[industry] = score
        
        detected_industry = max(industry_scores, key=industry_scores.get) if industry_scores else "general"
        
        # Extract FAQ-like content (questions)
        faqs = []
        question_patterns = [
            r"(?:^|\n)\s*(?:Q:|FAQ:)?\s*([^?\n]+\?)",
            r"<h[2-4][^>]*>([^<]*\?)</h[2-4]>",
        ]
        for pattern in question_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches[:10]:
                q = match.strip()
                if len(q) > 10 and len(q) < 200:
                    faqs.append({
                        "title": q,
                        "summary": "Extracted from website - please review and expand",
                        "content": "Please add detailed answer here"
                    })
        
        # Extract hours (common patterns)
        hours_patterns = [
            r"(\d{1,2}(?::\d{2})?\s*(?:am|pm)\s*[-–to]+\s*\d{1,2}(?::\d{2})?\s*(?:am|pm))",
            r"(monday|tuesday|wednesday|thursday|friday|saturday|sunday)[:\s]+(\d{1,2}(?::\d{2})?\s*(?:am|pm)?)",
        ]
        hours_text = []
        for pattern in hours_patterns:
            matches = re.findall(pattern, full_text, re.IGNORECASE)
            hours_text.extend([str(m) for m in matches[:5]])
        
        # Default hours config
        hours_config = {
            "timezone": "America/New_York",
            "schedule": [
                {"day": "MONDAY", "start": "09:00", "end": "17:00"},
                {"day": "TUESDAY", "start": "09:00", "end": "17:00"},
                {"day": "WEDNESDAY", "start": "09:00", "end": "17:00"},
                {"day": "THURSDAY", "start": "09:00", "end": "17:00"},
                {"day": "FRIDAY", "start": "09:00", "end": "17:00"},
            ],
            "extracted_hints": hours_text if hours_text else ["No hours found - using default M-F 9-5"]
        }
        
        # Extract contact info
        email_match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", html)
        phone_match = re.search(r"[\+]?[\d\s\-\(\)]{10,}", html)
        
        # Get templates for detected industry
        templates = INDUSTRY_TEMPLATES.get(detected_industry, INDUSTRY_TEMPLATES["general"])
        
        return {
            "brand": brand,
            "brand_slug": brand_slug,
            "url": url,
            "industry": detected_industry,
            "industry_confidence": industry_scores.get(detected_industry, 0),
            "hours": hours_config,
            "faqs": faqs if faqs else [
                {"title": "What are your hours?", "summary": "Our business hours", "content": "Please add your hours here"},
                {"title": "How do I contact support?", "summary": "Contact options", "content": "Please add contact info here"},
                {"title": "What is your return policy?", "summary": "Return policy details", "content": "Please add policy here"}
            ],
            "contact": {
                "email": email_match.group(0) if email_match else None,
                "phone": phone_match.group(0).strip() if phone_match else None
            },
            "recommended_templates": templates,
            "next_step": "Review this data, then call wizard_generate_faq_files(brand_slug, faqs) to create FAQ files"
        }

    @mcp.tool()
    def wizard_generate_faq_files(brand: str, faqs: list[dict]) -> dict[str, Any]:
        """Generate FAQ text files for Q in Connect knowledge base.
        
        Creates one .txt file per FAQ question in ./{brand}/faq/ directory.
        Files are formatted for Q in Connect ingestion (max 1MB each).
        
        Args:
            brand: Brand slug for directory name (e.g., 'acme-corp')
            faqs: List of FAQ objects with title, summary, and content fields
        
        Returns paths to created files and state file location.
        """
        base_dir = Path(f"./{brand}")
        faq_dir = base_dir / "faq"
        
        # Create directories
        faq_dir.mkdir(parents=True, exist_ok=True)
        
        created_files = []
        for i, faq in enumerate(faqs, 1):
            title = faq.get("title", f"Question {i}")
            summary = faq.get("summary", "")
            content = faq.get("content", "")
            
            # Create filename from title
            filename = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:50]
            filename = f"{i:02d}-{filename}.txt"
            filepath = faq_dir / filename
            
            # Format content
            file_content = f"""Title: {title}

Summary: {summary}

Content:
{content}
"""
            filepath.write_text(file_content)
            created_files.append(str(filepath))
        
        # Initialize state file
        state = {
            "brand": brand,
            "started_at": datetime.utcnow().isoformat() + "Z",
            "updated_at": datetime.utcnow().isoformat() + "Z",
            "current_phase": 0,
            "current_step": 0,
            "completed_steps": [],
            "resources": {},
            "faq_directory": str(faq_dir),
            "faq_count": len(created_files),
            "error": None
        }
        state_file = base_dir / f"{brand}_onboarding_state.json"
        state_file.write_text(json.dumps(state, indent=2))
        
        return {
            "brand": brand,
            "faq_directory": str(faq_dir),
            "files_created": created_files,
            "state_file": str(state_file),
            "next_step": f"Review FAQ files in {faq_dir}/, edit as needed, then call wizard_execute_onboarding()"
        }

    @mcp.tool()
    def wizard_execute_onboarding(
        brand: str,
        region: str = "us-east-1",
        industry: str = "general",
        hours_config: dict | None = None,
        resume: bool = True
    ) -> dict[str, Any]:
        """Execute the full onboarding workflow with resume support.
        
        Creates Connect instance, configures routing, enables Cases and Q in Connect.
        Reads state from ./{brand}/{brand}_onboarding_state.json for resume capability.
        
        Args:
            brand: Brand slug (must match directory created by wizard_generate_faq_files)
            region: AWS region for the instance
            industry: Industry type for template selection
            hours_config: Optional custom hours configuration
            resume: If True, resume from last successful step
        
        Returns current progress and next manual steps if any.
        """
        base_dir = Path(f"./{brand}")
        state_file = base_dir / f"{brand}_onboarding_state.json"
        
        # Load or create state
        if state_file.exists() and resume:
            state = json.loads(state_file.read_text())
        else:
            state = {
                "brand": brand,
                "started_at": datetime.utcnow().isoformat() + "Z",
                "updated_at": datetime.utcnow().isoformat() + "Z",
                "region": region,
                "industry": industry,
                "current_phase": 1,
                "current_step": 0,
                "completed_steps": [],
                "resources": {},
                "error": None
            }
        
        state["region"] = region
        state["industry"] = industry
        if hours_config:
            state["hours_config"] = hours_config
        
        def save_state():
            state["updated_at"] = datetime.utcnow().isoformat() + "Z"
            state_file.write_text(json.dumps(state, indent=2))
        
        # Get templates for industry
        templates = INDUSTRY_TEMPLATES.get(industry, INDUSTRY_TEMPLATES["general"])
        state["templates"] = templates
        save_state()
        
        # Return orchestration instructions for LLM
        completed = state.get("completed_steps", [])
        resources = state.get("resources", {})
        
        steps = [
            {
                "step": 1,
                "phase": "Instance Creation",
                "tool": "create_instance",
                "params": {
                    "instance_alias": brand,
                    "identity_management_type": "CONNECT_MANAGED",
                    "region": region
                },
                "save_output": "instance_id",
                "completed": 1 in completed
            },
            {
                "step": 2,
                "phase": "Wait for Instance",
                "action": "wait",
                "description": "Sleep 60s then check instance status with describe_instance",
                "completed": 2 in completed
            },
            {
                "step": 3,
                "phase": "Set Session",
                "tool": "set_session",
                "params": {
                    "instance_id": resources.get("instance_id", "<from step 1>"),
                    "region": region
                },
                "completed": 3 in completed
            },
            {
                "step": 4,
                "phase": "Hours of Operation",
                "tool": "config_create_hours_of_operation",
                "params": {
                    "name": f"{brand} Hours",
                    "time_zone": hours_config.get("timezone", "America/New_York") if hours_config else "America/New_York",
                    "config": _build_hours_config(hours_config)
                },
                "save_output": "hours_of_operation_id",
                "completed": 4 in completed
            },
            {
                "step": 5,
                "phase": "Queue",
                "tool": "config_create_queue",
                "params": {
                    "name": f"{brand} Support",
                    "hours_of_operation_id": resources.get("hours_of_operation_id", "<from step 4>")
                },
                "save_output": "queue_id",
                "completed": 5 in completed
            },
            {
                "step": 6,
                "phase": "Routing Profile",
                "tool": "config_create_routing_profile",
                "params": {
                    "name": f"{brand} Agent",
                    "default_outbound_queue_id": resources.get("queue_id", "<from step 5>")
                },
                "save_output": "routing_profile_id",
                "completed": 6 in completed
            },
            {
                "step": 7,
                "phase": "Customer Profiles Domain",
                "tool": "profiles_create_domain",
                "params": {"domain_name": brand},
                "save_output": "profiles_domain_name",
                "completed": 7 in completed
            },
            {
                "step": 8,
                "phase": "Cases Domain",
                "tool": "cases_create_domain",
                "params": {"name": brand},
                "save_output": "cases_domain_id",
                "completed": 8 in completed
            },
            {
                "step": 9,
                "phase": "Cases Template",
                "tool": "cases_create_template",
                "params": {
                    "domain_id": resources.get("cases_domain_id", "<from step 8>"),
                    "name": f"{brand} Support"
                },
                "save_output": "cases_template_id",
                "completed": 9 in completed
            },
            {
                "step": 10,
                "phase": "Q in Connect",
                "action": "manual",
                "description": "Enable Amazon Q in Connect via console, then upload FAQ files",
                "faq_directory": str(base_dir / "faq"),
                "completed": 10 in completed
            }
        ]
        
        # Find next step
        next_step = None
        for step in steps:
            if not step["completed"]:
                next_step = step
                break
        
        return {
            "brand": brand,
            "region": region,
            "industry": industry,
            "state_file": str(state_file),
            "progress": f"{len(completed)}/{len(steps)} steps completed",
            "resources": resources,
            "steps": steps,
            "next_step": next_step,
            "instructions": "Execute each step in order. After each tool call, call wizard_update_onboarding_state() to save progress."
        }

    @mcp.tool()
    def wizard_update_onboarding_state(
        brand: str,
        step: int,
        resource_key: str | None = None,
        resource_value: str | None = None,
        error: str | None = None
    ) -> dict[str, Any]:
        """Update onboarding state after completing a step.
        
        Call this after each successful tool execution to enable resume.
        
        Args:
            brand: Brand slug
            step: Step number that was completed
            resource_key: Optional key to save (e.g., 'instance_id')
            resource_value: Optional value to save
            error: Optional error message if step failed
        
        Returns updated state.
        """
        state_file = Path(f"./{brand}/{brand}_onboarding_state.json")
        
        if not state_file.exists():
            return {"error": f"State file not found: {state_file}"}
        
        state = json.loads(state_file.read_text())
        
        if error:
            state["error"] = {"step": step, "message": error}
        else:
            if step not in state.get("completed_steps", []):
                state.setdefault("completed_steps", []).append(step)
            if resource_key and resource_value:
                state.setdefault("resources", {})[resource_key] = resource_value
            state["current_step"] = step
            state["error"] = None
        
        state["updated_at"] = datetime.utcnow().isoformat() + "Z"
        state_file.write_text(json.dumps(state, indent=2))
        
        return {
            "brand": brand,
            "step_completed": step,
            "resource_saved": {resource_key: resource_value} if resource_key else None,
            "total_completed": len(state.get("completed_steps", [])),
            "state": state
        }


def _build_hours_config(hours_config: dict | None) -> list[dict]:
    """Build hours of operation config from schedule."""
    if not hours_config or "schedule" not in hours_config:
        # Default M-F 9-5
        return [
            {"Day": day, "StartTime": {"Hours": 9, "Minutes": 0}, "EndTime": {"Hours": 17, "Minutes": 0}}
            for day in ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY"]
        ]
    
    config = []
    for item in hours_config["schedule"]:
        start_parts = item.get("start", "09:00").split(":")
        end_parts = item.get("end", "17:00").split(":")
        config.append({
            "Day": item.get("day", "MONDAY").upper(),
            "StartTime": {"Hours": int(start_parts[0]), "Minutes": int(start_parts[1]) if len(start_parts) > 1 else 0},
            "EndTime": {"Hours": int(end_parts[0]), "Minutes": int(end_parts[1]) if len(end_parts) > 1 else 0}
        })
    return config
