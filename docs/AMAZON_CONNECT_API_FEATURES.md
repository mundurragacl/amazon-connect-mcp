# Amazon Connect Features & API Reference for MCP Server Development

This document outlines Amazon Connect features and their API interfaces that can be leveraged to build an MCP (Model Context Protocol) server.

## Overview

Amazon Connect is a cloud-based omnichannel contact center solution. It consists of multiple service APIs that can be integrated into an MCP server.

---

## Service APIs

### 1. Amazon Connect Service (Core)
**AWS CLI Service:** `connect`

The main service for contact center management.

#### Key API Categories:

| Category | APIs | MCP Use Cases |
|----------|------|---------------|
| **Instance Management** | CreateInstance, DescribeInstance, ListInstances, DeleteInstance | Manage Connect instances |
| **Contact Flows** | CreateContactFlow, DescribeContactFlow, ListContactFlows, UpdateContactFlowContent | Build/modify IVR flows |
| **Contacts** | DescribeContact, SearchContacts, StartOutboundVoiceContact, StartChatContact, StopContact, TransferContact | Initiate/manage customer interactions |
| **Queues** | CreateQueue, DescribeQueue, ListQueues, UpdateQueueStatus | Queue management |
| **Routing Profiles** | CreateRoutingProfile, DescribeRoutingProfile, ListRoutingProfiles | Agent routing configuration |
| **Users/Agents** | CreateUser, DescribeUser, ListUsers, UpdateUserStatus, PutUserStatus | Agent management |
| **Agent Status** | CreateAgentStatus, ListAgentStatuses, UpdateAgentStatus | Agent availability |
| **Hours of Operation** | CreateHoursOfOperation, ListHoursOfOperations | Business hours config |
| **Phone Numbers** | ClaimPhoneNumber, ListPhoneNumbers, SearchAvailablePhoneNumbers | Telephony management |
| **Metrics** | GetCurrentMetricData, GetMetricDataV2, GetCurrentUserData | Real-time analytics |
| **Evaluations** | CreateEvaluationForm, StartContactEvaluation, SubmitContactEvaluation | Quality management |
| **Rules** | CreateRule, ListRules, UpdateRule | Automation rules |
| **Tasks** | StartTaskContact, CreateTaskTemplate | Task management |
| **Email** | CreateEmailAddress, StartEmailContact, SendOutboundEmail | Email channel |
| **Recording** | StartContactRecording, StopContactRecording, SuspendContactRecording | Call recording |
| **Data Tables** | CreateDataTable, BatchCreateDataTableValue, ListDataTables | Configuration storage |
| **Workspaces** | CreateWorkspace, ListWorkspaces, UpdateWorkspaceTheme | Agent workspace customization |

---

### 2. Amazon Connect Contact Lens
**AWS CLI Service:** `connect-contact-lens`

Real-time and post-call speech analytics.

| API | Description | MCP Use Cases |
|-----|-------------|---------------|
| ListRealtimeContactAnalysisSegments | Get real-time transcription and analytics | Live sentiment analysis, keyword detection |

---

### 3. Amazon Connect Cases
**AWS CLI Service:** `connectcases`

Case management for tracking customer issues.

| Category | APIs | MCP Use Cases |
|----------|------|---------------|
| **Cases** | CreateCase, GetCase, UpdateCase, SearchCases, DeleteCase | Issue tracking |
| **Domains** | CreateDomain, GetDomain, ListDomains | Case domain management |
| **Fields** | CreateField, BatchGetField, ListFields | Custom field definitions |
| **Templates** | CreateTemplate, GetTemplate, ListTemplates | Case templates |
| **Layouts** | CreateLayout, GetLayout, ListLayouts | UI layouts |
| **Related Items** | CreateRelatedItem, SearchRelatedItems | Link contacts to cases |

---

### 4. Amazon Connect Customer Profiles
**AWS CLI Service:** `customer-profiles`

Unified customer profile management.

| Category | APIs | MCP Use Cases |
|----------|------|---------------|
| **Profiles** | CreateProfile, GetProfile, SearchProfiles, UpdateProfile, MergeProfiles | Customer data management |
| **Domains** | CreateDomain, GetDomain, ListDomains | Profile domain setup |
| **Integrations** | PutIntegration, ListIntegrations | External data sources |
| **Segments** | CreateSegmentDefinition, GetSegmentMembership | Customer segmentation |
| **Identity Resolution** | GetMatches, ListIdentityResolutionJobs | Duplicate detection |
| **Calculated Attributes** | CreateCalculatedAttributeDefinition | Derived customer metrics |

