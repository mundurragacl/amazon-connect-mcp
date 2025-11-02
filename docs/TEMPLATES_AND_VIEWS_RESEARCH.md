# Amazon Connect Templates, Views & Configuration Research

## Overview

This document captures research on Amazon Connect configuration templates for:
- Cases Templates & Fields
- Agent Workspace Views
- Step-by-Step Guides
- Data Tables
- Routing Configuration
- Customer Profiles
- Amazon Q in Connect (AI)
- Outbound Campaigns
- Infrastructure as Code (IaC)

---

## 1. Cases Templates & Fields

### Case Templates
Case templates are forms used to ensure agents collect specific information for customer issues.

**Key Components:**
- **Template Name**: Unique identifier (max 100 chars)
- **Layout Configuration**: Defines field arrangement
- **Required Fields**: Fields that must have values
- **Status**: Active or Inactive
- **Case Rules**: Dynamic conditions for fields

**Template Structure:**
```json
{
  "name": "General Support Case",
  "description": "Standard support case template",
  "status": "Active",
  "layoutConfiguration": {
    "defaultLayout": "<layout-id>"
  },
  "requiredFields": [
    {"fieldId": "<field-id>"}
  ],
  "rules": []
}
```

### Case Fields
**System Fields (Cannot be altered):**
- Case ID
- Case Reason
- Status (Open, Closed + custom)
- Title
- Customer
- Created Date
- Last Updated

**Custom Field Types:**
- Text (single/multi-line)
- Number
- Single-select (dropdown)
- Boolean (true/false)
- DateTime
- URL

### Case Layouts
Layouts determine:
- Which fields to display
- Section placement (Top panel vs More information)
- Field order within sections

**Layout Sections:**
1. **Top Panel**: Always visible fields
2. **More Information**: Tabbed subsection

### Case Field Conditions
Three types of dynamic conditions:
1. **Conditionally Required**: Enforce field completion based on criteria
2. **Hidden Field Conditions**: Show/hide fields based on other values
3. **Dependent Field Options**: Cascading dropdowns

---

## 2. Agent Workspace Views

### AWS Managed Views

#### Detail View
Display information and provide action lists.
```json
{
  "AttributeBar": [
    {"Label": "Queue", "Value": "Sales"},
    {"Label": "Case ID", "Value": "123456", "LinkType": "case", "ResourceId": "123456", "Copyable": true}
  ],
  "Back": {"Label": "Back"},
  "Heading": "Customer Information",
  "Description": "Review customer details",
  "Sections": [
    {"TemplateString": "Customer has been with us for 5 years"}
  ],
  "Actions": ["Create Case", "Transfer Call", "Schedule Callback"]
}
```

#### List View
Display items with titles and descriptions.
```json
{
  "Heading": "Customer may be contacting about...",
  "SubHeading": "Select an option",
  "Items": [
    {"Heading": "Billing Issue", "Description": "Payment or invoice questions", "Icon": "Payment", "Id": "billing"},
    {"Heading": "Technical Support", "Description": "Product issues", "Icon": "Support", "Id": "tech"},
    {"Heading": "Account Changes", "Description": "Update account info", "Icon": "Account", "Id": "account"}
  ]
}
```

#### Form View
Gather data from agents with input fields.
```json
{
  "Heading": "Create New Case",
  "Sections": [
    {
      "Type": "FormSection",
      "Heading": "Customer Details",
      "Items": [
        {"Type": "FormInput", "Label": "Customer Name", "Name": "customer-name", "InputType": "text"},
        {"Type": "FormInput", "Label": "Phone", "Name": "phone", "InputType": "tel"},
        {"Type": "FormInput", "Label": "Email", "Name": "email", "InputType": "email"}
      ]
    }
  ],
  "Next": {"Label": "Submit"},
  "Cancel": {"Label": "Cancel"}
}
```

#### Confirmation View
Display after form submission or action completion.
```json
{
  "Heading": "Case Created Successfully",
  "Description": "Case #12345 has been created",
  "Icon": "Success",
  "Actions": ["View Case", "Back to Home"]
}
```

#### Cards View
Present topics for agents to choose from.
```json
{
  "Heading": "Select Topic",
  "Sections": [
    {"Summary": "Returns", "Detail": "Process return requests"},
    {"Summary": "Exchanges", "Detail": "Handle product exchanges"},
    {"Summary": "Refunds", "Detail": "Issue refunds"}
  ]
}
```

