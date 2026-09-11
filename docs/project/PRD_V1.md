# SupportPilot AI — Product Requirements Document

**Version:** 1.0  
**Domain:** E-commerce customer support  
**Project type:** AI-powered customer support automation platform

---

## 1. Product Overview

**SupportPilot AI** is an AI-powered customer support automation platform for e-commerce businesses.

Businesses can provide their **support policies** and connect their **customer/order data**. Customers can then submit support requests, and SupportPilot AI can:

- understand the customer's request,
- retrieve relevant customer/order information,
- retrieve relevant company policies,
- generate an appropriate response,
- perform approved support actions through controlled tools,
- and record important actions for auditing.

The system is designed around **controlled AI automation**, rather than allowing an LLM to directly modify business data.

---

## 2. Problem Statement

E-commerce support agents often spend significant time performing repetitive tasks:

- looking up orders,
- checking delivery status,
- reading return/refund policies,
- determining eligibility,
- answering common questions,
- creating support tickets,
- and recording support activity.

This creates unnecessary manual work and can lead to inconsistent responses.

SupportPilot AI aims to automate suitable parts of this workflow while keeping business data, permissions, and actions under controlled application logic.

---

## 3. Product Goal

The primary goal is:

> **To automate repetitive e-commerce customer-support workflows using AI while maintaining reliable data retrieval, controlled actions, security, and auditability.**

---

## 4. Target Users

### Customer

Can:

- submit support requests,
- ask about orders,
- ask policy-related questions,
- continue conversations,
- receive responses,
- receive ticket information.

### Support Agent

Can:

- view customer conversations,
- view order information,
- view support tickets,
- review AI interactions,
- intervene when necessary.

### Business Administrator

Can:

- manage business information,
- manage support policies,
- manage customer/order data,
- manage users and permissions,
- review audit logs.

---

## 5. Core User Journey

Example:

> "My order #48291 arrived damaged. Can I get a replacement?"

SupportPilot AI should process this approximately as:

```text
Customer Request
       ↓
Understand Request
       ↓
Identify Order
       ↓
Retrieve Order Data
       ↓
Retrieve Relevant Policy
       ↓
Determine Applicable Response
       ↓
Decide Whether Action Is Required
       ↓
Call Authorized Tool
       ↓
Create Support Ticket
       ↓
Generate Customer Response
       ↓
Record Audit Event
```

---

## 6. Functional Requirements

### FR-01 — Business Management

The system shall support business/workspace creation and configuration.

### FR-02 — Policy Management

Authorized administrators shall be able to upload company support-policy documents.

Examples:

- Return Policy
- Refund Policy
- Shipping Policy
- Cancellation Policy
- Warranty Policy

### FR-03 — Customer Management

The system shall maintain customer information.

### FR-04 — Order Management

The system shall maintain order information, including relevant order status and delivery information.

### FR-05 — Support Requests

Customers shall be able to submit support requests.

### FR-06 — Request Understanding

The system shall identify relevant information from incoming requests, such as:

```text
Intent
Order ID
Requested action
Relevant entities
```

Example:

```text
"My order 48291 arrived damaged."

Intent = DAMAGED_ORDER
Order ID = 48291
```

### FR-07 — Structured Data Retrieval

The system shall retrieve authoritative customer/order information from PostgreSQL.

### FR-08 — Policy Retrieval

The system shall retrieve relevant information from company policy documents.

### FR-09 — AI Response Generation

The system shall generate customer-facing responses using retrieved information.

### FR-10 — Controlled Actions

The system shall support approved actions through explicitly defined tools.

Initial example:

```text
create_support_ticket()
```

### FR-11 — Authentication

The system shall authenticate users before accessing protected resources.

### FR-12 — Authorization

The system shall restrict operations according to user roles and permissions.

### FR-13 — Conversation State

The system shall maintain relevant context across multiple messages in a conversation.

### FR-14 — Guardrails

The system shall prevent unsupported or unauthorized actions.

### FR-15 — Audit Logging

Important system and business actions shall be recorded.

