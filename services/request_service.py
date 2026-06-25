# =========================================================
# FILE: app/services/request_service.py
# =========================================================

# 1. IMPORTS (External dependencies)
import enum

from httpcore import request
from huggingface_hub import User
from sqlalchemy.orm import Session
from app.models.purchase_request import PurchaseRequest
from app.models.enums import RequestStatus

# =========================================================
# 2. CLASS: RequestService
#    Purpose: This is the "SERVICE LAYER".
#    It groups ALL business rules related to Purchase Requests.
# =========================================================
class RequestService:

    # =========================================================
    # 3. METHOD: submit_for_approval
    #    Type: @staticmethod (we call it directly on the class)
    #    Purpose: This FUNCTION implements the "Submit" workflow.
    #    Parameters:
    #       - db: The database session (to talk to SQLAlchemy)
    #       - request_id: The ID of the request to submit
    #    Returns: The updated PurchaseRequest object
    # =========================================================
    @staticmethod
    def submit_for_approval(db: Session, request_id: int):
        
        # =========================================================
        # 4. DATABASE QUERY (Reading data)
        #    .query(PurchaseRequest) -> Tells SQLAlchemy which table
        #    .filter(...)           -> Adds a WHERE clause
        #    .first()               -> Executes the query and returns 1 row
        #    This is NOT a condition. This is a "READ" operation.
        # =========================================================
        request = db.query(PurchaseRequest).filter(PurchaseRequest.id == request_id).first()
        
        # =========================================================
        # 5. BUSINESS RULE 1 (CONDITION)
        #    Check: Is the request in DRAFT status?
        #    If NOT, raise an error. (This blocks the flow).
        # =========================================================
        if request.status != RequestStatus.DRAFT:
            raise ValueError("Only draft requests can be submitted.")
        
        # =========================================================
        # 6. BUSINESS RULE 2 (CONDITION)
        #    Check: Does the request have a supplier selected?
        #    If NOT, raise an error.
        # =========================================================
        if not request.supplier_id:
            raise ValueError("Please select a supplier before submitting.")
        
        # =========================================================
        # 7. THE GATEWAY (CONDITION + ASSIGNMENT)
        #    This translates your BPMN Exclusive Gateway into Python.
        #    - If total_price > 10000 -> Path A (Procurement)
        #    - Else                  -> Path B (Manager)
        # =========================================================
        if request.total_price > 10000:
            request.status = RequestStatus.PENDING_PROCUREMENT
        else:
            request.status = RequestStatus.PENDING_MANAGER
        
        # =========================================================
        # 8. DATABASE SAVE (Writing data)
        #    db.commit() -> Saves the new status to PostgreSQL.
        # =========================================================
        db.commit()
        
        # =========================================================
        # 9. RETURN (Output)
        #    Gives the updated request back to the Controller.
        # =========================================================
        return request
    
    
    # INSIDE the Service Layer (request_service.py)
@staticmethod
# =========================================================
# FILE: app/services/request_service.py (continued)
# =========================================================

from sqlalchemy.orm import Session
from app.models.purchase_request import PurchaseRequest, RequestStatus
from app.models.user import User  # <-- We import the User model to check roles

class RequestService:

    # ... (submit_for_approval method is above) ...

    # =========================================================
    # METHOD: approve_request
    # Type: @staticmethod
    # Purpose: Handles the "Approve" or "Reject" action from the BPMN.
    #          This maps to the User Tasks in Lane 2 (Manager) and Lane 3 (Procurement).
    # Parameters:
    #   - db: The database session.
    #   - request_id: Which request is being approved/rejected.
    #   - current_user: The logged-in user (passed from the Controller).
    #   - decision: "approved" or "rejected" (sent from the frontend).
    # Returns: The updated PurchaseRequest object.
    # =========================================================
    @staticmethod
    def approve_request(
        db: Session, 
        request_id: int, 
        current_user: User,      # <-- The user making the request
        decision: str            # <-- "approved" or "rejected"
    ):
        # =========================================================
        # 1. DATABASE QUERY: Fetch the request from the database.
        # =========================================================
        request = db.query(PurchaseRequest).filter(PurchaseRequest.id == request_id).first()
        
        # =========================================================
        # 2. BUSINESS RULE (Role-Based Access Control - RBAC):
        #    Check: Is the current user allowed to approve this?
        #    - Only "manager" can approve PENDING_MANAGER requests.
        #    - Only "procurement" can approve PENDING_PROCUREMENT requests.
        #    If the user has the wrong role, block them with an error.
        # =========================================================
        if request.status == RequestStatus.PENDING_MANAGER and current_user.role != "manager":
            raise PermissionError("Only Managers can approve this request.")
            
        if request.status == RequestStatus.PENDING_PROCUREMENT and current_user.role != "procurement":
            raise PermissionError("Only Procurement team can approve this high-value request.")
        
        # =========================================================
        # 3. BUSINESS RULE: Prevent approving a request that isn't pending.
        #    If someone tries to approve a DRAFT or already APPROVED request, block it.
        # =========================================================
        if request.status not in [RequestStatus.PENDING_MANAGER, RequestStatus.PENDING_PROCUREMENT]:
            raise ValueError("This request is not pending approval.")
        
        # =========================================================
        # 4. THE GATEWAY 2 (Approval Outcome):
        #    This matches your BPMN "Approved?" Exclusive Gateway.
        #    - If "approved": Move to ORDER_PLACED (trigger the Service Task).
        #    - If "rejected": Move to REJECTED (go back to requester).
        # =========================================================
        if decision == "approved":
            # =========================================================
            # SERVICE TASK TRIGGER:
            # In the BPMN, after approval, the flow goes to the 
            # "Generate PO & Send to Supplier" Service Task.
            # We call this function immediately after setting the status.
            # =========================================================
            request.status = RequestStatus.ORDER_PLACED
            
            # This triggers the external call to the supplier API.
            # (We will implement this function separately).
            send_order_to_supplier(request.id)  
            
        else:
            # Rejected: goes back to the requester.
            request.status = RequestStatus.REJECTED
        
        # =========================================================
        # 5. DATABASE SAVE: Write the new status to PostgreSQL.
        # =========================================================
        db.commit()
        
        # =========================================================
        # 6. RETURN: Send the updated request back to the Controller.
        # =========================================================
        return request
    

    class RequestService:

    @staticmethod
    def submit_for_approval(db: Session, request_id: int):
        # ... existing code ...

    @staticmethod
    def approve_request(db: Session, request_id: int, current_user: User, decision: str):
        # ... existing logic ...
        
        if decision == "approved":
            request.status = RequestStatus.ORDER_PLACED
            
            # CALL THE NEW METHOD HERE
            RequestService._send_order_to_supplier(request.id)  
            
        # ... rest of code ...

    # NEW METHOD: Handles the "Service Task" from BPMN
    @staticmethod
    def _send_order_to_supplier(request_id: int):
        # This is where you would call an external API (e.g., the supplier's system)
        # For now, we just print a message.
        print(f"Order {request_id} sent to supplier!")
        # Future: HTTP request to supplier API
    


# Your IDE auto-completes this. No typos!
request.status = RequestStatus.PENDING_MANAGER  # Always correct