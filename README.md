# Intelligent IVR with Amazon Connect, Lex, and Lambda

[![AWS](https://img.shields.io/badge/AWS-Amazon%20Connect%20%7C%20Lex%20%7C%20Lambda-orange?style=flat-square&logo=amazon-aws)](https://aws.amazon.com/)
[![Terraform](https://img.shields.io/badge/Infrastructure-Terraform-blueviolet?style=flat-square&logo=terraform)](https://www.terraform.io/)

This project demonstrates a production-ready **Intelligent IVR (Interactive Voice Response)** solution built on Amazon Connect. It leverages Natural Language Understanding (NLU) via Amazon Lex to recognize caller intent and AWS Lambda to integrate with business logic and customer data stored in DynamoDB.

---

## 🏢 Business Problem

Traditional IVRs often rely on rigid "press 1 for X" menus that lead to high customer frustration and poor first-contact resolution. Modern customers expect a more conversational, intuitive experience.

**The Goal:** Build an IVR that understands natural speech, personalizes the experience based on caller history, and routes callers to the most qualified agent with zero manual input.

---

## 🏗️ Architecture

![Architecture Diagram](architecture/diagram.png) *(Placeholder: Diagram includes Connect, Lex, Lambda, and DynamoDB flow)*

1.  **Entry Point:** The caller dials the Amazon Connect number.
2.  **Customer Lookup:** An AWS Lambda function searches for the caller's phone number in a DynamoDB table (Mock CRM).
3.  **Personalized Greeting:** Connect uses the retrieved name to greet the customer.
4.  **Intent Recognition:** Amazon Lex listens to the customer's request (e.g., "I want to check my account balance").
5.  **Dynamic Routing:** Based on the Lex intent and the customer's membership level (e.g., Platinum vs. Bronze), a Lambda function decides the optimal queue and priority.
6.  **Agent Delivery:** The call is routed to an agent or a specialized queue with all previous context available.

---

## 🧩 Key Components

### 1. Amazon Lex Bot Design
The bot is configured with three primary intents:
- **`CheckBalance`**: Uses slots to identify which account type the user is asking about.
- **`UpdateMembership`**: Handles requests to change membership tiers.
- **`SpeakToAgent`**: A priority intent that bypasses automation when a caller shows high frustration or explicitly asks for a human.
- **`FallbackIntent`**: Handles low-confidence recognition by offering to repeat or transferring to a general agent.

### 2. AWS Lambda Functions
- **`customer-lookup`**: Queries DynamoDB using `ContactData.CustomerEndpoint.Address`. Returns name and membership tier.
- **`routing-logic`**: Evaluates the combination of Lex Intent and Membership Tier to set `QueueName` and `RoutingPriority` attributes in the Connect flow.

### 3. Amazon Connect Contact Flow
- **Error Handling**: Every Lambda call includes a "Success" and "Error/No Match" path.
- **Business Hours**: A "Check Hours" block ensures callers are routed to an after-hours message or external support if the center is closed.
- **Fallback Logic**: If Lex fails twice or Lambda times out, the call is immediately transferred to a "Safety Queue" to ensure no customer is left stuck.

---

## 🚀 Deployment

### Prerequisites
- AWS Account with Amazon Connect instance created.
- Terraform installed locally.

### Infrastructure Setup
1.  Navigate to the `terraform/` directory.
2.  Run `terraform init` and `terraform apply`.
3.  Upload the generated Lambda code (or zip the local files) to AWS.

### Amazon Connect Integration
1.  Add the `IVR-Customer-Lookup` and `IVR-Routing-Logic` Lambda functions to your Connect instance settings.
2.  Import the Lex bot provided in the `lex-bot/` (if exported) or manually create intents.
3.  Import the `intelligent-ivr-flow.json` into your Contact Flows.

---

## 🛡️ Best Practices & Trade-offs

-   **Security**: IAM roles follow the principle of least privilege, granting access only to specific DynamoDB tables.
-   **Resilience**: The IVR is designed with a "Default-to-Agent" philosophy. If any integration fails, the caller is sent to a human rather than being disconnected.
-   **Cost-Efficiency**: Uses Serverless components (Lambda, Lex, DynamoDB) to ensure costs only scale with usage.
-   **Trade-offs**: For this portfolio version, DynamoDB is used as a mock CRM. In a real-world enterprise, this would be replaced with a secure API call to Salesforce or a legacy backend system.

---

## 📈 Future Improvements
- [ ] **Sentiment Analysis**: Use Amazon Comprehend to detect caller frustration in real-time.
- [ ] **Proactive Notifications**: Send a follow-up SMS via Amazon Pinpoint after the call.
- [ ] **Voice Biometrics**: Integrate Amazon Connect Voice ID for secure authentication.

---

*This project is provided for example and demonstration purposes only.*