---

### 5. Amazon Connect Participant Service
**AWS CLI Service:** `connectparticipant`

Manage chat/messaging participants.

| API | Description | MCP Use Cases |
|-----|-------------|---------------|
| CreateParticipantConnection | Establish participant connection | Chat initialization |
| SendMessage | Send chat messages | Automated responses |
| SendEvent | Send typing indicators, etc. | Chat UX |
| GetTranscript | Retrieve chat history | Conversation context |
| GetAttachment | Download shared files | File handling |
| DisconnectParticipant | End participant session | Chat cleanup |

---

### 6. Amazon Q in Connect
**AWS CLI Service:** `qconnect`

Generative AI-powered agent assistance.

| Category | APIs | MCP Use Cases |
|----------|------|---------------|
| **Knowledge Bases** | CreateKnowledgeBase, ListKnowledgeBases, SearchContent | Knowledge management |
| **Assistants** | CreateAssistant, GetAssistant, QueryAssistant | AI assistant config |
| **Sessions** | CreateSession, GetSession, GetRecommendations | Real-time recommendations |
| **Quick Responses** | CreateQuickResponse, SearchQuickResponses | Canned responses |
| **Message Templates** | CreateMessageTemplate, RenderMessageTemplate | Template management |
| **AI Agents** | CreateAIAgent, UpdateAIAgent, ListAIAgents | Custom AI agents |
| **AI Guardrails** | CreateAIGuardrail, ListAIGuardrails | Safety controls |
| **Content** | CreateContent, SearchContent, StartContentUpload | Knowledge articles |

---

### 7. Amazon Connect Outbound Campaigns (V2)
**AWS CLI Service:** `connectcampaignsv2`

High-volume outbound communications.

| Category | APIs | MCP Use Cases |
|----------|------|---------------|
| **Campaigns** | CreateCampaign, DescribeCampaign, ListCampaigns | Campaign management |
| **Campaign Control** | StartCampaign, PauseCampaign, ResumeCampaign, StopCampaign | Campaign execution |
| **Outbound Requests** | PutOutboundRequestBatch, PutProfileOutboundRequestBatch | Dial list management |
| **Configuration** | UpdateCampaignChannelSubtypeConfig, UpdateCampaignSchedule | Campaign settings |

---

### 8. Amazon AppIntegrations Service
**AWS CLI Service:** `appintegrations`

External application integrations.

| Category | APIs | MCP Use Cases |
|----------|------|---------------|
| **Applications** | CreateApplication, ListApplications | 3rd party app config |
| **Data Integrations** | CreateDataIntegration, ListDataIntegrations | Data sync setup |
| **Event Integrations** | CreateEventIntegration, ListEventIntegrations | Event routing |

---

### 9. Amazon Connect Voice ID ⚠️
**AWS CLI Service:** `voice-id`

> **Note:** End of support May 20, 2026

| Category | APIs | MCP Use Cases |
|----------|------|---------------|
| **Speakers** | DescribeSpeaker, ListSpeakers | Voice enrollment |
| **Fraudsters** | ListFraudsters, AssociateFraudster | Fraud detection |
| **Sessions** | EvaluateSession | Real-time authentication |

---

## Recommended MCP Server Tools

Based on the API analysis, here are suggested MCP tools organized by functionality:

---

### 🔧 SETUP & CONFIGURATION TOOLS

#### Instance Management
```
- create_instance              # CreateInstance - Provision new Connect instance
- describe_instance            # DescribeInstance - Get instance details
- list_instances               # ListInstances - List all instances
- delete_instance              # DeleteInstance - Remove instance
- update_instance_attribute    # UpdateInstanceAttribute - Modify instance settings
- replicate_instance           # ReplicateInstance - Clone instance to another region
```

#### Views (Agent UI Components)
```
- create_view                  # CreateView - Create custom agent UI view
- describe_view                # DescribeView - Get view details
- list_views                   # ListViews - List all views
- update_view_content          # UpdateViewContent - Modify view definition
- update_view_metadata         # UpdateViewMetadata - Update view name/description
- create_view_version          # CreateViewVersion - Version a view
- list_view_versions           # ListViewVersions - List view versions
- delete_view                  # DeleteView - Remove view
- delete_view_version          # DeleteViewVersion - Remove specific version
- search_views                 # SearchViews - Find views by criteria
```

