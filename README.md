# Procurement Management API

## Goal

Build a Procurement Management API while learning and applying backend engineering concepts.

Topics to practice:

* REST API design
* MVC architecture
* Database design and normalization
* ORM usage (SQLAlchemy)
* Authentication and authorization
* CRUD operations
* Dependency injection
* Service layer architecture
* Design patterns
* Database migrations
* Testing

---

## Business Overview

The system allows users to:

* Create procurement requests
* Submit requests for approval
* Approve or reject requests
* Assign suppliers
* Track request status
* Maintain approval history

---

## Architecture

### MVC

#### Model

Responsible for:

* Database schema
* ORM entities
* Relationships between entities
* Data persistence

Entities:

* User
* Supplier
* PurchaseRequest
* Approval

---

#### View

Future frontend:

* NiceGUI

Possible features:

* Login page
* Dashboard
* Create request form
* Approval queue
* Supplier management

---

#### Controller

Responsible for:

* API endpoints
* Request validation
* Calling services
* Returning responses

Examples:

* Create Request
* Update Request
* Approve Request
* Reject Request
* Get Requests

---

## Week 1 — Model Layer

### Documentation

* Define business rules
* Define requirements
* Define workflows

### Database Design

Location:

```text
database/
└── schema.dbml
```

---

## Development Roadmap

### Phase 1 — Database

* [x] Design database schema
* [ ] Create ORM models
* [ ] Create database connection
* [ ] Create migrations
* [ ] Generate database tables

### Phase 2 — Data Access

* [ ] Create repositories
* [ ] Implement CRUD operations
* [ ] Add validation

### Phase 3 — API

* [ ] Create FastAPI application
* [ ] Create routes
* [ ] Create controllers
* [ ] Add exception handling

### Phase 4 — Authentication

* [ ] User registration
* [ ] User login
* [ ] Password hashing
* [ ] JWT authentication
* [ ] Role-based authorization

### Phase 5 — Procurement Workflow

* [ ] Create request
* [ ] Submit request
* [ ] Approve request
* [ ] Reject request
* [ ] Assign supplier
* [ ] Close request

### Phase 6 — Frontend

* [ ] NiceGUI setup
* [ ] Dashboard
* [ ] Request management
* [ ] Approval management

### Phase 7 — Testing

* [ ] Unit tests
* [ ] Integration tests
* [ ] API tests

---

## Current Progress

### 
Completed:

* Readme File
* Created database schema
* Create Entities
* Created `schema.dbml`

### Next Task

Create SQLAlchemy ORM models:

- From DBML to SQLAlchemy (Pyton Code)
- Create Database file (The Engine)
- Camunda Workflow: User > Purchase request > Manager Approval > Procurement Approval > Supplier Assignment > ERP/SAP Export
- Prio:Signavioo Model: User > Purchase request > Manager Approval > Procurement Approval > Supplier Assignment > ERP/SAP Export
- Status Model API Logic: Draft > Submitted > Manager Approved > Procurement Approved > Sent to Supplier > Completed > Rejected/Cancelled


###
