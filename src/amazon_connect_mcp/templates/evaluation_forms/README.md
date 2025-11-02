# Amazon Connect Evaluation Forms Templates

This directory contains industry-specific evaluation form templates for Amazon Connect quality management and agent performance scoring.

## Overview

These templates are designed based on Amazon Connect best practices for quality management, incorporating industry-specific criteria and scoring methodologies. Each template uses a question-only scoring strategy with weighted sections to provide comprehensive agent performance evaluation.

## Available Templates

### General Evaluation (`general_evaluation.json`)
- **Use Case**: Universal template suitable for any industry
- **Sections**: Opening & Customer ID, Communication Skills, Problem Resolution, Product Knowledge, Call Closing
- **Focus**: Core customer service skills and professional standards

### Healthcare Evaluation (`healthcare_evaluation.json`)
- **Use Case**: Healthcare customer service and patient support
- **Key Focus Areas**:
  - HIPAA Compliance & Privacy (25%)
  - Clinical Communication & Accuracy (25%)
  - Empathy & Patient Care (20%)
  - Communication & Professionalism (20%)
  - Problem Resolution & Follow-up (10%)
- **Special Considerations**: Patient privacy, clinical boundaries, empathy requirements

### Financial Services Evaluation (`financial_services_evaluation.json`)
- **Use Case**: Banking, insurance, and financial services
- **Key Focus Areas**:
  - Regulatory Compliance & Security (30%)
  - Financial Accuracy & Knowledge (25%)
  - Customer Trust & Relationship (20%)
  - Communication & Professionalism (15%)
  - Problem Resolution & Follow-up (10%)
- **Special Considerations**: Regulatory compliance, fraud prevention, trust building

### E-Commerce/Retail Evaluation (`ecommerce_retail_evaluation.json`)
- **Use Case**: Online retail, e-commerce, and retail customer service
- **Key Focus Areas**:
  - Product Knowledge & Information (25%)
  - Order Management & Processing (30%)
  - Customer Experience & Satisfaction (20%)
  - Communication & Efficiency (15%)
  - Problem Resolution & Value Addition (10%)
- **Special Considerations**: Order tracking, returns processing, upselling appropriateness

### Telecommunications Evaluation (`telecommunications_evaluation.json`)
- **Use Case**: Telecom, ISP, and network service providers
- **Key Focus Areas**:
  - Technical Knowledge & Troubleshooting (30%)
  - Service & Account Management (25%)
  - Outage & Emergency Response (20%)
  - Communication & Customer Education (15%)
  - Problem Resolution & Follow-up (10%)
- **Special Considerations**: Technical troubleshooting, outage management, service changes

### Technology/SaaS Evaluation (`technology_saas_evaluation.json`)
- **Use Case**: Software companies, SaaS providers, and technical support
- **Key Focus Areas**:
  - Technical Expertise & Problem Solving (35%)
  - Product Knowledge & Documentation (25%)
  - Customer Education & Empowerment (20%)
  - Communication & Collaboration (12%)
  - Issue Resolution & Follow-up (8%)
- **Special Considerations**: Technical depth, code accuracy, knowledge transfer

## Template Structure

Each evaluation form follows the Amazon Connect evaluation form schema:

```json
{
  "EvaluationFormTitle": "Form Name",
  "Description": "Form description",
  "ScoringStrategy": {
    "Mode": "QUESTION_ONLY",
    "Status": "ENABLED"
  },
  "Items": [
    {
      "Section": {
        "Title": "Section Name",
        "RefId": "section_id",
        "Instructions": "Section instructions",
        "Weight": 25.0,
        "Items": [
          {
            "Question": {
              "Title": "Question Title",
              "Instructions": "Question instructions",
              "RefId": "question_id",
              "QuestionType": "SINGLESELECT",
              "QuestionTypeProperties": {
                "Options": [
                  {"Text": "Option text", "Score": 5}
                ],
                "DisplayAs": "DROPDOWN"
              },
              "Weight": 40.0
            }
          }
        ]
      }
    }
  ]
}
```

## Scoring System

All templates use a 5-point scoring scale:
- **5 - Excellent**: Exceeds expectations, exemplary performance
- **4 - Good**: Meets expectations with minor areas for improvement
- **3 - Satisfactory**: Meets basic requirements
- **2 - Needs Improvement**: Below expectations, requires coaching
- **1 - Unsatisfactory**: Significantly below expectations, requires immediate attention

## Weight Distribution

Each template uses weighted sections to reflect industry priorities:
- **Section weights** determine the relative importance of different evaluation areas
- **Question weights** within sections determine the relative importance of specific criteria
- Total section weights sum to 100%

## Implementation

### Using with Amazon Connect

1. **Create Evaluation Form**:
   ```python
   # Use the analytics_create_evaluation_form tool (if available)
   # Or manually create through AWS Console/API
   ```

2. **Customize for Your Organization**:
   - Modify question text to match your terminology
   - Adjust weights based on your priorities
   - Add or remove questions as needed
   - Update scoring criteria to match your standards

3. **Deploy and Train**:
   - Deploy forms to your Amazon Connect instance
   - Train quality analysts on scoring criteria
   - Establish calibration sessions for consistency

### Customization Guidelines

- **Industry Adaptation**: Modify questions to reflect your specific industry requirements
- **Compliance Requirements**: Add questions for industry-specific compliance needs
- **Company Values**: Incorporate your organization's values and service standards
- **Performance Metrics**: Align scoring with your KPIs and performance goals

## Best Practices

### Quality Management
- **Calibration Sessions**: Regular sessions to ensure consistent scoring
- **Feedback Loops**: Use evaluation results for targeted coaching
- **Trend Analysis**: Monitor scores over time to identify improvement areas
- **Agent Development**: Use results for personalized development plans

### Scoring Consistency
- **Clear Criteria**: Ensure scoring criteria are specific and measurable
- **Regular Training**: Train evaluators on consistent application of criteria
- **Inter-rater Reliability**: Monitor consistency between different evaluators
- **Documentation**: Maintain detailed notes to support scoring decisions

### Continuous Improvement
- **Regular Reviews**: Periodically review and update evaluation criteria
- **Agent Feedback**: Incorporate agent feedback on evaluation fairness
- **Performance Correlation**: Analyze correlation between scores and business outcomes
- **Industry Updates**: Update forms to reflect changing industry standards

## Integration with Amazon Connect

These templates integrate with Amazon Connect's quality management features:

- **Contact Evaluations**: Use with `analytics_start_contact_evaluation`
- **Evaluation Forms**: Manage with `analytics_list_evaluation_forms`
- **Performance Analytics**: Combine with historical metrics for comprehensive analysis
- **Agent Coaching**: Use results to drive targeted coaching sessions

## Support and Customization

For additional customization or industry-specific requirements:
1. Review the base templates for structure and best practices
2. Modify questions and weights to match your specific needs
3. Test with a small group before full deployment
4. Establish clear scoring guidelines and training materials
5. Monitor results and adjust as needed

## Compliance Considerations

- **Data Privacy**: Ensure evaluation data handling complies with privacy regulations
- **Industry Regulations**: Incorporate industry-specific compliance requirements
- **Documentation**: Maintain proper documentation for audit purposes
- **Access Controls**: Implement appropriate access controls for evaluation data