#### Workspaces (Agent Desktop)
```
- create_workspace             # CreateWorkspace - Create agent workspace
- describe_workspace           # DescribeWorkspace - Get workspace details
- list_workspaces              # ListWorkspaces - List all workspaces
- update_workspace_metadata    # UpdateWorkspaceMetadata - Update workspace info
- update_workspace_theme       # UpdateWorkspaceTheme - Customize appearance
- update_workspace_visibility  # UpdateWorkspaceVisibility - Control access
- create_workspace_page        # CreateWorkspacePage - Add page to workspace
- list_workspace_pages         # ListWorkspacePages - List workspace pages
- update_workspace_page        # UpdateWorkspacePage - Modify page
- delete_workspace_page        # DeleteWorkspacePage - Remove page
- import_workspace_media       # ImportWorkspaceMedia - Upload images/assets
- list_workspace_media         # ListWorkspaceMedia - List uploaded media
- delete_workspace_media       # DeleteWorkspaceMedia - Remove media
- associate_workspace          # AssociateWorkspace - Link workspace to instance
- disassociate_workspace       # DisassociateWorkspace - Unlink workspace
- search_workspaces            # SearchWorkspaces - Find workspaces
- search_workspace_associations # SearchWorkspaceAssociations - Find linked workspaces
- delete_workspace             # DeleteWorkspace - Remove workspace
```

#### Data Tables (Agent Configuration Tables)
```
- create_data_table            # CreateDataTable - Create config table
- describe_data_table          # DescribeDataTable - Get table details
- list_data_tables             # ListDataTables - List all tables
- search_data_tables           # SearchDataTables - Find tables
- update_data_table_metadata   # UpdateDataTableMetadata - Update table info
- delete_data_table            # DeleteDataTable - Remove table
- create_data_table_attribute  # CreateDataTableAttribute - Add column
- describe_data_table_attribute # DescribeDataTableAttribute - Get column details
- list_data_table_attributes   # ListDataTableAttributes - List columns
- update_data_table_attribute  # UpdateDataTableAttribute - Modify column
- delete_data_table_attribute  # DeleteDataTableAttribute - Remove column
- batch_create_data_table_value # BatchCreateDataTableValue - Insert rows
- batch_describe_data_table_value # BatchDescribeDataTableValue - Get rows
- batch_update_data_table_value # BatchUpdateDataTableValue - Update rows
- batch_delete_data_table_value # BatchDeleteDataTableValue - Delete rows
- list_data_table_values       # ListDataTableValues - List all rows
- list_data_table_primary_values # ListDataTablePrimaryValues - List primary keys
- update_data_table_primary_values # UpdateDataTablePrimaryValues - Update keys
- evaluate_data_table_values   # EvaluateDataTableValues - Query/filter rows
```

#### Task Templates
```
- create_task_template         # CreateTaskTemplate - Define task structure
- get_task_template            # GetTaskTemplate - Get template details
- list_task_templates          # ListTaskTemplates - List all templates
- update_task_template         # UpdateTaskTemplate - Modify template
- delete_task_template         # DeleteTaskTemplate - Remove template
```

#### Contact Flows
```
- create_contact_flow          # CreateContactFlow - Create IVR flow
- describe_contact_flow        # DescribeContactFlow - Get flow details
- list_contact_flows           # ListContactFlows - List all flows
- update_contact_flow_content  # UpdateContactFlowContent - Modify flow logic
- update_contact_flow_metadata # UpdateContactFlowMetadata - Update flow info
- update_contact_flow_name     # UpdateContactFlowName - Rename flow
- create_contact_flow_version  # CreateContactFlowVersion - Version a flow
- list_contact_flow_versions   # ListContactFlowVersions - List versions
- delete_contact_flow          # DeleteContactFlow - Remove flow
- delete_contact_flow_version  # DeleteContactFlowVersion - Remove version
- search_contact_flows         # SearchContactFlows - Find flows
```