### Custom Views
Support HTML and JSX for advanced customization.

---

## 3. Data Tables

### Purpose
Store operational data for dynamic lookups in flows without code.

### Use Cases
- Holiday schedules
- Emergency routing flags
- Agent extension mappings
- Location-specific prompts
- Business hours overrides

### Data Table Structure
```json
{
  "name": "HolidaySchedule",
  "description": "Contact center holiday closures",
  "timezone": "America/New_York",
  "attributes": [
    {"name": "date", "type": "text", "isPrimaryKey": true},
    {"name": "holiday_name", "type": "text"},
    {"name": "is_closed", "type": "boolean"},
    {"name": "custom_message", "type": "text"}
  ]
}
```

### Data Table Records
```json
[
  {"date": "2026-01-01", "holiday_name": "New Year's Day", "is_closed": true, "custom_message": "Happy New Year!"},
  {"date": "2026-12-25", "holiday_name": "Christmas", "is_closed": true, "custom_message": "Merry Christmas!"}
]
```

---

## 4. Routing Configuration

### Hours of Operation
```json
{
  "name": "Business Hours",
  "description": "Standard business hours",
  "timezone": "America/New_York",
  "config": [
    {"day": "MONDAY", "startTime": {"hours": 8, "minutes": 0}, "endTime": {"hours": 17, "minutes": 0}},
    {"day": "TUESDAY", "startTime": {"hours": 8, "minutes": 0}, "endTime": {"hours": 17, "minutes": 0}},
    {"day": "WEDNESDAY", "startTime": {"hours": 8, "minutes": 0}, "endTime": {"hours": 17, "minutes": 0}},
    {"day": "THURSDAY", "startTime": {"hours": 8, "minutes": 0}, "endTime": {"hours": 17, "minutes": 0}},
    {"day": "FRIDAY", "startTime": {"hours": 8, "minutes": 0}, "endTime": {"hours": 17, "minutes": 0}}
  ]
}
```

### Queues
```json
{
  "name": "General Support",
  "description": "General customer support queue",
  "hoursOfOperationId": "<hours-id>",
  "maxContacts": 10,
  "outboundCallerConfig": {
    "outboundCallerIdName": "Support",
    "outboundCallerIdNumberId": "<phone-number-id>"
  }
}
```

### Routing Profiles
```json
{
  "name": "Support Agent Profile",
  "description": "Profile for support agents",
  "defaultOutboundQueueId": "<queue-id>",
  "mediaConcurrencies": [
    {"channel": "VOICE", "concurrency": 1},
    {"channel": "CHAT", "concurrency": 3},
    {"channel": "TASK", "concurrency": 5}
  ],
  "queueConfigs": [
    {"queueId": "<queue-id>", "priority": 1, "delay": 0}
  ]
}
```

---

## 5. Customer Profiles

### Object Type Mapping
```json
{
  "objectTypeName": "CustomerOrder",
  "description": "Customer order data",
  "templateId": null,
  "expirationDays": 365,
  "allowProfileCreation": true,
  "fields": {
    "orderId": {"source": "_source.order_id", "target": "_profile.Attributes.OrderId"},
    "orderDate": {"source": "_source.order_date", "target": "_profile.Attributes.LastOrderDate"},
    "totalAmount": {"source": "_source.total", "target": "_profile.Attributes.TotalSpent"}
  },
  "keys": {
    "_email": [{"fieldNames": ["email"]}],
    "_phone": [{"fieldNames": ["phone"]}],
    "orderId": [{"fieldNames": ["orderId"]}]
  }
}
```

### Standard Profile Fields
- FirstName, LastName, MiddleName
- PhoneNumber, MobilePhoneNumber, HomePhoneNumber
- EmailAddress
- Address, City, State, PostalCode, Country
- AccountNumber
- BirthDate
- Gender

---

## 6. Amazon Q in Connect (AI)

### AI Prompts
Default prompts that can be customized:
- **QinConnectAnswerGenerationPrompt**: Generate answers from knowledge base
- **QinConnectIntentLabelingGenerationPrompt**: Identify customer intents
- **QinConnectQueryReformulationPrompt**: Search knowledge base
- **QinConnectSelfServicePreProcessingPrompt**: Determine self-service task
- **QinConnectCaseSummarizationPrompt**: Summarize cases

