# SupportPilot AI — System Design

**Version:** 1.0  
**Domain:** E-commerce Customer Support  
**Architecture:** Modular Monolith

---

## 1. System Overview

SupportPilot AI is an AI-powered customer support automation platform for e-commerce businesses.

The system allows businesses to provide support policies and customer/order data. Customers can submit support requests, and the platform can understand the request, retrieve relevant information, generate a response, and perform controlled support actions when authorized.

The initial architecture is a **modular monolith** built around a FastAPI backend.

---

## 2. Architecture Goals

The system is designed to provide:

- Reliable access to structured business data
- Grounded answers from company policies
- Controlled AI-driven actions
- Authentication and authorization
- Conversation state management
- Guardrails and safe failure behavior
- Auditability
- Monitoring and observability
- Maintainable and extensible code

---

## 3. High-Level Architecture

```text
                         ┌─────────────────┐
                         │     Customer    │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │    Frontend     │
                         │   Streamlit     │
                         └────────┬────────┘
                                  │ HTTPS
                                  ▼
                    ┌──────────────────────────┐
                    │        FastAPI           │
                    │        Backend           │
                    └────────────┬─────────────┘
                                 │
             ┌───────────────────┼────────────────────┐
             │                   │                    │
             ▼                   ▼                    ▼
      Authentication      Conversation         Business Logic
      & Authorization       Management                │
                                                     │
                                      ┌──────────────┼──────────────┐
                                      │              │              │
                                      ▼              ▼              ▼
                                 PostgreSQL        RAG           LLM
                                      │              │              │
                                      │              │              ▼
                                      │              │          Agent
                                      │              │              │
                                      │              │       ┌──────┴──────┐
                                      │              │       ▼             ▼
                                      │              │   get_order   create_ticket
                                      │              │       │             │
                                      └──────────────┴───────┴─────────────┘
                                                                    │
                                                                    ▼
                                                               Guardrails
                                                                    │
                                                                    ▼
                                                              Audit/Monitoring
```

---

## 4. Major Components

### 4.1 Frontend

The initial frontend will use **Streamlit**.

Responsibilities:

- Customer support chat interface
- Display AI responses
- Display conversation history
- Display relevant ticket information
- Provide a basic business/admin interface where required

The frontend communicates with the backend through HTTP APIs.

---

### 4.2 FastAPI Backend

FastAPI is the primary backend/API layer.

Responsibilities:

- Expose REST APIs
- Validate incoming requests
- Authenticate users
- Authorize operations
- Coordinate application services
- Return API responses
- Handle API-level errors

The backend will be organized into clear modules rather than one large application file.

---

### 4.3 Authentication and Authorization

Authentication determines **who the user is**.

Authorization determines **what the user is allowed to do**.

The system will use JWT-based authentication initially.

Example roles:

```text
CUSTOMER
SUPPORT_AGENT
BUSINESS_ADMIN
```

Authorization will be enforced by the application rather than delegated to the LLM.

---

### 4.4 Business Logic Layer

The business logic layer contains application and domain rules.

Examples:

- Verify that an order belongs to the customer
- Determine whether an operation is permitted
- Validate ticket creation
- Apply business rules
- Coordinate database operations

This layer is intentionally independent from the LLM.

---

### 4.5 PostgreSQL

PostgreSQL is the primary structured-data store.

Initial entities include:

```text
Businesses
Users
Customers
Products
Orders
Order Items
Support Tickets
Conversations
Messages
Audit Logs
```

PostgreSQL is the authoritative source for structured business information.

Examples:

- Order status
- Customer information
- Product information
- Ticket status
- Conversation records

---

### 4.6 RAG Pipeline

The RAG subsystem provides access to company support policies.

Conceptual flow:

```text
Policy Documents
      ↓
Document Processing
      ↓
Chunking
      ↓
Embeddings
      ↓
Vector Storage
      ↓
Similarity Search
      ↓
Relevant Policy Context
```

The initial vector storage technology will be **pgvector**, integrated with PostgreSQL.

RAG is responsible for retrieving relevant company knowledge. It does not replace the transactional database.

---

### 4.7 Language Model

The LLM is responsible for language understanding and generation.

Potential responsibilities:

- Intent identification
- Entity extraction
- Natural-language reasoning
- Response generation
- Tool selection/request generation

The application will treat the LLM as a reasoning/generation component rather than the source of truth for business data.

The LLM provider will be configurable.

---

### 4.8 Agent Orchestration

The agent coordinates multi-step support workflows.

Conceptual flow:

```text
User Request
     ↓
Understand Request
     ↓
Retrieve Information
     ↓
Reason
     ↓
Select Tool if Required
     ↓
Validate Action
     ↓
Execute Tool
     ↓
Generate Response
```

The agent will not receive unrestricted database access.

---

### 4.9 Tool Layer

Tools expose controlled application capabilities to the agent.