#### Flow Modules (Reusable Flow Components)
```
- create_contact_flow_module   # CreateContactFlowModule - Create reusable module
- describe_contact_flow_module # DescribeContactFlowModule - Get module details
- list_contact_flow_modules    # ListContactFlowModules - List all modules
- update_contact_flow_module_content # UpdateContactFlowModuleContent - Modify module
- update_contact_flow_module_metadata # UpdateContactFlowModuleMetadata - Update info
- create_contact_flow_module_version # CreateContactFlowModuleVersion - Version module
- list_contact_flow_module_versions # ListContactFlowModuleVersions - List versions
- delete_contact_flow_module   # DeleteContactFlowModule - Remove module
- search_contact_flow_modules  # SearchContactFlowModules - Find modules
```

---

### 📋 CASES CONFIGURATION TOOLS

#### Case Domains
```
- create_domain                # CreateDomain - Create case domain
- get_domain                   # GetDomain - Get domain details
- list_domains                 # ListDomains - List all domains
- delete_domain                # DeleteDomain - Remove domain
```

#### Case Templates
```
- create_template              # CreateTemplate - Define case template
- get_template                 # GetTemplate - Get template details
- list_templates               # ListTemplates - List all templates
- update_template              # UpdateTemplate - Modify template
- delete_template              # DeleteTemplate - Remove template
```

#### Case Fields
```
- create_field                 # CreateField - Create custom field
- batch_get_field              # BatchGetField - Get multiple fields
- list_fields                  # ListFields - List all fields
- update_field                 # UpdateField - Modify field
- delete_field                 # DeleteField - Remove field
- batch_put_field_options      # BatchPutFieldOptions - Set field options (dropdowns)
- list_field_options           # ListFieldOptions - List field options
```

#### Case Layouts
```
- create_layout                # CreateLayout - Create case UI layout
- get_layout                   # GetLayout - Get layout details
- list_layouts                 # ListLayouts - List all layouts
- update_layout                # UpdateLayout - Modify layout
- delete_layout                # DeleteLayout - Remove layout
```

#### Case Rules (Automation)
```
- create_case_rule             # CreateCaseRule - Create automation rule
- batch_get_case_rule          # BatchGetCaseRule - Get multiple rules
- list_case_rules              # ListCaseRules - List all rules
- update_case_rule             # UpdateCaseRule - Modify rule
- delete_case_rule             # DeleteCaseRule - Remove rule
```

#### Case Event Configuration
```
- get_case_event_configuration # GetCaseEventConfiguration - Get event settings
- put_case_event_configuration # PutCaseEventConfiguration - Configure events
```

---

### 📝 CASES OPERATIONS TOOLS

#### Case CRUD
```
- create_case                  # CreateCase - Create new case
- get_case                     # GetCase - Get case details
- update_case                  # UpdateCase - Modify case (status, fields, assignment)
- delete_case                  # DeleteCase - Remove case
- search_cases                 # SearchCases - Find cases by criteria
- list_cases_for_contact       # ListCasesForContact - Get cases linked to contact
- get_case_audit_events        # GetCaseAuditEvents - Get case history/changes
```

#### Case Related Items (Link Contacts, Comments, etc.)
```
- create_related_item          # CreateRelatedItem - Link contact/comment to case
- search_related_items         # SearchRelatedItems - Find related items
- search_all_related_items     # SearchAllRelatedItems - Search across all items
- delete_related_item          # DeleteRelatedItem - Remove related item
```

---

### 👥 AGENT & USER MANAGEMENT TOOLS

#### Users
```
- create_user                  # CreateUser - Create agent account
- describe_user                # DescribeUser - Get user details
- list_users                   # ListUsers - List all users
- search_users                 # SearchUsers - Find users by criteria
- update_user_identity_info    # UpdateUserIdentityInfo - Update name/email
- update_user_phone_config     # UpdateUserPhoneConfig - Update phone settings
- update_user_routing_profile  # UpdateUserRoutingProfile - Change routing
- update_user_security_profiles # UpdateUserSecurityProfiles - Change permissions
- update_user_hierarchy        # UpdateUserHierarchy - Change org position
- delete_user                  # DeleteUser - Remove user
```

#### Agent Status
```
- create_agent_status          # CreateAgentStatus - Create status (Available, Break, etc.)
- describe_agent_status        # DescribeAgentStatus - Get status details
- list_agent_statuses          # ListAgentStatuses - List all statuses
- search_agent_statuses        # SearchAgentStatuses - Find statuses
- update_agent_status          # UpdateAgentStatus - Modify status
- put_user_status              # PutUserStatus - Set agent's current status
```

