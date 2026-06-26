from sqlalchemy.orm import Session

from models.enums import RequestStatus
from models.purchase_request import PurchaseRequest
from models.users import User

from services.order_service import OrderService


class RequestService:
    @staticmethod
    def submit_for_approval(db: Session, request_id: int):
        request = db.query(PurchaseRequest).filter(PurchaseRequest.id == request_id).first()

        if request is None:
            raise ValueError("Purchase request not found.")

        if request.status != RequestStatus.DRAFT.value:
            raise ValueError("Only draft requests can be submitted.")

        if not request.supplier_id:
            raise ValueError("Please select a supplier before submitting.")

        request.status = (
            RequestStatus.PENDING_PROCUREMENT.value
            if (request.total_price or 0) > 10000
            else RequestStatus.PENDING_MANAGER.value
        )

        db.commit()
        db.refresh(request)
        return request

    @staticmethod
    def approve_request(db: Session, request_id: int, current_user: User, decision: str):
        request = db.query(PurchaseRequest).filter(PurchaseRequest.id == request_id).first()

        if request is None:
            raise ValueError("Purchase request not found.")

        if request.status == RequestStatus.PENDING_MANAGER.value and current_user.role != "manager":
            raise PermissionError("Only Managers can approve this request.")

        if request.status == RequestStatus.PENDING_PROCUREMENT.value and current_user.role != "procurement":
            raise PermissionError("Only Procurement team can approve this high-value request.")

        if request.status not in [RequestStatus.PENDING_MANAGER.value, RequestStatus.PENDING_PROCUREMENT.value]:
            raise ValueError("This request is not pending approval.")

        if decision == "approved":
            request.status = RequestStatus.ORDER_PLACED.value
            OrderService.send_to_supplier(request)
        elif decision == "rejected":
            request.status = RequestStatus.REJECTED.value
        else:
            raise ValueError("decision must be either 'approved' or 'rejected'.")

        db.commit()
        db.refresh(request)
        return request