Initial tools may include:

```text
get_order()
get_ticket()
create_support_ticket()
update_support_ticket()
```

A tool request must pass application validation and authorization before execution.

---

### 4.10 Guardrails

Guardrails provide safety and reliability controls.

They may validate:

- Tool arguments
- User permissions
- Tenant boundaries
- Required information
- Allowed actions
- Business rules
- Model outputs

The system should fail safely rather than perform an unsupported action.

---

### 4.11 Audit Logging

Important actions will be recorded.

Examples:

```text
Request received
Database operation
Policy retrieved
Tool requested
Tool executed
Ticket created
Authorization denied
Error occurred
```

Audit records should provide enough information to understand what happened without unnecessarily storing sensitive data.

---

### 4.12 Monitoring and Observability

Monitoring will help identify:

- API errors
- Database failures
- LLM failures
- Tool failures
- Request latency
- RAG retrieval issues
- Unexpected behavior

Detailed monitoring will be implemented in a later phase.

---

## 5. Request Flow — Informational Query

Example:

> "Where is my order #48291?"

```text
Customer
   ↓
Frontend
   ↓
FastAPI
   ↓
Authentication
   ↓
Conversation State
   ↓
Request Understanding
   ↓
Order Service
   ↓
PostgreSQL
   ↓
Verified Order Information
   ↓
Response Generation
   ↓
Customer
```

The order status comes from PostgreSQL, not from the LLM's internal knowledge.

---

## 6. Request Flow — Policy Query

Example:

> "Can I return an item after 25 days?"

```text
Customer
   ↓
Frontend
   ↓
FastAPI
   ↓
Authentication
   ↓
Conversation State
   ↓
RAG Retrieval
   ↓
Relevant Policy Chunks
   ↓
LLM
   ↓
Grounded Response
   ↓
Customer
```

The response should be grounded in the business's uploaded policy.

---

## 7. Request Flow — Action Query

Example:

> "My order #48291 arrived damaged. Please create a support ticket."

```text
Customer
   ↓
Frontend
   ↓
FastAPI
   ↓
Authentication
   ↓
Conversation State
   ↓
Agent
   ↓
Get Order Tool
   ↓
PostgreSQL
   ↓
RAG Policy Retrieval
   ↓
Agent Decision
   ↓
Guardrails
   ↓
Authorization
   ↓
Create Ticket Tool
   ↓
PostgreSQL
   ↓
Audit Log
   ↓
Response Generation
   ↓
Customer
```

---

## 8. Data Flow

SupportPilot AI has three major information flows.

### Structured Business Data

```text
PostgreSQL
    ↓
Customers
Orders
Products
Tickets
Conversations
```

### Unstructured Business Knowledge

```text
Policy Documents
      ↓
RAG
      ↓
Relevant Policy Context
```

### AI Reasoning and Generation

```text
User Request
     +
Structured Information
     +
Retrieved Policy
     ↓
    LLM
     ↓
Response / Tool Request
```

---

## 9. Source-of-Truth Strategy

Different components have different responsibilities.

| Information | Source of Truth |
|---|---|
| Customer data | PostgreSQL |
| Order data | PostgreSQL |
| Product data | PostgreSQL |
| Ticket data | PostgreSQL |
| Conversation records | PostgreSQL |
| Company policies | Uploaded policy documents |
| Retrieved policy context | RAG |
| Natural-language response | LLM |

The LLM must not invent authoritative business information.

---

## 10. Multi-Tenancy

SupportPilot AI is designed for multiple businesses.

Conceptually:

```text
Business A
 ├── Customers
 ├── Orders
 ├── Tickets
 └── Policies

Business B
 ├── Customers
 ├── Orders
 ├── Tickets
 └── Policies
```

Tenant isolation is required so that one business cannot access another business's data.

The initial implementation will use a shared PostgreSQL database with tenant/business identifiers on relevant records.

Tenant isolation will be enforced at the application and authorization layers.

---

## 11. Trust Boundaries

The LLM is not trusted with unrestricted access to business systems.

The intended action flow is:

```text
LLM
 ↓
Tool Request
 ↓
Guardrails
 ↓
Authorization
 ↓
Business Logic
 ↓
Tool Execution
 ↓
Database
```

An LLM-generated request is therefore **not equivalent to permission**.

---

## 12. Architecture Style

### Modular Monolith

The initial backend will be deployed as one application while maintaining internal module boundaries.

### Docker-First Development

SupportPilot AI will use a **Docker-first development approach** from Phase 2 onward.

Instead of relying on a project-specific local Python environment as the primary runtime, the application and its supporting services will be developed and run through Docker.

The initial local development environment will be structured around Docker Compose:

```text
Docker Compose
      │
      ├── FastAPI Backend
      ├── PostgreSQL
      └── Frontend
```

Benefits of this approach include:

- Consistent development environments
- Reproducible dependencies
- Easier PostgreSQL setup
- Reduced "works on my machine" problems
- A smoother transition from local development to deployment

The actual container configuration will be introduced during **Phase 2 — Project Setup** and refined during **Phase 16 — Docker Containerization**.

Conceptual structure:

```text
FastAPI Application
│
├── API Layer
├── Authentication
├── Business Logic
├── Data Access
├── Conversation Management
├── RAG
├── LLM Integration
├── Tools
├── Agent Orchestration
├── Guardrails
└── Audit / Monitoring
```

This approach keeps initial development and deployment manageable while allowing future extraction of independently scalable components if needed.

---

## 13. Technology Stack

| Layer | Technology |
|---|---|
| Backend | Python + FastAPI |
| Database | PostgreSQL |
| Database access | SQLAlchemy + psycopg |
| Vector search | pgvector |
| Authentication | JWT |
| Frontend | Streamlit |
| LLM | Configurable provider |
| Embeddings | Configurable embedding model |
| Containerization | Docker |
| Local orchestration | Docker Compose |
| Deployment | Render |
| Version control | Git + GitHub |

---

## 14. Key Architecture Decisions

### ADR-01 — Use a Modular Monolith

**Decision:** Start with a modular monolith.

**Reason:** The project has manageable initial complexity. This provides clean separation without introducing unnecessary microservice operational overhead.

---

### ADR-02 — PostgreSQL as Primary Database

**Decision:** Use PostgreSQL.

**Reason:** It provides strong relational modeling, transactions, mature SQL support, and can also support vector search through pgvector.

---

### ADR-03 — Use pgvector for Initial RAG Storage

**Decision:** Use pgvector alongside PostgreSQL.

**Reason:** It keeps structured business data and initial vector search infrastructure within a familiar database ecosystem and reduces infrastructure complexity.

---

### ADR-04 — LLM Does Not Directly Access the Database

**Decision:** Database access occurs through application services/tools.

**Reason:** This provides validation, authorization, predictable business rules, and auditability.

---

### ADR-05 — Configurable AI Providers

**Decision:** Avoid tightly coupling the application to one LLM or embedding provider.

**Reason:** Providers can change, and abstraction makes experimentation and future migration easier.

---

## 15. Reliability Strategy

The system should prefer safe failure over unsupported automation.

Examples:

```text
Missing order ID
      ↓
Ask customer for order information
```

```text
Order not found
      ↓
Do not fabricate order information
```

```text
Tool failure
      ↓
Do not claim the action succeeded
```

```text
Insufficient policy information
      ↓
Avoid unsupported policy claims
```

```text
Unauthorized action
      ↓
Reject the action
```

---

## 16. Scalability Direction

The first implementation will remain a modular monolith.

If usage increases, components can later be separated based on actual bottlenecks.

Potential future candidates:

```text
Document Processing Worker
RAG Service
Agent Service
Notification Service
Analytics Service
```

We will not introduce these services until there is a concrete requirement.

---

## 17. Security Principles

The system will follow these principles:

- Never expose database credentials to the frontend.
- Store secrets in environment variables.
- Authenticate protected API requests.
- Authorize operations based on user roles and tenant.
- Validate all external input.
- Prevent cross-tenant data access.
- Restrict agent tools.
- Log security-sensitive events.
- Avoid unnecessary storage of sensitive information.

---

## 18. Phase Mapping

The architecture will be implemented progressively:

```text
Phase 2  → Docker-First Project Setup
Phase 3  → PostgreSQL Database Design
Phase 4  → SQL Layer + Database Connection
Phase 5  → FastAPI Backend
Phase 6  → Orders + Tickets Business Logic
Phase 7  → Authentication + Authorization
Phase 8  → Conversation State
Phase 9  → RAG
Phase 10 → LLM Integration
Phase 11 → Tool Calling
Phase 12 → Agent Orchestration
Phase 13 → Guardrails + Reliability
Phase 14 → Audit Logs + Monitoring
Phase 15 → Testing
Phase 16 → Docker
Phase 17 → Deployment
```

---

## 19. Final Architecture Summary

SupportPilot AI will initially use a **Docker-first modular monolithic architecture** with:

```text
Streamlit
    ↓
FastAPI
    ↓
Authentication / Authorization
    ↓
Business Logic
    ↓
PostgreSQL
    │
    ├── Structured Business Data
    │
    └── pgvector
           ↑
           │
       RAG Pipeline
           ↑
           │
    Policy Documents

FastAPI
    ↓
LLM
    ↓
Agent
    ↓
Controlled Tools
    ↓
Guardrails + Authorization
    ↓
Business Logic
    ↓
PostgreSQL

All important actions
    ↓
Audit Logs
    ↓
Monitoring
```

This architecture provides a foundation for building SupportPilot AI incrementally while keeping business data authoritative, AI capabilities controlled, and the system explainable and auditable.