#### User Hierarchy
```
- create_user_hierarchy_group  # CreateUserHierarchyGroup - Create org group
- describe_user_hierarchy_group # DescribeUserHierarchyGroup - Get group details
- describe_user_hierarchy_structure # DescribeUserHierarchyStructure - Get org structure
- list_user_hierarchy_groups   # ListUserHierarchyGroups - List groups
- search_user_hierarchy_groups # SearchUserHierarchyGroups - Find groups
- update_user_hierarchy_group_name # UpdateUserHierarchyGroupName - Rename group
- update_user_hierarchy_structure # UpdateUserHierarchyStructure - Modify structure
- delete_user_hierarchy_group  # DeleteUserHierarchyGroup - Remove group
```

#### User Proficiencies (Skills)
```
- associate_user_proficiencies # AssociateUserProficiencies - Add skills to user
- list_user_proficiencies      # ListUserProficiencies - List user skills
- update_user_proficiencies    # UpdateUserProficiencies - Modify skill levels
- disassociate_user_proficiencies # DisassociateUserProficiencies - Remove skills
```

---

### 📞 CONTACT OPERATIONS TOOLS

#### Inbound/Outbound Contacts
```
- start_outbound_voice_contact # StartOutboundVoiceContact - Initiate outbound call
- start_chat_contact           # StartChatContact - Start chat session
- start_task_contact           # StartTaskContact - Create task
- start_email_contact          # StartEmailContact - Start email interaction
- start_outbound_chat_contact  # StartOutboundChatContact - Outbound chat
- start_outbound_email_contact # StartOutboundEmailContact - Outbound email
- start_web_rtc_contact        # StartWebRTCContact - Start web call
```

#### Contact Management
```
- describe_contact             # DescribeContact - Get contact details
- search_contacts              # SearchContacts - Find contacts
- update_contact               # UpdateContact - Modify contact
- update_contact_attributes    # UpdateContactAttributes - Set custom attributes
- transfer_contact             # TransferContact - Transfer to queue/agent
- stop_contact                 # StopContact - End contact
- pause_contact                # PauseContact - Pause contact
- resume_contact               # ResumeContact - Resume paused contact
- monitor_contact              # MonitorContact - Supervisor monitoring
```

#### Contact Recording
```
- start_contact_recording      # StartContactRecording - Begin recording
- stop_contact_recording       # StopContactRecording - End recording
- suspend_contact_recording    # SuspendContactRecording - Pause recording
- resume_contact_recording     # ResumeContactRecording - Resume recording
```

---

### 📊 REAL-TIME & ANALYTICS TOOLS

#### Real-time Metrics
```
- get_current_metric_data      # GetCurrentMetricData - Real-time queue/agent metrics
- get_current_user_data        # GetCurrentUserData - Real-time agent data
- get_metric_data_v2           # GetMetricDataV2 - Advanced metrics query
```

#### Historical Metrics
```
- get_metric_data              # GetMetricData - Historical metrics
- search_contacts              # SearchContacts - Contact history search
```

#### Contact Lens Analytics
```
- list_realtime_contact_analysis_segments # Real-time transcription/sentiment
- list_realtime_contact_analysis_segments_v2 # Enhanced real-time analytics
```

---

### 🧠 KNOWLEDGE & AI TOOLS (Amazon Q in Connect)

#### Knowledge Bases
```
- create_knowledge_base        # CreateKnowledgeBase - Create KB
- get_knowledge_base           # GetKnowledgeBase - Get KB details
- list_knowledge_bases         # ListKnowledgeBases - List all KBs
- delete_knowledge_base        # DeleteKnowledgeBase - Remove KB
```

#### Content Management
```
- create_content               # CreateContent - Add article
- get_content                  # GetContent - Get article
- list_contents                # ListContents - List articles
- search_content               # SearchContent - Search articles
- update_content               # UpdateContent - Modify article
- delete_content               # DeleteContent - Remove article
- start_content_upload         # StartContentUpload - Upload content file
```