### AI Guardrails
- Filter harmful/inappropriate responses
- Redact sensitive PII
- Limit hallucination

### AI Agent Configuration
```json
{
  "name": "CustomSupportAgent",
  "type": "ANSWER_RECOMMENDATION",
  "configuration": {
    "answerRecommendationAIAgentConfiguration": {
      "answerGenerationAIPromptId": "<prompt-id>",
      "queryReformulationAIPromptId": "<prompt-id>"
    }
  }
}
```

---

## 7. Outbound Campaigns

### Campaign Configuration
```json
{
  "name": "Appointment Reminders",
  "connectInstanceId": "<instance-id>",
  "dialerConfig": {
    "predictiveDialerConfig": {
      "bandwidthAllocation": 0.7,
      "dialingCapacity": 0.5
    }
  },
  "outboundCallConfig": {
    "connectContactFlowId": "<flow-id>",
    "connectQueueId": "<queue-id>",
    "connectSourcePhoneNumber": "+1234567890",
    "answerMachineDetectionConfig": {
      "enableAnswerMachineDetection": true,
      "awaitAnswerMachinePrompt": false
    }
  }
}
```

### Dialer Types
1. **Predictive**: Algorithm anticipates agent availability
2. **Progressive**: Dials after agent completes call
3. **Agentless**: High-volume notifications without agents
4. **Preview**: Agent reviews info before calling

---

## 8. Infrastructure as Code

### CloudFormation Resources
Key resources for Amazon Connect IaC:
- `AWS::Connect::Instance`
- `AWS::Connect::ContactFlow`
- `AWS::Connect::Queue`
- `AWS::Connect::RoutingProfile`
- `AWS::Connect::HoursOfOperation`
- `AWS::Connect::User`
- `AWS::Connect::PhoneNumber`
- `AWS::Connect::QuickConnect`
- `AWS::Connect::Rule`
- `AWS::Connect::View`

### Sample CloudFormation Template Structure
```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: Amazon Connect Instance with basic configuration

Parameters:
  InstanceAlias:
    Type: String
    Description: Unique alias for the Connect instance

Resources:
  ConnectInstance:
    Type: AWS::Connect::Instance
    Properties:
      InstanceAlias: !Ref InstanceAlias
      IdentityManagementType: CONNECT_MANAGED
      Attributes:
        InboundCalls: true
        OutboundCalls: true
        ContactflowLogs: true
        ContactLens: true

  BusinessHours:
    Type: AWS::Connect::HoursOfOperation
    Properties:
      InstanceArn: !GetAtt ConnectInstance.Arn
      Name: BusinessHours
      TimeZone: America/New_York
      Config:
        - Day: MONDAY
          StartTime:
            Hours: 8
            Minutes: 0
          EndTime:
            Hours: 17
            Minutes: 0

  GeneralQueue:
    Type: AWS::Connect::Queue
    Properties:
      InstanceArn: !GetAtt ConnectInstance.Arn
      Name: GeneralSupport
      HoursOfOperationArn: !GetAtt BusinessHours.HoursOfOperationArn
```

---

## Default Templates for MCP Wizard

### Recommended Default Templates

#### 1. Basic Contact Center Setup
- Instance with voice/chat enabled
- Business hours (M-F 8-5)
- Single queue
- Basic routing profile
- Admin user

#### 2. Cases-Enabled Setup
- All from Basic +
- Cases domain
- General case template
- Standard case fields
- Case assignment rules

#### 3. AI-Enhanced Setup
- All from Cases +
- Amazon Q in Connect enabled
- Knowledge base integration
- Default AI prompts
- Step-by-step guides

#### 4. Full Enterprise Setup
- All from AI-Enhanced +
- Multiple queues by department
- Customer Profiles
- Contact Lens analytics
- Outbound campaigns
- Data tables for dynamic config

---

## References

- [Amazon Connect Admin Guide](https://docs.aws.amazon.com/connect/latest/adminguide/)
- [Amazon Connect API Reference](https://docs.aws.amazon.com/connect/latest/APIReference/)
- [Amazon Connect Cases API](https://docs.aws.amazon.com/cases/latest/APIReference/)
- [AWS Solutions - Connect IaC](https://github.com/aws-solutions-library-samples/guidance-for-deploying-amazon-connect-with-infrastructure-as-code-on-aws)
- [Step-by-Step Guides Interactive Docs](https://d3irlmavjxd3d8.cloudfront.net/)