### FR-16 — Failure Handling

The system shall handle cases such as:

- missing order information,
- unavailable policy information,
- database failures,
- LLM failures,
- tool failures,
- unauthorized actions.

---

## 7. Non-Functional Requirements

### Security

Sensitive credentials and customer information must be protected.

### Reliability

Failures should result in safe behavior rather than fabricated information or unauthorized actions.

### Maintainability

The system should use modular components with clear responsibilities.

### Scalability

The architecture should allow the number of businesses, customers, conversations and documents to grow.

### Observability

System behavior and failures should be traceable.

### Auditability

Important actions should have an identifiable history.

### Performance

The system should provide customer responses within a reasonable response time.

---

## 8. AI Design Principles

### Principle 1 — Database is the source of truth for structured data

The LLM must not invent:

- order status,
- customer information,
- payment information,
- delivery information.

Those should come from the application/database.

### Principle 2 — Company policies come from the company's documents

Policy-related answers should be grounded in retrieved company documents.

### Principle 3 — LLM does not directly control the database

The LLM can request a tool/action, but application logic decides whether that action is allowed.

### Principle 4 — Actions require authorization

For example:

```text
LLM
 ↓
"Create ticket"
 ↓
Application validates request
 ↓
Authorization check
 ↓
Tool execution
 ↓
Database update
```

### Principle 5 — Important actions are auditable

We should be able to determine:

```text
Who?
What?
When?
Why?
Which customer?
Which order?
Which tool?
What result?
```

---

## 9. MVP Scope

The first complete version will support:

### Customer

- Submit support requests
- Continue conversations
- Receive AI responses

### Business

- Customers
- Orders
- Support tickets
- Policy documents

### AI

- Request understanding
- PostgreSQL retrieval
- RAG
- LLM integration
- Tool calling
- Controlled ticket creation

### Platform

- Authentication
- Authorization
- Conversation state
- Guardrails
- Audit logging
- Testing
- Docker
- Deployment

---

## 10. Out of Scope

For the initial version:

- Payment processing
- Real shipping-provider integrations
- WhatsApp integration
- Voice support
- Full Zendesk replacement
- Kubernetes
- Multi-region infrastructure
- Custom LLM training/fine-tuning

These can be future extensions.

---

## 11. Success Criteria

SupportPilot AI will be considered successful when a customer can submit a request such as:

> **"My order #48291 arrived damaged. Can I get a replacement?"**

and the system can:

1. Understand the request.
2. Identify the order.
3. Retrieve the actual order information.
4. Retrieve the relevant company policy.
5. Determine the appropriate response.
6. Decide whether an action is permitted.
7. Create a support ticket through an authorized tool when appropriate.
8. Respond to the customer.
9. Record the important events in an audit log.

---

## 12. Future Architecture Direction

We are deliberately designing toward:

```text
Customer
   │
   ▼
Frontend
   │
   ▼
FastAPI
   │
   ▼
Application / Business Logic
   │
   ├──────────────► PostgreSQL
   │
   ├──────────────► RAG / Vector Search
   │
   ├──────────────► LLM
   │
   └──────────────► Authorized Tools
                           │
                           ▼
                     Business Actions
                           │
                           ▼
                       Audit Log
```

**This is not the final system design.** Phase 1 will turn these requirements into the detailed technical architecture.

---

## 13. Project Roadmap

SupportPilot AI will be developed through the following phases:

1. PRD
2. System Design
3. Project Setup
4. PostgreSQL Database Design
5. SQL Layer + Database Connection
6. FastAPI Backend
7. Orders + Tickets Business Logic
8. Authentication + Authorization
9. Conversation State Management
10. RAG Pipeline
11. Language Model Integration
12. Tool Calling
13. Agent Orchestration
14. Guardrails + Reliability
15. Audit Logs + Monitoring
16. Testing
17. Docker Containerization
18. Deployment
19. Documentation
20. Interview Preparation

Each phase will follow:

> **Theory → Design → Implementation → Testing → Debugging → Explanation → Interview Questions**