#### AI Assistants
```
- create_assistant             # CreateAssistant - Create AI assistant
- get_assistant                # GetAssistant - Get assistant details
- list_assistants              # ListAssistants - List assistants
- delete_assistant             # DeleteAssistant - Remove assistant
- query_assistant              # QueryAssistant - Query for recommendations
```

#### Sessions & Recommendations
```
- create_session               # CreateSession - Start AI session
- get_session                  # GetSession - Get session details
- get_recommendations          # GetRecommendations - Get AI suggestions
- search_sessions              # SearchSessions - Find sessions
```

#### Quick Responses
```
- create_quick_response        # CreateQuickResponse - Create canned response
- get_quick_response           # GetQuickResponse - Get response details
- list_quick_responses         # ListQuickResponses - List responses
- search_quick_responses       # SearchQuickResponses - Find responses
- update_quick_response        # UpdateQuickResponse - Modify response
- delete_quick_response        # DeleteQuickResponse - Remove response
```

---

### 👤 CUSTOMER PROFILES TOOLS

#### Profile Operations
```
- create_profile               # CreateProfile - Create customer profile
- get_profile                  # GetProfile - Get profile details
- search_profiles              # SearchProfiles - Find profiles
- update_profile               # UpdateProfile - Modify profile
- delete_profile               # DeleteProfile - Remove profile
- merge_profiles               # MergeProfiles - Combine duplicate profiles
- batch_get_profile            # BatchGetProfile - Get multiple profiles
```

#### Segmentation
```
- create_segment_definition    # CreateSegmentDefinition - Define segment
- get_segment_definition       # GetSegmentDefinition - Get segment details
- list_segment_definitions     # ListSegmentDefinitions - List segments
- get_segment_membership       # GetSegmentMembership - Get profiles in segment
- delete_segment_definition    # DeleteSegmentDefinition - Remove segment
```

---

### 📢 OUTBOUND CAMPAIGNS TOOLS

#### Campaign Management
```
- create_campaign              # CreateCampaign - Create outbound campaign
- describe_campaign            # DescribeCampaign - Get campaign details
- list_campaigns               # ListCampaigns - List all campaigns
- update_campaign_name         # UpdateCampaignName - Rename campaign
- update_campaign_schedule     # UpdateCampaignSchedule - Modify schedule
- delete_campaign              # DeleteCampaign - Remove campaign
```

#### Campaign Execution
```
- start_campaign               # StartCampaign - Begin campaign
- pause_campaign               # PauseCampaign - Pause campaign
- resume_campaign              # ResumeCampaign - Resume campaign
- stop_campaign                # StopCampaign - End campaign
- get_campaign_state           # GetCampaignState - Get campaign status
```

#### Outbound Requests
```
- put_outbound_request_batch   # PutOutboundRequestBatch - Add contacts to dial
- put_profile_outbound_request_batch # PutProfileOutboundRequestBatch - Add profiles to dial
```

---

### 💬 CHAT OPERATIONS TOOLS (Participant Service)

```
- create_participant_connection # CreateParticipantConnection - Connect to chat
- send_message                 # SendMessage - Send chat message
- send_event                   # SendEvent - Send typing indicator, etc.
- get_transcript               # GetTranscript - Get chat history
- get_attachment               # GetAttachment - Download file
- disconnect_participant       # DisconnectParticipant - End chat session
```

---

## API Authentication

All APIs use AWS IAM authentication. The MCP server should:
1. Use AWS SDK credentials (environment variables, profiles, or IAM roles)
2. Require appropriate IAM permissions for each operation
3. Support region configuration

---

## Key Considerations for MCP Implementation

1. **Rate Limits**: Amazon Connect has service quotas - implement throttling
2. **Instance ID**: Most APIs require `InstanceId` - consider caching
3. **ARN Format**: Many resources use ARNs - provide helper utilities
4. **Pagination**: List operations return paginated results
5. **Real-time vs Historical**: Different APIs for real-time metrics vs historical data
6. **Regional**: Connect instances are regional - handle multi-region scenarios

---

## References

- [Amazon Connect API Reference](https://docs.aws.amazon.com/connect/latest/APIReference/Welcome.html)
- [Amazon Connect Admin Guide](https://docs.aws.amazon.com/connect/latest/adminguide/)
- [Amazon Connect Service Quotas](https://docs.aws.amazon.com/connect/latest/adminguide/amazon-connect-service-limits.html)
