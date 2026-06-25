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

### Day2:
- Create a BPMN Process diagram for validation
- Process Name: Procure to Pay (P2P) for operational process
- Idea: Buy the stuff you need right now, based on the contracts that already exist.
- Tasks: Create a request, get it approved, create a purchase order, receive the goods, pay the invoice
- Use Case: A user needs 10 chairs. He placed his request, which gets validated by a manager based on business rules. After validation, the order is sent to the supplier

### Scenario et Step by Step solution:
- Got Process as XML file from process engineers


### Step by Step Solution
1- Extract the "States" from the XML (The Status Enum) in this use case
2- Extract the "Business Rules" (The Gateways) and translate it to code: 
    <bpmn:sequenceFlow id="Flow_Gateway_High" sourceRef="Gateway_Amount" targetRef="Activity_HighValueReview">
  <bpmn:conditionExpression xsi:type="bpmn:tFormalExpression">${totalPrice > 10000}</bpmn:conditionExpression>
</bpmn:sequenceFlow>
    To
    if request.total_price > 10000:
    request.status = "pending_procurement"  # Goes to Lane 3
else:
    request.status = "pending_manager"      # Goes to Lane 2

3- Map User Tasks to API Endpoints (Controllers)
User Task (Human Action)	API Endpoint (FastAPI)
"Create Purchase Request"	POST /api/v1/requests (Creates a Draft)
"Submit for Approval"	POST /api/v1/requests/{id}/submit
"Approve or Reject" (Manager)	POST /api/v1/requests/{id}/approve
"Review High-Value" (Procurement)	POST /api/v1/requests/{id}/approve (same endpoint, but role-restricted)

4: Map the Service Task to a Background Job
The XML has:

xml
<bpmn:serviceTask id="Activity_GenerateOrder" name="Generate PO &amp; Send to Supplier" />
Translation to Code:
This is not triggered by a human. It is triggered automatically when a request is approved.
In your approve function, after setting status = "approved", you immediately call:

python
# This is the Service Task!
send_order_to_supplier(request.id)  



Completed Week 2:
- Create folder process docementation with process.cml file


### Layers Architecture:
Layer	Folder / File	What goes here?	Example from your project
Model Layer	app/models/	Database Classes (SQLAlchemy). These map 1:1 to your PostgreSQL tables. They contain zero business logic—they just define columns and relationships.	class PurchaseRequest(Base): with columns like id, title, status, total_price.
Enum Layer	app/models/enums.py	Constants & Restrictions. Ensures the database only accepts specific strings (prevents typos like "draftt").	class RequestStatus(str, Enum):
Service Layer (Business Rules)	app/services/	The Orchestrator Classes. This is where the Business Rules live. The Service takes data from the Model, applies the rules (e.g., if total_price > 10000), and saves it back.	class RequestService:
Controller Layer	app/api/v1/	The HTTP Traffic Cops. These classes (Routers) handle incoming HTTP requests, call the Service Layer, and return JSON responses. They contain zero business logic.	@router.post("/requests")


### Phase:
Design Phase (Done) → DBML, BPMN.

Model Layer (Done) → SQLAlchemy classes.

Enum Layer (In Progress) → RequestStatus.

Service Layer  → RequestService with business rules.

Controller Layer  → FastAPI endpoints.

Testing  → Postman or pytest

### Done

Create SQLAlchemy ORM models:

- Prio:Signavioo Model: User > Purchase request > Manager Approval > Procurement Approval > Supplier Assignment > ERP/SAP Export
- From DBML to SQLAlchemy (Pyton Code)
- Create Database file (The Engine)
- XML FIle of the process
- Status Model API Logic: Draft > Submitted > Manager Approved > Procurement Approved > Sent to Supplier > Completed > Rejected/Cancelled
- Business Rules Engine:
- Auto-routing based on amount
- Supplier-based rules
- Department-based approvals
- SAP sync conditions
- How do CRUD applied here ?: CRUD is a basic concept in backend development. It stands for:

Create → add new data (e.g., create a new user)
Read → get or view data (e.g., load a user profile)
Update → change existing data (e.g., edit your email)
Delete → remove data (e.g., delete your account)

###
Learning and Best practices: 
- The RequestService is the bridge between the outside world (your HTTP API) and the Database
- RequestService = Business Logic Orchestrator.
- Group by Domain (Subject). If it's about "Requests", put it in RequestService. If it's about "Users", create UserService
- New rule about Requests (e.g., "If total > 5000, require a second manager signature").	Add a new method to RequestService.
New rule about Sending Orders (e.g., "If supplier is not in our DB, raise an error").	Add a new method (e.g., send_order_to_supplier) inside RequestService OR create a new service called SupplierService or OrderService if it gets complex.
New rule about Users (e.g., "Users must reset passwords every 90 days").	Create a new service called UserService.
In short: Group by Domain (Subject). If it's about "Requests", put it in RequestService. If it's about "Users", create UserService
- This only is a function "def submit_for_approval(...)" but in this case it is inside a class and is a method
- the Service Layer is the Enforcer of access
- The Model (User table): Stores the user's role (role = "manager").
- The Service Layer: Checks the user's role and decides if they are allowed to proceed
- Where else do we use Enums?
- Enums to enumarate descriptions and conditions go into service
-  Model Architecture contains: UsersTable, StatusTable, 
-  Users.py Table attributes must match dbml structure

UserRole (requester, manager, procurement, admin).

ApprovalDecision (approved, rejected, pending).

SupplierStatus (onboarded, pending_review, blocked).
- Create database:
- Postgresql or sqllite connect with this code: from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite runs entirely in a file called "procurement.db" in your project root.
# No Docker. No PostgreSQL server.
SQLALCHEMY_DATABASE_URL = "sqlite:///./procurement.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
### To Do
Install PostgreSQL
